# DeFi 协议实现模式

用于构建去中心化金融 (DeFi) 协议的生产级模式：涵盖 AMM/DEX、借贷、质押、流动性挖矿、闪电贷以及预言机集成。包括 EVM (Solidity) 和 Solana 实现及安全性考量。

---

## 目录

1. [AMM 与 DEX 模式](#amm-与-dex-模式)
2. [借贷协议模式](#借贷协议模式)
3. [质押与奖励分发](#质押与奖励分发)
4. [流动性挖矿与金库模式](#流动性挖矿与金库模式)
5. [闪电贷 (Flash Loans)](#闪电贷)
6. [预言机 (Oracle) 集成](#预言机集成)
7. [价格操纵防范](#价格操纵防范)
8. [DeFi 可组合性与协议风险](#defi-可组合性与协议风险)
9. [开发反模式](#开发反模式)

---

## AMM 与 DEX 模式

### 恒定乘积 AMM (Uniswap V2 模型)

这是最简单且被分叉最广泛的 AMM 模型。恒定乘积公式 `x * y = k` 决定了资产价格。

```solidity
// 核心交换逻辑 (简化的 Uniswap V2 模式)
contract ConstantProductAMM {
    IERC20 public tokenA;
    IERC20 public tokenB;
    uint256 public reserveA;
    uint256 public reserveB;

    uint256 private constant FEE_NUMERATOR = 997;    // 0.3% 手续费
    uint256 private constant FEE_DENOMINATOR = 1000;

    function swap(
        address tokenIn,
        uint256 amountIn
    ) external returns (uint256 amountOut) {
        require(amountIn > 0, "Amount must be positive");
        require(
            tokenIn == address(tokenA) || tokenIn == address(tokenB),
            "Invalid token"
        );

        bool isTokenA = tokenIn == address(tokenA);
        (uint256 resIn, uint256 resOut) = isTokenA
            ? (reserveA, reserveB)
            : (reserveB, reserveA);

        // 扣除手续费后的输入量
        uint256 amountInWithFee = amountIn * FEE_NUMERATOR;

        // 恒定乘积公式: amountOut = (resOut * amountInWithFee) / (resIn * FEE_DENOMINATOR + amountInWithFee)
        amountOut = (resOut * amountInWithFee) /
            (resIn * FEE_DENOMINATOR + amountInWithFee);

        // 更新储备金状态
        if (isTokenA) {
            reserveA += amountIn;
            reserveB -= amountOut;
        } else {
            reserveB += amountIn;
            reserveA -= amountOut;
        }

        // 执行代币转账
        IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn);
        IERC20(isTokenA ? address(tokenB) : address(tokenA))
            .transfer(msg.sender, amountOut);
    }
}
```

**关键特性：**
- 价格滑点随着交易额占池深度的比例增加而增大。
- 流动性提供者 (LP) 按持股比例赚取手续费。
- 当代币价格与存入比例背离时会产生无常损失。
- 不依赖外部预言机——价格完全源自储备金比例。

### 集中流动性 (Uniswap V3 模型)

LP 可以在特定的价格区间（Ticks）内提供流动性，极大提高了资本效率。

```text
Uniswap V3 核心概念:
  - Ticks: 离散的价格点（每个 tick 代表 0.01% 的价格变化）
  - Positions: 在两个 tick 之间 [tickLower, tickUpper] 部署的流动性
  - 活跃流动性: 只有当当前价格处于该区间时，对应的流动性才能赚取手续费
  - 资本效率: 在窄区间内相比 V2 可提升 100-4000 倍
```

**设计选型对比：**

| 维度 | V2 模式 | V3 模式 | 权衡 |
|----------|------------|------------|----------|
| 流动性范围 | 全范围 (0, ∞) | 自定义范围 [a, b] | 收益更高，但需主动管理 |
| LP 令牌形式 | 同质化 (ERC-20) | 非同质化 (ERC-721) | 灵活性更高，但可组合性变难 |
| 手续费层级 | 固定 0.3% | 0.01%, 0.05%, 0.3%, 1% | 更好适配不同波动性的交易对 |
| 预言机机制 | 累积价格 | 几何平均 TWAP | 抗操纵能力更强 |

---

## 借贷协议模式

### Compound/Aave 借贷模型

借贷协议的核心架构：
```text
借贷协议架构:
  - 存款端: 用户存入资产，获得生息代币 (Interest-bearing tokens)
  - 借款端: 用户抵押资产，借出其它资产
  - 利率模型: 根据资金利用率 (Utilization) 由算法动态决定
  - 清算机制: 抵押率不足的仓位将被清算
```

### 抵押率与健康因子 (Health Factor)

```solidity
// 健康因子计算 (参考 Aave 模式)
contract LendingPool {
    // 抵押因子：决定抵押品能借出的最大额度
    // 如 0.75 表示 $100 的 ETH 抵押品最多借出 $75 资产
    mapping(address => uint256) public collateralFactor;

    // 清算阈值：决定仓位何时进入可清算状态
    // 如 0.80 表示当 借款额 / 抵押额 > 80% 时触发清算
    mapping(address => uint256) public liquidationThreshold;

    function healthFactor(address user) public view returns (uint256) {
        uint256 totalCollateralValue = getUserCollateralValue(user);
        uint256 totalBorrowValue = getUserBorrowValue(user);

        if (totalBorrowValue == 0) return type(uint256).max;

        // healthFactor = (抵押额 * 清算阈值) / 借款额
        // healthFactor < 1.0 表示仓位可被清算
        return (totalCollateralValue * liquidationThreshold[user]) /
            totalBorrowValue;
    }
}
```

### 利率曲线模型

```solidity
// 基于资金利用率的利率模型
contract InterestRateModel {
    uint256 public baseRate = 2e16;        // 2% 基础利率
    uint256 public slope1 = 4e16;          // 拐点前的增长斜率 (4%)
    uint256 public slope2 = 75e16;         // 拐点后的增长斜率 (75%，极陡)
    uint256 public optimalUtilization = 80e16; // 80% 拐点

    function getBorrowRate(
        uint256 totalBorrows,
        uint256 totalSupply
    ) public view returns (uint256) {
        if (totalSupply == 0) return baseRate;

        uint256 utilization = (totalBorrows * 1e18) / totalSupply;

        if (utilization <= optimalUtilization) {
            // 拐点前：斜率平缓
            return baseRate + (utilization * slope1) / optimalUtilization;
        } else {
            // 拐点后：斜率陡增（旨在激励用户还款）
            uint256 excessUtilization = utilization - optimalUtilization;
            uint256 maxExcess = 1e18 - optimalUtilization;
            return baseRate + slope1 + (excessUtilization * slope2) / maxExcess;
        }
    }
}
```

---

## 质押与奖励分发

### 时间加权奖励分发 (Synthetix 模式)

这是目前 DeFi 行业的标准质押算法。

```solidity
contract StakingRewards {
    IERC20 public stakingToken;
    IERC20 public rewardToken;

    uint256 public rewardRate;           // 每秒分发的奖励额
    uint256 public lastUpdateTime;
    uint256 public rewardPerTokenStored;
    uint256 public totalStaked;

    mapping(address => uint256) public userRewardPerTokenPaid;
    mapping(address => uint256) public rewards;
    mapping(address => uint256) public balances;

    modifier updateReward(address account) {
        rewardPerTokenStored = rewardPerToken();
        lastUpdateTime = block.timestamp;
        if (account != address(0)) {
            rewards[account] = earned(account);
            userRewardPerTokenPaid[account] = rewardPerTokenStored;
        }
        _;
    }

    function rewardPerToken() public view returns (uint256) {
        if (totalStaked == 0) return rewardPerTokenStored;
        return rewardPerTokenStored +
            ((block.timestamp - lastUpdateTime) * rewardRate * 1e18) /
            totalStaked;
    }

    function earned(address account) public view returns (uint256) {
        return (balances[account] *
            (rewardPerToken() - userRewardPerTokenPaid[account])) /
            1e18 + rewards[account];
    }

    function stake(uint256 amount) external updateReward(msg.sender) {
        totalStaked += amount;
        balances[msg.sender] += amount;
        stakingToken.transferFrom(msg.sender, address(this), amount);
    }

    function getReward() external updateReward(msg.sender) {
        uint256 reward = rewards[msg.sender];
        rewards[msg.sender] = 0;
        rewardToken.transfer(msg.sender, reward);
    }
}
```

---

## 流动性挖矿与金库模式

### ERC-4626 令牌化金库标准

```solidity
import "@openzeppelin/contracts/token/ERC20/extensions/ERC4626.sol";

contract YieldVault is ERC4626 {
    constructor(IERC20 asset_)
        ERC4626(asset_)
        ERC20("Vault Shares", "vSHARE")
    {}

    // 金库管理的总资产
    function totalAssets() public view override returns (uint256) {
        return asset.balanceOf(address(this)) + _getStrategyBalance();
    }

    // 存入资产获取份额 (Shares)
    // shares = (资产数 * 总份额) / 总资产
    // 销毁份额取回资产 (Assets)
    // assets = (份额数 * 总资产) / 总份额
}
```

---

## 闪电贷 (Flash Loans)

闪电贷允许用户在单个事务中无抵押借款，前提是必须在事务结束前归还。

**常见用例：**
- **套利 (Arbitrage)**：利用不同 DEX 间的价差获利。
- **清算 (Liquidation)**：借款执行抵押不足仓位的清算任务。
- **抵押品更换**：在不平仓的情况下更换抵押资产。
- **治理攻击预警**：通过借入大量令牌瞬间获得投票权（需通过快照机制防范）。

---

## 预言机 (Oracle) 集成

### Chainlink 价格喂价

```solidity
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract ChainlinkConsumer {
    AggregatorV3Interface internal priceFeed;
    uint256 private constant STALE_THRESHOLD = 3600; // 1 小时过期阈值

    function getPrice() public view returns (uint256) {
        (
            uint80 roundId,
            int256 price,
            ,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();

        // 必须执行的所有安全性检查
        require(price > 0, "Invalid price");
        require(updatedAt > 0, "Incomplete round");
        require(answeredInRound >= roundId, "Stale round data");
        require(
            block.timestamp - updatedAt < STALE_THRESHOLD,
            "Price data too old"
        );

        return uint256(price);
    }
}
```

---

## 价格操纵防范

**常见攻击向量与防御：**
- **闪电贷攻击**：通过巨额借款瞬间改变 AMM 现货价格。**防范：** 使用 TWAP 预言机或多源价格校验。
- **三明治攻击**：在大型交易前后进行抢跑和回跑。**防范：** 使用 MEV 保护（如私有内存池）和设置合理的滑点上限。
- **捐赠攻击**：通过直接转账代币抬高金库份额价格。**防范：** 引入“虚拟份额” (Virtual Shares) 机制。

---

## 开发反模式 (禁忌做法)

1. **依赖现货价格进行估值**：这是最常见的漏洞。绝对不要直接用 `getReserves()` 决定资产价值。
2. **无限额度的代币授权**：始终建议按需授权，或使用 `Permit2` 协议进行单次精准授权。
3. **缺少滑点保护**：如果 `amountOutMin` 设置为 0，交易将被 MEV 机器人吃掉所有利润。
4. **硬编码合约地址**：这会导致合约无法在其它链上部署或进行版本升级。
5. **没有紧急暂停机制**：在发现漏洞时，如果无法立即停止协议运行，损失将无法挽回。

---

## 交叉引用

- `blockchain-best-practices.md` —— 通用区块链安全模式。
- `solidity-best-practices.md` —— Solidity 特有的 Gas 优化与安全模式。
- `SKILL.md` —— DeFi 业务范围、预言机集成、MEV 保护概览。
