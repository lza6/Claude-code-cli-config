---
name: software-crypto-web3
description: "针对 EVM、Solana、Cosmos 和 TON 的安全区块链开发。在构建智能合约、审计或集成链上后端时使用。"
---

# 软件加密与 Web3 工程 (Software Crypto/Web3)

使用此技能来设计、实施和审查安全的区块链系统，包括：智能合约、链上/链下集成、托管与签名、测试、审计及生产运营。

默认原则：**安全优先开发**、明确的威胁模型、全方位的测试（单元测试+集成测试+分叉测试+模糊测试/不变量测试）、高价值场景下的形式化方法、可升级的安全性（时间锁、治理、回滚计划）以及密钥托管与签名的深度防御。

---

## 快速参考表

| 任务 | 工具/框架 | 常用命令 | 使用场景 |
|------|----------------|---------|-------------|
| Solidity 开发 | Hardhat/Foundry | `npx hardhat init` 或 `forge init` | 以太坊/EVM 智能合约 |
| Solana 开发 | Anchor | `anchor init` | Solana 区块链开发 |
| Cosmos 合约 | CosmWasm | `cargo generate --git cosmwasm-template` | Cosmos 生态系统合约 |
| TON 合约 | Tact/FunC + Blueprint | `npm create ton@latest` | TON 区块链开发 |
| 可靠性测试 | Foundry/Hardhat | `forge test` 或 `npx hardhat test` | 单元、分叉、不变量测试 |
| 安全审计 | Slither/Aderyn/Echidna | `slither .` 或 `aderyn .` | 静态分析、模糊测试 |
| AI 辅助审查 | AI 扫描器 (可选) | N/A | 预审计准备（需人工验证结果）|
| 模糊测试 | Echidna/Medusa | `echidna` 或 `medusa fuzz` | 基于属性的模糊测试 |
| Gas 优化 | Foundry Gas 快照 | `forge snapshot` | 基准测试与优化 Gas 消耗 |
| 部署任务 | Hardhat Deploy/Forge Script | `npx hardhat deploy` | 主网/测试网部署 |
| 合约验证 | Etherscan API | `npx hardhat verify` | 源代码验证 |
| 可升级合约 | OpenZeppelin Upgrades | `@openzeppelin/hardhat-upgrades` | 基于代理 (Proxy) 的升级 |
| 智能钱包 | ERC-4337, EIP-7702 | 账户抽象 (AA) SDK | 智能账户与赞助 Gas (需验证网络支持) |

## 适用范围

当您需要进行以下工作时，请使用此技能：

- 智能合约开发 (Solidity, Rust, CosmWasm)
- DeFi 协议实施 (AMM, 借贷, 质押, 流动性挖矿)
- NFT 与令牌标准 (ERC-20, ERC-721, ERC-1155, SPL Token)
- DAO 治理系统开发
- 跨链桥接与互操作性方案
- Gas 优化与存储模式设计
- 智能合约安全审计
- 测试策略制定 (Foundry, Hardhat, Anchor)
- 预言机 (Oracle) 集成 (Chainlink, Pyth)
- 可升级合约模式 (Proxy, Diamond)
- Web3 前端集成 (ethers.js, web3.js, @solana/web3.js)
- 区块链数据索引 (The Graph, Subgraphs)
- MEV 保护与闪电贷机器人开发
- L2 扩容方案 (Base, Arbitrum, Optimism, zkSync)
- 账户抽象 (ERC-4337, EIP-7702, 智能钱包)
- **后端加密集成** (.NET/C#, 多提供商架构, CQRS)
- Webhook 处理与签名验证 (Fireblocks, 托管服务商)
- 基于 Kafka 的加密支付事件驱动架构
- 交易生命周期管理与监控
- 钱包管理 (托管与非托管)

## 决策树：区块链平台选择

```text
项目需求: [使用场景]
  - 是否需要兼容 EVM 的智能合约？
    - 复杂的测试需求 -> Foundry (支持模糊测试、不变量、Gas 快照)
    - TypeScript 生态偏好 -> Hardhat (丰富插件、TS 支持、Ethers.js/Viem)
    - 企业级功能 -> NestJS + Hardhat

  - 追求高吞吐量 / 低费用？
    - 基于 Rust 生态 -> Solana (Anchor)
    - EVM L2 方案 -> Arbitrum/Optimism/Base (共享以太坊安全性，极低 Gas)
    - 结合 Telegram 分发 -> TON (Tact/FunC)

  - 追求跨链互操作性？
    - Cosmos 生态 -> CosmWasm (IBC 协议)
    - 多链应用 -> LayerZero 或 Wormhole (需验证其信任假设)
    - 自研桥接 -> 风险极高；需建立严密的威胁模型

  - 代币标准实施？
    - 同质化代币 -> ERC20 (OpenZeppelin), SPL Token (Solana)
    - NFT -> ERC721/ERC1155 (OpenZeppelin), Metaplex (Solana)
    - 半同质化代币 -> ERC1155 (适用于游戏、碎片化 NFT)

  - DeFi 协议开发？
    - AMM/DEX -> Uniswap V3 分叉或自定义 (集中流动性)
    - 借贷协议 -> Compound/Aave 分叉 (抵押借贷)
    - 质押/收益 -> 自定义奖励分配合约

  - 需要合约可升级？
    - 透明代理 (Transparent) -> OpenZeppelin (实现管理员/用户权限分离)
    - UUPS 代理 -> 升级逻辑集成在实现合约中
    - 钻石模式 (Diamond) -> 模块化功能扩展 (EIP-2535)

  - 后端集成方案？
    - .NET/C# -> 采用多提供商架构 (参见后端集成参考)
    - Node.js -> Ethers.js/Viem + 持久化队列
    - Python -> Web3.py + FastAPI
```

**各链特定注意事项：**
- **以太坊/EVM**：安全第一、Gas 成本较高、生态系统最庞大。
- **Solana**：性能优先、需使用 Rust 语言、费用极低。
- **Cosmos**：互操作性优先、原生支持 IBC、生态持续增长。
- **TON**：Telegram 生态优先、异步合约调用、架构独特。

请参阅 `references/` 目录以获取各链的最佳实践。

---

## 安全优先模式 (2026 年 1 月更新)

> **安全基线**：假设处于对抗性环境。将合约和签名基础设施视为完全公开、随时可能受攻击的 API。

### 托管、密钥与签名 (核心)

密钥管理是生产级加密系统中最主要的风险来源。请参考真实的密钥管理标准（如 [NIST SP 800-57](https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final)）。

| 模式 | 密钥持有者 | 典型用途 | 主要风险 | 默认控制措施 |
|------|-----------------|------------------------|------------------------|--------------------|
| 非托管 | 最终用户钱包 | 消费者应用、自我托管 | 钓鱼、授权错误、用户操作失误 | 硬件钱包支持、清晰的签名 UI、交互白名单 |
| 托管 | 您的服务 (HSM/MPC) | 交易平台、支付、B2B | 密钥失窃、内部威胁、操作失误 | 使用 HSM/MPC、职责分离、限额/审批、审计日志 |
| 混合 | 责任共担 | 企业级应用 | 复杂的故障模式 | 明确的恢复/覆盖路径、完善的操作手册 |

**最佳实践：**
- 建立相互独立的“热/温/冷”签名路径，并设置限额和审批流。
- 高额转账必须经过双重控制（策略引擎验证 + 人工审批）。
- 为每一次签名请求保留不可篡改的审计追踪（谁、什么时间、操作内容、原因）。

**禁忌做法：**
- 严禁在数据库或应用配置文件中明文存储私钥。
- 严禁跨环境（开发/预发/生产）重复使用签名密钥。
- 严禁在没有速率限制和“熔断机制”的情况下运行热钱包自动化。

### “检查-效果-交互” (CEI) 模式

**所有状态修改函数必须遵循此模式**。

```solidity
// 正确做法: CEI 模式
function withdraw(uint256 amount) external {
    // 1. 检查 (Checks): 验证所有前提条件
    require(balances[msg.sender] >= amount, "余额不足");

    // 2. 效果 (Effects): 在进行外部调用之前更新内部状态
    balances[msg.sender] -= amount;

    // 3. 交互 (Interactions): 将外部调用放在最后执行
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "转账失败");
}

// 错误做法: 在更新状态前进行外部调用（极易导致重入攻击）
function withdrawUnsafe(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] -= amount; // 更新太晚了！
}
```

### 安全工具箱 (2026 年 1 月更新)

| 类别 | 工具名称 | 核心用途 | 使用建议 |
|----------|------|---------|------------|
| 静态分析 | Slither | 漏洞检测，内置 92+ 种检测器 | 每个合约必用 |
| 静态分析 | Aderyn | 基于 Rust，处理大型代码库速度极快 | 大型项目推荐 |
| 模糊测试 | Echidna | 基于属性的模糊测试 | 处理复杂状态时必用 |
| 模糊测试 | Medusa | 并行化的 Go 语言模糊测试工具 | 集成到 CI/CD 流水线 |
| 形式化验证 | SMTChecker | Solidity 内置的逻辑检查器 | 每个合约推荐使用 |
| 形式化验证 | Certora | 基于属性的证明 (CVL) | DeFi 及高价值合约必用 |
| 形式化验证 | Halmos | 符号执行测试 | 验证复杂的不变量 |
| AI 辅助 | Sherlock AI | 机器学习驱动的漏洞检测 | 审计前预检 |
| AI 辅助 | Olympia | 集成到 DevSecOps | CI/CD 环节安全加固 |
| AI 辅助 | Auditless | 423+ 检测器，由 LLM 驱动 | 审查业务逻辑漏洞 |
| 突变测试 | Sumi | 评估测试套件的覆盖质量 | 验证测试的有效性 |

```solidity
// Certora CVL 验证规则示例
rule balanceNeverNegative(address user) {
    env e;
    require balances[user] >= 0;
    deposit(e);
    assert balances[user] >= 0;
}
```

> **注意**：使用 AI 工具应仅用于审计前的预检和辅助覆盖，不能替代最终的安全决策。应将其输出视为不可信，必须通过确定性工具、测试和人工复核来验证结果。

### MEV (最大可提取价值) 保护

| 保护策略 | 具体实施方式 |
|----------|----------------|
| 私有内存池 | 使用 Flashbots Protect、MEV Blocker |
| “提交-揭示”模式 | 使用哈希承诺，在截止日期后揭晓内容 |
| 批量拍卖 | 使用 CoW Protocol、Gnosis Protocol |
| 加密内存池 | 使用 Shutter Network |

```solidity
// “提交-揭示” (Commit-Reveal) 模式示例
mapping(address => bytes32) public commitments;

function commit(bytes32 hash) external {
    commitments[msg.sender] = hash;
}

function reveal(uint256 value, bytes32 salt) external {
    require(
        keccak256(abi.encodePacked(value, salt)) == commitments[msg.sender],
        "揭示验证失败"
    );
    // 逻辑处理揭示后的真实数值
}
```

---

## 账户抽象 (AA) (2026 年 1 月更新)

> **注意**：账户抽象的采用率和协议升级计划变化极快。在提出具体方案前，请务必使用 `WebSearch` 验证 ERC-4337 生态系统的当前状态以及 EIP-7702 的激活细节。

### ERC-4337 与 EIP-7702 对比

| 标准 | 类型 | 核心特点 | 典型场景 |
|----------|------|-------------|----------|
| ERC-4337 | 智能合约钱包 | 无需修改以太坊协议的完整 AA 方案 | 新用户钱包、DeFi 深度集成、游戏 |
| EIP-7702 | EOA 账户增强 | 让普通 EOA 账户能执行合约代码 | 现有钱包升级、批量交易处理 |
| ERC-6900 | 模块化账户 | AA 钱包的插件化管理标准 | 可扩展、可定制的钱包功能 |

**ERC-4337 运作架构：**
```text
用户 -> UserOperation (用户操作) -> Bundler (打包器) -> EntryPoint (入口合约) -> 智能账户 -> 目标合约
                                    |
                                    v
                                Paymaster (Gas 赞助商)
```

**EIP-7702 (Pectra 升级相关)：**
- 普通 EOA 账户可以临时委派给智能合约。
- 支持批量交易，并能为现有地址提供赞助 Gas。
- 与 ERC-4337 互补（共用 Bundler/Paymaster 基础设施）。
- 已获得 Ambire, Trust Wallet 等越来越多钱包的支持。

**核心能力：**
- **免 Gas 交易**：通过 Paymasters 使用 ERC-20 代币或法币代付 Gas 费。
- **批量操作**：在单个事务中完成多个操作。
- **社交恢复**：支持多重签名或基于受托人的密钥恢复机制。
- **会话密钥 (Session keys)**：为 dApp 分配有限权限，无需完全授权钱包。

---

## L2 (第二层网络) 开发 (2026 年 1 月更新)

> **注意**：L2 的市场份额和风险评估处于快速变动中。在对 L2 进行排名、统计 TVL 或风险分类前，请参考最新数据（如 L2Beat）。

### L2 选择建议

| 网络 | 类型 | 最适合场景 | 核心优势 |
|----|------|----------|-------------|
| Base | Optimistic | 消费级应用、主流普及 | 与 Coinbase 深度集成，费用极低 |
| Arbitrum | Optimistic | DeFi 协议、成熟的生态 | TVL 最高、活跃的 DAO 资助 |
| Optimism | Optimistic | 公共物品、超级链 (Superchain) 生态 | 完善的 OP Stack 与资助计划 |
| zkSync Era | ZK-Rollup | 快速确认、原生支持 AA | zkEVM 兼容，提现无需等待 |
| Starknet | ZK-Rollup | Cairo 语言开发、原生 ZK 支持 | STARK 证明技术，定制化 VM |

### 企业级 Rollup 趋势 (2025-2026)

越来越多的大型机构基于 OP Stack 推出自己的 L2 网络：
- **Kraken INK** - 交易平台原生 L2。
- **Uniswap UniChain** - 针对 DeFi 深度优化。
- **Sony Soneium** - 专注于游戏与媒体内容。
- **Robinhood** - 集成 Arbitrum 网络。

### EIP-4844 (Blob 数据优化)

自 2024 年 3 月起，Rollup 开始使用基于 Blob 的数据发布方式：
- 之前：通过 `calldata` 发布 -> 成本极高。
- 之后：通过 `blob` 发布 -> 数据可用性 (DA) 成本大幅降低。

---

## 常见漏洞与错误 (2025-2026)

> **警示**：合约漏洞通常会造成惨重损失。权限控制、签名/托管逻辑以及集成环节的错误依然是事故频发的主要原因。

| 错误类型 | 潜在影响 | 预防措施 |
|--------|--------|------------|
| **权限控制缺失** | 未授权的管理员操作 | 使用 OpenZeppelin 的 `Ownable2Step` 或 `AccessControl` |
| **重入攻击 (Reentrancy)** | 资金被循环提取至空 | 严格执行 CEI 模式，使用 `ReentrancyGuard` |
| **未检查外部调用返回值** | 操作静默失败 | 始终检查 `call` 返回值，使用 `SafeERC20` 库 |
| **整数溢出 (0.8 以前版本)** | 数值被恶意操纵 | 升级至 Solidity 0.8.x+ (内置溢出检查) |
| **抢跑交易 (Front-running)** | MEV 被提取、三明治攻击 | 使用 Commit-reveal、Flashbots Protect 或私有内存池 |
| **预言机操纵** | 价格喂价遭受攻击 | 采用 TWAP (时间加权平均价)、多预言机校验、设置波动阈值 |
| **初始化不当** | 代理合约被非法接管 | 使用 `initializer` 修饰符，调用 `_disableInitializers()` |
| **存储冲突 (代理模式下)** | 合约数据损坏 | 遵循 EIP-1967 标准插槽，使用 OpenZeppelin Upgrades 插件 |

### 禁忌的开发模式

**严禁使用：**
- 使用 `tx.origin` 进行身份验证（存在钓鱼风险）。
- 在链上存储任何敏感私密信息（所有链上数据皆为公开可见）。
- 利用 `block.timestamp` 生成伪随机数（易受矿工/验证者操控）。
- 忽略 `transfer`/`send` 的执行返回值。
- 使用已停止维护的工具（如 Truffle, Ganache, Brownie）。

**最佳实践建议：**
- 每次代码变更后都运行静态分析（如 Slither 和 Aderyn）。
- 在任何审计启动前，必须完成模糊测试和不变量测试。
- 高价值 DeFi 项目必须采用形式化验证（如 Certora 和符号执行测试）。

---

### LLM 在智能合约开发中的局限性

**严禁完全依赖 LLM 进行：**
- 涉及到安全性关键逻辑的验证。
- 复杂的 Gas 消耗优化计算。
- 严密的数学逻辑证明。

**推荐利用 LLM 进行：**
- 样板代码生成（如测试脚本、基础文档）。
- 代码逻辑解释和审计前的初步梳理。
- 提出初始漏洞假设（但必须经过人工和工具验证）。

---

## 导航与参考

**核心参考资料**
- `references/blockchain-best-practices.md` - 通用区块链设计模式与安全性。
- `references/backend-integration-best-practices.md` - 后端加密集成模式 (.NET/C#, CQRS, Kafka)。
- `references/solidity-best-practices.md` - Solidity/EVM 特定开发指南。
- `references/rust-solana-best-practices.md` - Solana 与 Anchor 开发模式。
- `references/cosmwasm-best-practices.md` - Cosmos/CosmWasm 最佳实践。
- `references/ton-best-practices.md` - TON 合约 (Tact/FunC) 开发与部署。
- `references/defi-protocol-patterns.md` - 深度解析 DeFi 各类协议（AMM、借贷、预言机等）。
- `references/nft-token-standards.md` - NFT 相关标准与元数据处理。
- `references/cross-chain-bridges.md` - 跨链桥架构与安全性分析。
- `data/sources.json` - 精选的各链外部参考资源。

**代码模板**
- 以太坊/EVM: `assets/ethereum/template-solidity-hardhat.md`, `assets/ethereum/template-solidity-foundry.md`
- Solana: `assets/solana/template-rust-anchor.md`
- Cosmos: `assets/cosmos/template-cosmwasm.md`
- TON: `assets/ton/template-tact-blueprint.md`, `assets/ton/template-func-blueprint.md`
- 比特币: `assets/bitcoin/template-bitcoin-core.md`

---

## 趋势感知协议 (Trend Awareness Protocol)

**重要事项**：当涉及 Web3/加密货币的技术选型或趋势询问时，您必须在回答前先执行 `WebSearch` 以获取最新动态。

### 触发关键词
- “最适合 [用例] 的区块链是哪个？”
- “开发 [智能合约/DeFi/NFT] 推荐使用什么工具？”
- “Web3 开发目前的最新进展是什么？”
- “2026 年关于 [Solidity/审计/Gas 优化] 的最佳实践？”
- “[以太坊] vs [Solana] vs [其它网络] 选哪个？”

### 必须执行的搜索
1. `“2026年Web3开发最佳实践”`
2. `“[Ethereum/Solana/Base] 2026年开发动态更新”`
3. `“智能合约安全审计 2026”`
4. `“[Hardhat/Foundry] 2026年对比分析”`

### 结果汇报要求
搜索后，您的回复应包含：
- **当前现状**：目前主流的链、工具及框架。
- **新兴趋势**：正在获得关注的新协议或设计模式。
- **过时警示**：已失去热度或不再推荐的技术方案。
- **专家建议**：基于最新数据和生态活跃度给出的针对性建议。

---

## 操作手册
- `references/operational-playbook.md` - 包含智能合约架构、安全优先工作流以及各平台特定的操作模式。

## 事实核查要求
- 在给出最终答复前，务必验证当前的外部事实、版本号、定价、法规动态及平台行为。
- 优先选择一手信息源。
- 如果无法进行网络搜索，请在答复中明确说明局限性，并将指南标记为“未经验证”。
