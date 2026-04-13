# NFT 与令牌 (Token) 标准实施指南

本指南涵盖了同质化代币 (ERC-20)、非同质化代币 (ERC-721, ERC-1155) 以及 Solana 令牌标准 (SPL Token, Metaplex) 的生产级实施模式。包括实现细节、元数据架构、安全性考量及常见漏洞防范。

---

## 目录

1. [ERC-20：同质化代币](#erc-20-同质化代币)
2. [ERC-721：非同质化代币 (NFT)](#erc-721-非同质化代币)
3. [ERC-1155：多代币标准](#erc-1155-多代币标准)
4. [SPL Token (Solana)](#spl-token-solana)
5. [Metaplex (Solana NFT)](#metaplex-solana-nfts)
6. [令牌门控 (Token Gating) 模式](#令牌门控模式)
7. [元数据：链上与链下对比](#元数据链上与链下对比)
8. [常见令牌漏洞](#常见令牌漏洞)
9. [决策框架](#决策框架)

---

## ERC-20：同质化代币

### 标准实施建议

```solidity
// 生产环境建议使用 OpenZeppelin 库
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";
import "@openzeppelin/contracts/access/Ownable2Step.sol";

contract MyToken is ERC20, ERC20Permit, Ownable2Step {
    uint256 public constant MAX_SUPPLY = 1_000_000_000e18; // 总量 10 亿

    constructor()
        ERC20("My Token", "MTK")
        ERC20Permit("My Token")
        Ownable(msg.sender)
    {
        _mint(msg.sender, MAX_SUPPLY);
    }
}
```

### 授权 (Approve) 模式

```solidity
// 危险：标准 approve 函数存在已知的竞态条件漏洞
// 如果将授权额度从 100 改为 50，攻击者可以：
// 1. 在新授权生效前抢先用掉 100 额度
// 2. 在新授权生效后再用掉 50 额度

// 安全做法：使用增加/减少津贴的函数
token.increaseAllowance(spender, amount);
token.decreaseAllowance(spender, amount);

// 最佳做法：使用 ERC-2612 Permit (免 Gas 授权)
// 用户在链下签名消息，支出者提交签名完成 permit + transfer
function permitAndTransfer(
    address owner,
    uint256 amount,
    uint256 deadline,
    uint8 v, bytes32 r, bytes32 s
) external {
    token.permit(owner, address(this), amount, deadline, v, r, s);
    token.transferFrom(owner, address(this), amount);
}
```

### SafeERC20 的必要性

```solidity
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract TokenHandler {
    using SafeERC20 for IERC20;

    // 错误做法：部分代币 (如 USDT) 在失败时不返回 bool，且转账逻辑不标准
    // token.transfer(to, amount);  // 可能会静默失败

    // 正确做法：使用 SafeERC20 处理非标准代币
    function safeTransfer(IERC20 token, address to, uint256 amount) external {
        token.safeTransfer(to, amount);  // 失败时会自动回滚 (revert)
    }
}
```

---

## ERC-721：非同质化代币 (NFT)

### 标准实施

```solidity
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/common/ERC2981.sol";

contract MyNFT is ERC721, ERC721URIStorage, ERC2981 {
    // 核心逻辑：铸造、版税设置、URI 存储
    // 建议通过 _safeMint 确保接收者能正确处理 NFT
}
```

### 元数据标准格式 (JSON)

```json
{
  "name": "作品名称 #1",
  "description": "作品描述内容",
  "image": "ipfs://哈希值/1.png",
  "attributes": [
    { "trait_type": "背景", "value": "蓝色" },
    { "trait_type": "稀有度", "value": "史诗" }
  ]
}
```

---

## ERC-1155：多代币标准

### 选型场景

| 特性 | ERC-721 | ERC-1155 |
|---------|---------|----------|
| 代币类型 | 每个合约仅一种 NFT | 一个合约内支持同质化 + 非同质化代币 |
| 批量操作 | 不原生支持 | 支持原生的批量转账/铸造 |
| Gas 效率 | 每次转账成本较高 | 批量操作时 Gas 效率极高 |
| 适用场景 | PFP 收藏、艺术品 | 游戏道具、会员资格、门票 |

---

## SPL Token (Solana)

Solana 上的令牌管理模型：
- **Wallet Address** -> **Associated Token Account (ATA)** -> **Token Balance**
- 不同于 EVM（一个合约内管理所有余额），Solana 为每种代币维护独立的账户。
- ATA 是根据 (钱包地址, 代币 Mint 地址) 计算出的确定性地址。

---

## 令牌门控 (Token Gating) 模式

用于根据用户持有的令牌/NFT 授予特定访问权限。
- **链上校验**：在合约逻辑中使用 `balanceOf` 或 `ownerOf` 进行硬核限制。
- **链下校验**：后端通过 API 验证钱包签名及链上持有量，常用于 Discord 身份组授权、私密内容访问。

---

## 元数据存储：链上与链下对比

| 存储方式 | 成本 | 持久性 | 访问速度 | 适用场景 |
|--------|------|------------|--------|----------|
| **链上 (合约存储)** | 极高 | 永久 | 瞬时 | 小型核心数据（特征、分值） |
| **IPFS / Arweave** | 低/中 | 强依赖固定服务 | 中等 | 图像、视频、详细 JSON |
| **中心化存储 (S3/CDN)** | 低 | 取决于服务商 | 极快 | 经常变动的元数据、动态游戏道具 |

---

## 常见令牌漏洞

1. **铸造重入 (Reentrancy on Mint)**：`_safeMint` 会回调接收者的 `onERC721Received`，若状态未在回调前更新，会导致超额铸造。
2. **无限铸造漏洞**：缺少 `MAX_SUPPLY` 上限或对 `mint` 函数的访问控制不当。
3. **元数据篡改**：中心化存储的元数据在售罄后被修改。**防御：** 使用 IPFS 或锁定元数据修改权限。
4. **授权钓鱼 (Approval Phishing)**：诱导用户调用 `setApprovalForAll` 或大额授权。**防御：** UI 提示明确、集成 `Permit2` 进行限额授权。

---

## 决策框架：该使用哪种标准？

- **同质化、可分割？**
    - EVM -> **ERC-20**
    - Solana -> **SPL Token**
- **独一无二、非同质化？**
    - 普通收藏品 -> **ERC-721** (EVM) 或 **Metaplex** (Solana)
    - 大规模分发 (数百万量级) -> **Compressed NFTs** (Solana) 或 **ERC-721A**
- **包含多种分类、且有数量概念？**
    - 游戏道具、门票 -> **ERC-1155**
- **跨链需求？**
    - 现有资产桥接 -> **LayerZero OFT** (同质化) 或 **ONFT** (非同质化)
