# 核心区块链模式

＃＃ 目录

1.【模式：智能合约架构】(#pattern-smart-contract-architecture)
2. [模式：安全第一开发](#pattern-security-first-development)
3. [模式：Gas优化](#pattern-gas-optimization)
4. [模式：测试策略](#pattern-testing-strategy)
5. [模式：可升级合约](#pattern-upgradeable-contracts)
6. [模式：DeFi 协议模式](#pattern-defi-protocol-patterns)
7. [模式：代币标准](#pattern-token-standards)
8. [模式：多提供商架构](#pattern-multi-provider-architecture)
9. [模式：带有 MediatR 的 CQRS](#pattern-cqrs-with-mediatr)
10. [模式：Webhook 安全](#pattern-webhook-security)
11. [模式：交易生命周期](#pattern-transaction-lifecycle)
12. [模式：事件驱动的加密支付](#pattern-event-driven-crypto- payments)
13. [链上数据与链下数据](#on-chain-vs-off-chain-data)

## 模式：智能合约架构

**使用时间：**设计生产智能合约。

**原则：**
- 关注点分离（逻辑、存储、访问控制）
- 最小信任假设
- 故障安全默认设置（白名单与黑名单）
- 用于紧急停止的断路器
- 需要时可升级模式
- 尽可能不可变的核心逻辑

**标准架构：**
```
Contracts/
├── interfaces/          # External interfaces
├── libraries/           # Reusable logic
├── tokens/              # ERC20, ERC721, ERC1155
├── core/                # Protocol logic
├── governance/          # DAO and voting
├── utils/               # Helpers
└── mocks/               # Test contracts
```

**清单：**
- [ ] 访问控制（OpenZeppelin AccessControl/Ownable）
- [ ] 状态改变函数的重入防护
- [ ] 输入验证和边界检查
- [ ] 所有状态变化的事件
- [ ] NatSpec 文档
- [ ] Gas 优化回顾
- [ ] 紧急暂停机制
- [ ] 记录升级策略

---

## 模式：安全第一的开发

**使用场合：**构建任何智能合约（安全性是不可协商的）。

**需要预防的关键漏洞：**

**1.可重入**
```solidity
// BAD: VULNERABLE
function withdraw() public {
    uint amount = balances[msg.sender];
    (bool success,) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] = 0;
}

// GOOD: SECURE (Checks-Effects-Interactions)
function withdraw() public nonReentrant {
    uint amount = balances[msg.sender];
    balances[msg.sender] = 0;  // Update state BEFORE external call
    (bool success,) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

**2.整数上溢/下溢**
```solidity
// GOOD: Use Solidity 0.8.0+ (automatic overflow checks)
// Or OpenZeppelin SafeMath for <0.8.0
```

**3.访问控制**
```solidity
// BAD: VULNERABLE
function setAdmin(address newAdmin) public {
    admin = newAdmin;
}

// GOOD: SECURE
function setAdmin(address newAdmin) public onlyOwner {
    require(newAdmin != address(0), "Zero address");
    emit AdminChanged(admin, newAdmin);
    admin = newAdmin;
}
```

**4.抢先交易/MEV**
```solidity
// GOOD: Use commit-reveal schemes or Flashbots for sensitive operations
function commitOrder(bytes32 commitment) external;
function revealOrder(uint256 amount, bytes32 salt) external;
```

**5.委托调用不受信任的合约**
```solidity
// BAD: VULNERABLE
target.delegatecall(data);

// GOOD: SECURE (whitelist known implementations)
require(isApprovedImplementation[target], "Untrusted target");
target.delegatecall(data);
```

**安全检查表：**
- [ ] 所有外部调用都使用检查-效果-交互模式
- [ ] 所有状态改变函数的重入防护
- [ ] 特权功能的访问控制
- [ ] 输入验证与自定义错误
- [ ] 没有未经检查的外部调用
- [ ] 为所有状态更改发出事件
- [ ] 考虑循环的 Gas 限制
- [ ] Oracle 数据经过验证且未过时
- [ ] 可升级合约使用存储空间
- [ ] 针对主网状态进行了分叉测试

---

## 模式：Gas 优化

**使用时间：**优化合约部署和执行成本。

**存储优化：**
```solidity
// BAD: EXPENSIVE (multiple storage slots)
uint8 a;
uint256 b;
uint8 c;

// GOOD: OPTIMIZED (packed into single slot)
uint8 a;
uint8 c;
uint256 b;

// GOOD: OPTIMIZED (use uint256 for small numbers if not packing)
uint256 counter;  // cheaper than uint8 if standalone
```

**内存与存储：**
```solidity
// BAD: EXPENSIVE
function sum(uint[] storage arr) internal returns (uint) {
    uint total = 0;
    for(uint i = 0; i < arr.length; i++) {
        total += arr[i];  // SLOAD each iteration
    }
    return total;
}

// GOOD: OPTIMIZED
function sum(uint[] storage arr) internal returns (uint) {
    uint total = 0;
    uint length = arr.length;  // Cache length
    for(uint i = 0; i < length;) {
        total += arr[i];
        unchecked { ++i; }  // Save gas on overflow check
    }
    return total;
}
```

**通话数据与内存：**
```solidity
// BAD: MORE EXPENSIVE
function process(uint[] memory data) external { }

// GOOD: CHEAPER (for external functions)
function process(uint[] calldata data) external { }
```

**自定义错误：**
```solidity
// BAD: EXPENSIVE
require(amount > 0, "Amount must be greater than zero");

// GOOD: CHEAPER
error InvalidAmount();
if (amount == 0) revert InvalidAmount();
```

**气体优化清单：**
- [ ] 将存储变量打包到 32 字节槽中
- [ ] 使用 `calldata` 作为外部函数参数
- [ ] 在内存/堆栈中缓存存储变量
- [ ] 使用“unchecked”进行安全算术
- [ ] 自定义错误而不是需要字符串
- [ ] 尽可能使用不可变变量
- [ ] 批量操作以减少交易数量
- [ ] 在适用的情况下使用事件而不是存储

---

## 模式：测试策略

**使用时间：** 确保合同的正确性和安全性。

**测试金字塔：**
```
Unit Tests (80%)      - Individual functions, edge cases
Integration Tests (15%) - Multi-contract interactions
Fork Tests (5%)        - Mainnet state, protocol integrations
Invariant Tests        - Fuzzing, property-based testing
```

**铸造厂示例（Solidity）：**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/Token.sol";

contract TokenTest is Test {
    Token token;
    address alice = address(0x1);
    address bob = address(0x2);

    function setUp() public {
        token = new Token("Test", "TST");
        deal(alice, 100 ether);
    }

    function testTransfer() public {
        vm.startPrank(alice);
        token.transfer(bob, 100);
        assertEq(token.balanceOf(bob), 100);
        vm.stopPrank();
    }

    function testFuzzTransfer(uint256 amount) public {
        vm.assume(amount <= token.balanceOf(alice));
        vm.prank(alice);
        token.transfer(bob, amount);
        assertEq(token.balanceOf(bob), amount);
    }

    function invariant_totalSupplyConstant() public {
        assertEq(token.totalSupply(), 1_000_000e18);
    }
}
```

**锚示例（Rust/Solana）：**
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use anchor_lang::prelude::*;

    #[test]
    fn test_initialize() {
        let program_id = Pubkey::new_unique();
        let mut accounts = initialize_accounts();

        let result = initialize(
            Context::new(&program_id, &mut accounts, &[], BTreeMap::new()),
            100
        );

        assert!(result.is_ok());
    }
}
```

**测试清单：**
- [ ] 所有功能的单元测试
- [ ] 边缘情况（零值、最大 uint256、空数组）
- [ ] 访问控制测试（未经授权的调用失败）
- [ ] 重入攻击测试
- [ ] 使用随机输入进行模糊测试
- [ ] 针对实时协议进行分叉测试
- [ ] 天然气基准测试
- [ ] 多合约流程的集成测试
- [ ] 协议属性的不变测试
- [ ] 测试覆盖率 >90%

---

## 模式：可升级合约

**在以下情况下使用：** 协议需要未来改进或错误修复。

**代理模式：**

- **透明代理** (OpenZeppelin)：管理员/用户分离，实施升级
- **UUPS** (EIP-1822)：实施中的升级逻辑，gas 效率高
- **钻石标准** (EIP-2535)：多方面、模块化功能
- **信标代理**：多个代理共享一个实现

**关键考虑因素：**
```solidity
// GOOD: Use initializer instead of constructor
function initialize(uint256 _supply) public initializer {
    __Ownable_init();
    totalSupply = _supply;
}

// GOOD: Storage gaps for future variables
uint256[50] private __gap;

// GOOD: Namespace storage (EIP-7201)
bytes32 private constant STORAGE_LOCATION = keccak256("myprotocol.storage");
```

**可升级性清单：**

- [ ] 使用初始值设定项而不是构造函数
- [ ] 包括基础合约中的存储缺口
- [ ] 永远不要改变现有状态变量的顺序
- [ ] 在分叉测试中测试升级场景
- [ ] 升级功能的时间锁（24-48 小时）
- [ ] 独立于升级的紧急暂停

有关详细的代理实现和升级模式，请参阅 [references/solidity-best-practices.md](solidity-best-practices.md)。

---

## 模式：DeFi 协议模式

**使用场合：**构建去中心化金融应用程序。

**核心 DeFi 模式：**

- **AMM（自动做市商）**：恒定乘积公式（x * y = k），流动性池
- **贷款**：抵押借款、清算机制、利率模型
- **质押**：奖励分配、时间加权奖励、提前提现惩罚
- **Yield Farming**：多代币奖励、增加质押、归属时间表

**关键的 DeFi 安全：**
```solidity
// GOOD: Slippage protection
function swap(uint amountIn, uint minAmountOut) external {
    uint amountOut = calculateSwap(amountIn);
    require(amountOut >= minAmountOut, "Slippage exceeded");
}

// GOOD: Oracle validation
function getPrice() internal view returns (uint) {
    uint price = oracle.latestAnswer();
    require(block.timestamp - oracle.latestTimestamp() < 1 hours, "Stale price");
    return price;
}
```

** DeFi 清单：**
- [ ] 掉期滑点保护
- [ ] 价格预言机集成（TWAP/Chainlink）
- [ ] 闪电贷保护（余额检查）
- [ ] 清算机制已测试
- [ ] 利率模型已验证
- [ ] 紧急撤回功能

请参阅 [references/solidity-best-practices.md](solidity-best-practices.md) 了解详细的 DeFi 实现（AMM、借贷、质押）。

---

## 模式：代币标准

**在以下情况下使用：** 实现可替代或不可替代的代币。

**标准实施：**

- **ERC20**：可替代代币（使用 OpenZeppelin ERC20）
- **ERC721**：具有唯一 ID 的 NFT（元数据的 ERC721URIStorage）
- **ERC1155**：多代币（同质化 + NFT 在一份合约中）
- **SPL 代币**：Solana 可替代代币（通过 Anchor）
- **Jetton**：TON 可替代代币 (FunC/Tact)

**快速参考：**
```solidity
// ERC20 with OpenZeppelin
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
contract MyToken is ERC20 {
    constructor() ERC20("MyToken", "MTK") {
        _mint(msg.sender, 1_000_000e18);
    }
}
```

**代币清单：**

- [ ] 定义十进制精度（对于 ERC20，通常为 18）
- [ ] 总供应上限或铸币机构控制
- [ ] 刻录功能（如果需要）
- [ ] 紧急情况下可暂停（OpenZeppelin 可暂停）
- [ ] 无气体认证许可证 (EIP-2612)

有关 ERC721、ERC1155 和特定于链的代币实现，请参阅 [references/solidity-best-practices.md](solidity-best-practices.md)。

---

# 模板

请参阅“assets/”目录以了解区块链特定的实现，按链组织：

- `ethereum/template-solidity-hardhat.md` - 带有 Hardhat、OpenZeppelin、Ethers.js 的以太坊/EVM
- `ethereum/template-solidity-foundry.md` - 带有 Foundry、Forge、Cast 的以太坊/EVM
- `solana/template-rust-anchor.md` - 具有 Anchor 框架、SPL 代币的 Solana
- `cosmos/template-cosmwasm.md` - 具有 CosmWasm 智能合约的 Cosmos 生态系统
- `bitcoin/template-bitcoin-core.md` - 使用比特币核心进行比特币开发

可以为其他链添加更多模板（Polkadot Substrate、Avalanche、Near 等）

---

＃ 资源

**最佳实践指南**（`参考文献/`）

- `backend-integration-best-practices.md` - .NET/C# 加密集成模式，包括：
  - CQRS 与 MediatR 用于支付/钱包命令
  - 使用 FluentResults 进行面向铁路的编程
  - 多提供商架构（TON、Fireblocks、TG 钱包）
  - Webhook签名验证（HMAC，恒定时间比较）
  - Kafka 的事件驱动架构
  - 交易生命周期状态机
  - HTTP 客户端弹性（Polly 策略）
  - 测试模式（夹具、Wiremock、测试容器）
- `blockchain-best-practices.md` - 通用区块链模式包括：
  - 智能合约架构和设计
  - 安全模式和漏洞预防
  - 气体优化技术
  - 测试策略（单元、集成、分叉、不变量）
  - 部署和验证工作流程
  - 多链考虑
- `solidity-best-practices.md` - 以太坊/EVM 特定模式，包括：
  - Solidity语言的特点和陷阱
  - OpenZeppelin 库的使用
  - EVM 操作码和 Gas 成本
  - 代理模式和可升级性
  - DeFi协议实现
  - MEV保护策略
- `rust-solana-best-practices.md` - Solana 特定模式，包括：
  - 锚框架模式
  - 程序派生地址 (PDA)
  - 跨程序调用（CPI）
  - 账户数据结构
  - SPL 代币集成
  - Solana交易优化
- `cosmwasm-best-practices.md` - Cosmos 特定模式，包括：
  - CosmWasm合约结构
  - IBC（区块链间通信）
  - Cosmos SDK集成
  - 代币标准（CW20、CW721）
  - 治理模块
- `ton-best-practices.md` - TON 特定模式，包括：
  - FunC 和 Tact 语言功能
  - TON 虚拟机（TVM）优化
  - Jetton和NFT标准
  - TON Connect 集成
  - Telegram Bot API 模式

**智能合约安全**（参见 [software-security-appsec](../../software-security-appsec/SKILL.md) 技能）：

- [../software-security-appsec/references/smart-contract-security-auditing.md](../../software-security-appsec/references/smart-contract-security-auditing.md) - 全面的智能合约安全：
  - 常见漏洞模式（重入、访问控制、预言机操纵）
  - 审核清单和方法
  - 正式验证工具（Slither、Mythril、Echidna、Certora）
  - 测试框架和覆盖策略
  - 错误赏金计划设置

**外部文档：**
请参阅 [data/sources.json](../data/sources.json) 了解官方文档链接和学习资源。

---

# 后端集成模式

## 模式：多提供商架构

**使用场合：**构建需要多个区块链提供商的企业加密集成。

**提供者抽象：**
```csharp
// Abstract interface for provider operations
public interface ICryptoProvider
{
    CryptoProvider ProviderType { get; }
    Task<Result<WalletInfo>> CreateWalletAsync(string userId, Currency currency);
    Task<Result<TransactionInfo>> CreatePayoutAsync(PayoutRequest request);
}

// Provider selection based on currency/network
public class CalculateProviderService : ICalculateProviderService
{
    public Task<CryptoProvider> GetCryptoProviderAsync(Currency currency, CryptoNetwork network)
    {
        return (currency, network) switch
        {
            (Currency.TON, CryptoNetwork.TON) => CryptoProvider.TonDirect,
            (Currency.USDT, CryptoNetwork.TON) => CryptoProvider.TonDirect,  // Jetton
            (Currency.ETH, CryptoNetwork.Ethereum) => CryptoProvider.Fireblocks,
            _ => CryptoProvider.Fireblocks  // Default custodial
        };
    }
}
```

**提供商类型：**
- **直接区块链** (TonDirect)：非托管、直接 RPC 调用
- **保管** (Fireblocks)：托管密钥、合规性功能、AML
- **嵌入式钱包**（TG Wallet）：应用程序集成钱包

---

## 模式：带有 MediatR 的 CQRS

**使用场合：**构建具有复杂业务逻辑的加密支付/钱包服务。

```csharp
// Command with railway-oriented result
public record CreatePaymentCommand(
    string UserId,
    decimal Amount,
    Currency Currency
) : IRequest<Result<PaymentInfo>>;

// Handler with provider routing
public class CreatePaymentHandler : IRequestHandler<CreatePaymentCommand, Result<PaymentInfo>>
{
    public async Task<Result<PaymentInfo>> Handle(CreatePaymentCommand request, CancellationToken ct)
    {
        var provider = await _providerService.GetCryptoProviderAsync(request.Currency);

        return provider switch
        {
            CryptoProvider.TonDirect => await _mediator.Send(new TonCreatePaymentCommand(request)),
            CryptoProvider.Fireblocks => await _mediator.Send(new FireblocksCreatePaymentCommand(request)),
            _ => Result.Fail("Unsupported provider")
        };
    }
}
```

---

## 模式：Webhook 安全

**在以下情况下使用：** 从托管提供商（Fireblocks 等）接收 Webhooks。

```csharp
// HMAC signature validation with constant-time comparison
public bool ValidateSignature(string payload, string signature, string timestamp)
{
    var expectedSignature = ComputeHmacSha256($"{timestamp}.{payload}", _secret);
    return CryptographicOperations.FixedTimeEquals(
        Encoding.UTF8.GetBytes(signature),
        Encoding.UTF8.GetBytes(expectedSignature));
}

// Authentication handler for webhook endpoints
[Authorize(AuthenticationSchemes = "FireblocksWebhook")]
[HttpPost("webhooks/fireblocks")]
public async Task<IActionResult> HandleWebhook([FromBody] WebhookPayload payload)
{
    await _kafkaProducer.PublishAsync(new TransactionWebhookMessage(payload));
    return Ok();  // Always acknowledge receipt
}
```

**安全检查表：**
- [ ] 恒定时间签名比较（防止定时攻击）
- [ ] 时间戳验证（防止重放攻击）
- [ ] 幂等性处理（重复的 webhook 传递）
- [ ] 通过消息队列进行异步处理

---

## 模式：事务生命周期

**使用时间：**跟踪加密交易从创建到完成的状态。

```csharp
// State machine for transactions
public enum TransactionStatus { Created, Pending, Confirming, Completed, Failed }

public class TransactionStateMachine
{
    private static readonly Dictionary<(TransactionStatus, TransactionEvent), TransactionStatus>
        _transitions = new()
    {
        { (TransactionStatus.Created, TransactionEvent.Submitted), TransactionStatus.Pending },
        { (TransactionStatus.Pending, TransactionEvent.Broadcast), TransactionStatus.Confirming },
        { (TransactionStatus.Confirming, TransactionEvent.Confirmed), TransactionStatus.Completed },
        { (TransactionStatus.Pending, TransactionEvent.Rejected), TransactionStatus.Failed },
    };
}

// Background monitoring service
public class TransactionMonitoringService : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            var pending = await _repository.GetPendingTransactionsAsync();
            foreach (var tx in pending)
            {
                var status = await _blockchainClient.GetTransactionStatusAsync(tx.TxHash);
                if (status != tx.Status)
                    await _mediator.Send(new UpdateTransactionStatusCommand(tx.Id, status));
            }
            await Task.Delay(TimeSpan.FromSeconds(10), stoppingToken);
        }
    }
}
```

---

## 模式：事件驱动的加密支付

**使用时间：** 使用 Kafka 构建可扩展的支付处理。

```csharp
// Publish payment events
public class PaymentCompletedHandler : INotificationHandler<PaymentCompletedNotification>
{
    public async Task Handle(PaymentCompletedNotification notification, CancellationToken ct)
    {
        await _kafkaProducer.PublishAsync(new CryptoPaymentReceivedMessage
        {
            PaymentId = notification.PaymentId,
            Amount = notification.Amount.ToString(),
            Currency = notification.Currency.ToString(),
            TxHash = notification.TxHash
        });
    }
}

// Consume webhook messages
public class WebhookMessageHandler : IMessageHandler<TransactionWebhookMessage>
{
    public async Task HandleAsync(ConsumeResult<string, TransactionWebhookMessage> message, CancellationToken ct)
    {
        var result = await _mediator.Send(new ProcessTransactionCommand(message.Value));
        if (result.IsFailed)
            throw new MessageProcessingException(result.Errors.First().Message);
    }
}
```

有关完整模式，请参阅 [references/backend-integration-best-practices.md](backend-integration-best-practices.md)。

---

# 状态管理模式

## 链上数据与链下数据

**使用时间：**决定数据存储策略。

|数据类型 |存储|原因 |
|------------|---------|--------|
|余额、所有权|链上 |安全至关重要，需要达成共识|
| NFT 元数据 | IPFS + 链上 URI |不变性 + 成本效率 |
|历史数据|图/子图 |查询效率 |
|用户偏好 |链下数据库 |可变的、非关键的 |
|大文件 | Arweave/Filecoin |永久存储 |

---

# 跨链模式

**使用时：**构建多链协议。

**桥接策略：**
1. Lock-and-Mint（集中/联合）
2. 销毁并铸造（需要信任）
3. 流动性池（Hop协议）
4. 原子交换
5.IBC（区块链间通信-Cosmos）

**桥接安全注意事项：**
- [ ] 验证人设置去中心化
- [ ] 防欺诈机制
- [ ] 提款速率限制
- [ ] 多重签名要求
- [ ] 异常断路器

---

＃ 结尾
