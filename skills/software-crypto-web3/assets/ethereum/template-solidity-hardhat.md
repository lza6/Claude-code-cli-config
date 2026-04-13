# 以太坊智能合约开发 - Hardhat 模板

使用 Hardhat、OpenZeppelin 和 Ethers.js 进行生产级以太坊智能合约开发。

---

## 项目概述

该模板提供了一个完整的开发环境，用于使用以下方式构建、测试和部署以太坊智能合约：

- **Hardhat** - 以太坊开发环境（测试、部署、插件）
- **Solidity 0.8.x** - 智能合约语言（在工具链中固定一个确切的版本）
- **OpenZeppelin** - 经过实战考验的合约库
- **Ethers.js** - JavaScript 的以太坊库
- **TypeScript** - 类型安全开发
- **Chai** - 测试框架

**用例：** DeFi 协议、NFT 集合、DAO、代币合约、可升级系统

---

## 项目结构

```
hardhat-project/
├── contracts/
│   ├── Token.sol
│   ├── NFT.sol
│   └── interfaces/
│       └── IToken.sol
├── test/
│   ├── Token.test.ts
│   └── NFT.test.ts
├── scripts/
│   ├── deploy.ts
│   └── verify.ts
├── hardhat.config.ts
├── package.json
├── tsconfig.json
├── .env.example
└── README.md
```

---

## 环境设置

### 1.初始化项目

```bash
mkdir my-hardhat-project && cd my-hardhat-project
npm init -y
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
npx hardhat init
```

选择：“创建 TypeScript 项目”

### 2.安装依赖项

```bash
npm install --save-dev \
  @openzeppelin/contracts \
  @openzeppelin/contracts-upgradeable \
  @nomicfoundation/hardhat-verify \
  hardhat-gas-reporter \
  solidity-coverage \
  dotenv
```

### 3.配置环境

**.env.示例：**
```bash
# Network RPC URLs
MAINNET_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY

# Private Keys (NEVER commit .env)
DEPLOYER_PRIVATE_KEY=0x...

# Etherscan API Key
ETHERSCAN_API_KEY=YOUR_ETHERSCAN_API_KEY

# Coinmarketcap API Key (for gas reporter)
COINMARKETCAP_API_KEY=YOUR_CMC_API_KEY
```

---

## 安全帽配置

**hardhat.config.ts：**
```typescript
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import "@nomicfoundation/hardhat-verify";
import "hardhat-gas-reporter";
import "solidity-coverage";
import * as dotenv from "dotenv";

dotenv.config();

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {
      chainId: 31337,
    },
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL || "",
      accounts: process.env.DEPLOYER_PRIVATE_KEY
        ? [process.env.DEPLOYER_PRIVATE_KEY]
        : [],
      chainId: 11155111,
    },
    mainnet: {
      url: process.env.MAINNET_RPC_URL || "",
      accounts: process.env.DEPLOYER_PRIVATE_KEY
        ? [process.env.DEPLOYER_PRIVATE_KEY]
        : [],
      chainId: 1,
    },
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY,
  },
  gasReporter: {
    enabled: process.env.REPORT_GAS === "true",
    currency: "USD",
    coinmarketcap: process.env.COINMARKETCAP_API_KEY,
  },
};

export default config;
```

---

## 智能合约示例

### ERC20 代币

**合约/Token.sol：**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, Ownable {
    uint256 public constant MAX_SUPPLY = 1_000_000 * 10**18;

    constructor() ERC20("MyToken", "MTK") Ownable(msg.sender) {
        _mint(msg.sender, 1000 * 10**18); // Initial supply
    }

    function mint(address to, uint256 amount) public onlyOwner {
        require(totalSupply() + amount <= MAX_SUPPLY, "Exceeds max supply");
        _mint(to, amount);
    }
}
```

### ERC721 NFT

**合约/NFT.sol：**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721URIStorage, Ownable {
    uint256 private _tokenIdCounter;
    uint256 public constant MAX_SUPPLY = 10000;

    constructor() ERC721("MyNFT", "MNFT") Ownable(msg.sender) {}

    function mint(address to, string memory uri) public onlyOwner {
        require(_tokenIdCounter < MAX_SUPPLY, "Max supply reached");
        uint256 tokenId = _tokenIdCounter++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }
}
```

---

## 测试

**测试/Token.test.ts：**
```typescript
import { expect } from "chai";
import { ethers } from "hardhat";
import { MyToken } from "../typechain-types";
import { SignerWithAddress } from "@nomicfoundation/hardhat-ethers/signers";

describe("MyToken", function () {
  let token: MyToken;
  let owner: SignerWithAddress;
  let addr1: SignerWithAddress;
  let addr2: SignerWithAddress;

  beforeEach(async function () {
    [owner, addr1, addr2] = await ethers.getSigners();

    const Token = await ethers.getContractFactory("MyToken");
    token = await Token.deploy();
    await token.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await token.owner()).to.equal(owner.address);
    });

    it("Should assign initial supply to owner", async function () {
      const ownerBalance = await token.balanceOf(owner.address);
      expect(ownerBalance).to.equal(ethers.parseEther("1000"));
    });
  });

  describe("Minting", function () {
    it("Should mint tokens to address", async function () {
      await token.mint(addr1.address, ethers.parseEther("100"));
      expect(await token.balanceOf(addr1.address)).to.equal(
        ethers.parseEther("100")
      );
    });

    it("Should fail if non-owner tries to mint", async function () {
      await expect(
        token.connect(addr1).mint(addr2.address, ethers.parseEther("100"))
      ).to.be.revertedWithCustomError(token, "OwnableUnauthorizedAccount");
    });

    it("Should not exceed max supply", async function () {
      const maxSupply = await token.MAX_SUPPLY();
      const toMint = maxSupply + ethers.parseEther("1");

      await expect(
        token.mint(addr1.address, toMint)
      ).to.be.revertedWith("Exceeds max supply");
    });
  });

  describe("Transfers", function () {
    it("Should transfer tokens between accounts", async function () {
      await token.transfer(addr1.address, ethers.parseEther("50"));
      expect(await token.balanceOf(addr1.address)).to.equal(
        ethers.parseEther("50")
      );

      await token.connect(addr1).transfer(addr2.address, ethers.parseEther("25"));
      expect(await token.balanceOf(addr2.address)).to.equal(
        ethers.parseEther("25")
      );
    });
  });
});
```

**运行测试：**
```bash
npx hardhat test
npx hardhat test --grep "Minting"  # Run specific suite
REPORT_GAS=true npx hardhat test  # With gas reporting
npx hardhat coverage               # Coverage report
```

---

## 部署脚本

**脚本/deploy.ts：**
```typescript
import { ethers } from "hardhat";

async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying contracts with account:", deployer.address);
  console.log("Account balance:", (await ethers.provider.getBalance(deployer.address)).toString());

  // Deploy Token
  const Token = await ethers.getContractFactory("MyToken");
  const token = await Token.deploy();
  await token.waitForDeployment();

  const tokenAddress = await token.getAddress();
  console.log("Token deployed to:", tokenAddress);

  // Deploy NFT
  const NFT = await ethers.getContractFactory("MyNFT");
  const nft = await NFT.deploy();
  await nft.waitForDeployment();

  const nftAddress = await nft.getAddress();
  console.log("NFT deployed to:", nftAddress);

  // Save deployment info
  const deploymentInfo = {
    network: (await ethers.provider.getNetwork()).name,
    token: tokenAddress,
    nft: nftAddress,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
  };

  console.log("\nDeployment Info:", JSON.stringify(deploymentInfo, null, 2));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

**部署到网络：**
```bash
npx hardhat run scripts/deploy.ts --network sepolia
npx hardhat run scripts/deploy.ts --network mainnet
```

---

＃＃ 确认

**脚本/verify.ts：**
```typescript
import { run } from "hardhat";

async function main() {
  const TOKEN_ADDRESS = "0x...";  // Your deployed address

  console.log("Verifying contract...");

  try {
    await run("verify:verify", {
      address: TOKEN_ADDRESS,
      constructorArguments: [],
    });
    console.log("Contract verified successfully");
  } catch (error: any) {
    if (error.message.includes("Already Verified")) {
      console.log("Contract already verified");
    } else {
      console.error("Verification failed:", error);
    }
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

**核实：**
```bash
npx hardhat verify --network sepolia 0xYOUR_CONTRACT_ADDRESS
```

---

## 在本地 Fork 上测试

**测试/Fork.test.ts：**
```typescript
import { expect } from "chai";
import { ethers } from "hardhat";

describe("Fork Tests", function () {
  beforeEach(async function () {
    // Fork mainnet
    await ethers.provider.send("hardhat_reset", [
      {
        forking: {
          jsonRpcUrl: process.env.MAINNET_RPC_URL,
          blockNumber: 18000000, // Optional: pin to specific block
        },
      },
    ]);
  });

  it("Should interact with mainnet DAI", async function () {
    const DAI_ADDRESS = "0x6B175474E89094C44Da98b954EedeAC495271d0F";
    const dai = await ethers.getContractAt("IERC20", DAI_ADDRESS);

    expect(await dai.decimals()).to.equal(18);
  });
});
```

---

## 生产清单

在部署到主网之前：

**安全：**
- [ ] 所有测试均通过（100% 覆盖率）
- [ ] 无编译器警告
- [ ] OpenZeppelin 标准功能合约
- [ ] 正确实施访问控制
- [ ] 需要时可重入防护
- [ ] 专业审核完成
- [ ] 漏洞赏金计划已准备就绪

**配置：**
- [ ] Solidity 版本已锁定（无`^`）
- [ ] 通过适当的运行启用优化器
- [ ] 记录所有环境变量
- [ ] 私钥安全（硬件钱包/MPC）

**部署：**
- [ ] 首先部署到测试网
- [ ] 多重签名钱包设置为所有者
- [ ] 关键功能的时间锁定
- [ ] 在 Etherscan 上验证
- [ ] 配置监控和警报
- [ ] 紧急暂停机制已测试

**文件：**
- [ ] 自述文件及使用说明
- [ ] NatSpec 对所有公共功能的评论
- [ ] 架构图
- [ ] 记录已知限制

---

## 有用的命令

```bash
# Compile contracts
npx hardhat compile

# Run tests
npx hardhat test
REPORT_GAS=true npx hardhat test

# Test coverage
npx hardhat coverage

# Local node
npx hardhat node

# Console
npx hardhat console --network sepolia

# Clean build artifacts
npx hardhat clean

# Check contract size
npx hardhat size-contracts
```

---

＃＃ 资源

- [安全帽文档](https://hardhat.org/docs)
- [OpenZeppelin 合约](https://docs.openzeppelin.com/contracts/)
- [Ethers.js 文档](https://docs.ethers.org/)
- [Solidity 文档](https://docs.soliditylang.org/)
- [安全帽网络](https://hardhat.org/hardhat-network/)
