# 以太坊智能合约开发 - Foundry 模板

通过 Foundry、Solidity 和本机 Solidity 测试进行现代、极快的以太坊开发。

---

## 项目概述

该模板提供了一个完整的开发环境，用于使用以下方式构建、测试和部署以太坊智能合约：

- **Foundry** - 快速智能合约开发框架（Forge、Cast、Anvil）
- **Forge** - 具有改进的模糊器和反例最小化的以太坊测试框架
- **演员** - 用于与 EVM 合约交互的瑞士军刀
- **Anvil** - 本地以太坊节点（即时挖矿、分叉）
- **Solidity** - 用 Solidity 编写测试（不需要 JavaScript）
- **OpenZeppelin** - 经过实战考验的合约库

**用例：** DeFi 协议、代币合约、NFT 项目、DAO、可升级系统

---

## 项目结构

```
foundry-project/
├── src/
│   ├── Token.sol
│   ├── NFT.sol
│   └── interfaces/
│       └── IToken.sol
├── test/
│   ├── Token.t.sol
│   ├── NFT.t.sol
│   └── mocks/
│       └── MockERC20.sol
├── script/
│   ├── Deploy.s.sol
│   └── Upgrade.s.sol
├── lib/
│   ├── forge-std/
│   └── openzeppelin-contracts/
├── foundry.toml
├── .env.example
└── README.md
```

---

## 环境设置

### 1.安装Foundry

```bash
# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Verify installation
forge --version
cast --version
anvil --version
```

### 2.初始化项目

```bash
# Create new project
forge init my-project
cd my-project

# Install OpenZeppelin
forge install OpenZeppelin/openzeppelin-contracts

# Install OpenZeppelin Upgradeable
forge install OpenZeppelin/openzeppelin-contracts-upgradeable

# Install Chainlink (for price feeds)
forge install smartcontractkit/chainlink-brownie-contracts
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
```

---

## 代工配置

**Foundry.toml：**
```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc_version = "0.8.20"
optimizer = true
optimizer_runs = 200
via_ir = false

# Etherscan verification
[etherscan]
sepolia = { key = "${ETHERSCAN_API_KEY}" }
mainnet = { key = "${ETHERSCAN_API_KEY}" }

# RPC endpoints
[rpc_endpoints]
sepolia = "${SEPOLIA_RPC_URL}"
mainnet = "${MAINNET_RPC_URL}"

# Testing configuration
[profile.default.fuzz]
runs = 256
max_test_rejects = 65536

[profile.default.invariant]
runs = 256
depth = 15
fail_on_revert = false

# CI profile (more thorough)
[profile.ci]
fuzz_runs = 10000
invariant_runs = 1000

# Gas reporting
[profile.default.gas_reports]
contracts = ["*"]
```

---

## 智能合约示例

### ERC20 代币

**src/Token.sol:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, Ownable {
    uint256 public constant MAX_SUPPLY = 1_000_000 * 10**18;

    constructor() ERC20("MyToken", "MTK") Ownable(msg.sender) {
        _mint(msg.sender, 1000 * 10**18);
    }

    function mint(address to, uint256 amount) public onlyOwner {
        require(totalSupply() + amount <= MAX_SUPPLY, "Exceeds max supply");
        _mint(to, amount);
    }

    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
    }
}
```

### ERC721 NFT

**src/NFT.sol:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721URIStorage, Ownable {
    uint256 private _tokenIdCounter;
    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant MINT_PRICE = 0.01 ether;

    constructor() ERC721("MyNFT", "MNFT") Ownable(msg.sender) {}

    function mint(string memory uri) public payable {
        require(_tokenIdCounter < MAX_SUPPLY, "Max supply reached");
        require(msg.value >= MINT_PRICE, "Insufficient payment");

        uint256 tokenId = _tokenIdCounter++;
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, uri);
    }

    function withdraw() public onlyOwner {
        (bool success, ) = owner().call{value: address(this).balance}("");
        require(success, "Transfer failed");
    }
}
```

---

## 使用 Forge 进行测试

### 基本测试结构

**测试/Token.t.sol：**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "forge-std/Test.sol";
import "../src/Token.sol";

contract TokenTest is Test {
    MyToken public token;
    address public owner = address(this);
    address public alice = address(0x1);
    address public bob = address(0x2);

    function setUp() public {
        token = new MyToken();

        // Give Alice and Bob some ETH
        vm.deal(alice, 100 ether);
        vm.deal(bob, 100 ether);
    }

    function testInitialSupply() public {
        assertEq(token.totalSupply(), 1000 * 10**18);
        assertEq(token.balanceOf(owner), 1000 * 10**18);
    }

    function testMint() public {
        uint256 amount = 100 * 10**18;
        token.mint(alice, amount);

        assertEq(token.balanceOf(alice), amount);
        assertEq(token.totalSupply(), 1100 * 10**18);
    }

    function testMintFailsWhenNotOwner() public {
        vm.prank(alice);
        vm.expectRevert(
            abi.encodeWithSelector(
                Ownable.OwnableUnauthorizedAccount.selector,
                alice
            )
        );
        token.mint(bob, 100 * 10**18);
    }

    function testMintFailsWhenExceedsMaxSupply() public {
        uint256 maxSupply = token.MAX_SUPPLY();
        uint256 toMint = maxSupply + 1;

        vm.expectRevert("Exceeds max supply");
        token.mint(alice, toMint);
    }

    function testBurn() public {
        uint256 amount = 100 * 10**18;
        token.burn(amount);

        assertEq(token.balanceOf(owner), 900 * 10**18);
        assertEq(token.totalSupply(), 900 * 10**18);
    }

    function testTransfer() public {
        uint256 amount = 50 * 10**18;
        token.transfer(alice, amount);

        assertEq(token.balanceOf(alice), amount);
        assertEq(token.balanceOf(owner), 950 * 10**18);

        vm.prank(alice);
        token.transfer(bob, 25 * 10**18);

        assertEq(token.balanceOf(bob), 25 * 10**18);
        assertEq(token.balanceOf(alice), 25 * 10**18);
    }
}
```

### 模糊测试

```solidity
contract TokenFuzzTest is Test {
    MyToken public token;

    function setUp() public {
        token = new MyToken();
    }

    /// @notice Fuzz test: mint amount should never exceed max supply
    function testFuzzMint(address to, uint256 amount) public {
        vm.assume(to != address(0));
        vm.assume(amount <= token.MAX_SUPPLY());

        uint256 currentSupply = token.totalSupply();

        if (currentSupply + amount <= token.MAX_SUPPLY()) {
            token.mint(to, amount);
            assertEq(token.balanceOf(to), amount);
        } else {
            vm.expectRevert("Exceeds max supply");
            token.mint(to, amount);
        }
    }

    /// @notice Fuzz test: transfers preserve total supply
    function testFuzzTransfer(address from, address to, uint256 amount) public {
        vm.assume(from != address(0));
        vm.assume(to != address(0));
        vm.assume(from != to);
        vm.assume(amount <= token.MAX_SUPPLY());

        // Setup: mint to 'from' address
        token.mint(from, amount);
        uint256 totalBefore = token.totalSupply();

        // Execute transfer
        vm.prank(from);
        token.transfer(to, amount);

        // Verify invariant: total supply unchanged
        assertEq(token.totalSupply(), totalBefore);
        assertEq(token.balanceOf(to), amount);
    }
}
```

### 不变测试

```solidity
contract TokenInvariantTest is Test {
    MyToken public token;
    TokenHandler public handler;

    function setUp() public {
        token = new MyToken();
        handler = new TokenHandler(token);

        // Set handler as target for invariant tests
        targetContract(address(handler));
    }

    /// @notice Invariant: Total supply never exceeds MAX_SUPPLY
    function invariant_totalSupplyNeverExceedsMax() public {
        assertLe(token.totalSupply(), token.MAX_SUPPLY());
    }

    /// @notice Invariant: Sum of all balances equals total supply
    function invariant_sumOfBalancesEqualsTotalSupply() public {
        uint256 sum = 0;
        address[] memory users = handler.getUsers();

        for (uint256 i = 0; i < users.length; i++) {
            sum += token.balanceOf(users[i]);
        }

        assertEq(sum, token.totalSupply());
    }
}

/// @notice Handler contract for invariant testing
contract TokenHandler {
    MyToken public token;
    address[] public users;

    constructor(MyToken _token) {
        token = _token;
    }

    function mint(uint256 seed, uint256 amount) public {
        address user = _getRandomUser(seed);
        amount = bound(amount, 0, token.MAX_SUPPLY());

        try token.mint(user, amount) {
            if (!_isKnownUser(user)) {
                users.push(user);
            }
        } catch {}
    }

    function transfer(uint256 fromSeed, uint256 toSeed, uint256 amount) public {
        if (users.length == 0) return;

        address from = users[fromSeed % users.length];
        address to = _getRandomUser(toSeed);
        amount = bound(amount, 0, token.balanceOf(from));

        vm.prank(from);
        try token.transfer(to, amount) {
            if (!_isKnownUser(to)) {
                users.push(to);
            }
        } catch {}
    }

    function getUsers() external view returns (address[] memory) {
        return users;
    }

    function _getRandomUser(uint256 seed) internal pure returns (address) {
        return address(uint160(seed));
    }

    function _isKnownUser(address user) internal view returns (bool) {
        for (uint256 i = 0; i < users.length; i++) {
            if (users[i] == user) return true;
        }
        return false;
    }
}
```

### 前叉测试

```solidity
contract ForkTest is Test {
    uint256 mainnetFork;
    IERC20 constant DAI = IERC20(0x6B175474E89094C44Da98b954EedeAC495271d0F);

    function setUp() public {
        // Fork mainnet at latest block
        mainnetFork = vm.createFork(vm.envString("MAINNET_RPC_URL"));
        vm.selectFork(mainnetFork);
    }

    function testForkDAI() public {
        assertEq(DAI.decimals(), 18);
        assertEq(DAI.name(), "Dai Stablecoin");
    }

    function testForkSwap() public {
        // Fork at specific block for deterministic testing
        vm.createSelectFork(vm.envString("MAINNET_RPC_URL"), 18_000_000);

        // Impersonate whale address
        address whale = 0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643;
        vm.prank(whale);

        // Test swap logic
        // ...
    }
}
```

---

## 部署脚本

### 基本部署

**脚本/Deploy.s.sol：**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "forge-std/Script.sol";
import "../src/Token.sol";
import "../src/NFT.sol";

contract DeployScript is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("DEPLOYER_PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);

        // Deploy Token
        MyToken token = new MyToken();
        console.log("Token deployed at:", address(token));

        // Deploy NFT
        MyNFT nft = new MyNFT();
        console.log("NFT deployed at:", address(nft));

        vm.stopBroadcast();
    }
}
```

**部署到网络：**
```bash
# Deploy to Sepolia
forge script script/Deploy.s.sol:DeployScript --rpc-url sepolia --broadcast --verify

# Deploy to Mainnet (with additional confirmations)
forge script script/Deploy.s.sol:DeployScript --rpc-url mainnet --broadcast --verify --slow
```

### 确定性部署 (CREATE2)

```solidity
contract DeterministicDeploy is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("DEPLOYER_PRIVATE_KEY");
        bytes32 salt = keccak256("MyToken_v1");

        vm.startBroadcast(deployerPrivateKey);

        // Predict address
        address predicted = vm.computeCreate2Address(
            salt,
            keccak256(type(MyToken).creationCode)
        );
        console.log("Predicted address:", predicted);

        // Deploy with CREATE2
        MyToken token = new MyToken{salt: salt}();
        console.log("Deployed at:", address(token));

        require(address(token) == predicted, "Address mismatch");

        vm.stopBroadcast();
    }
}
```

---

## 有用的命令

### 编译和测试

```bash
# Build contracts
forge build

# Run tests
forge test

# Run tests with verbosity
forge test -vvv

# Run specific test
forge test --match-test testMint

# Run tests in specific contract
forge test --match-contract TokenTest

# Gas report
forge test --gas-report

# Coverage report
forge coverage

# Coverage with LCOV output
forge coverage --report lcov
```

### 模糊测试和不变量

```bash
# Fuzz testing with custom runs
forge test --fuzz-runs 10000

# Invariant testing
forge test --match-test invariant

# Invariant testing with custom depth
forge test --match-test invariant --depth 50
```

### 部署和验证

```bash
# Deploy to Sepolia
forge script script/Deploy.s.sol --rpc-url sepolia --broadcast

# Deploy with verification
forge script script/Deploy.s.sol --rpc-url sepolia --broadcast --verify

# Verify existing contract
forge verify-contract <CONTRACT_ADDRESS> src/Token.sol:MyToken --chain sepolia

# Flatten contract (for manual verification)
forge flatten src/Token.sol
```

### 本地节点（Anvil）

```bash
# Start local node
anvil

# Fork mainnet locally
anvil --fork-url $MAINNET_RPC_URL

# Fork at specific block
anvil --fork-url $MAINNET_RPC_URL --fork-block-number 18000000
```

### 演员（互动）

```bash
# Get balance
cast balance <ADDRESS>

# Call view function
cast call <CONTRACT> "totalSupply()(uint256)"

# Send transaction
cast send <CONTRACT> "mint(address,uint256)" <ADDRESS> 1000000000000000000 --private-key <KEY>

# Get transaction receipt
cast receipt <TX_HASH>

# Estimate gas
cast estimate <CONTRACT> "mint(address,uint256)" <ADDRESS> 1000000000000000000

# Get storage slot
cast storage <CONTRACT> <SLOT>

# Convert to checksummed address
cast --to-checksum-address 0x...

# Convert wei to ether
cast --from-wei 1000000000000000000

# Compute keccak256
cast keccak "mint(address,uint256)"

# Decode calldata
cast 4byte-decode 0x40c10f19...
```

---

## 生产清单

在部署到主网之前：

**安全：**
- [ ] 所有测试均通过（`forge test`）
- [ ] 高测试覆盖率（`伪造覆盖率`）
- [ ] 关键功能的模糊测试（`forge test --fuzz-runs 10000`）
- [ ] 不变测试通过（`forge test --match-test invariant`）
- [ ] 无编译器警告（`forge build`）
- [ ] OpenZeppelin 标准功能合约
- [ ] Slither 分析干净（`slither .`）
- [ ] 专业审核完成
- [ ] 漏洞赏金计划已准备就绪

**配置：**
- [ ] Solidity 版本已锁定（无`^`）
- [ ] 通过适当的运行启用优化器（一般运行 200 次，库运行超过 1000 次）
- [ ] 记录所有环境变量
- [ ] 私钥安全（硬件钱包/MPC）

**部署：**
- [ ] 首先部署到测试网
- [ ] 多重签名钱包设置为所有者
- [ ] 关键功能的时间锁定
- [ ] 在 Etherscan 上验证（`伪造验证合约`）
- [ ] 配置监控和警报
- [ ] 紧急暂停机制已测试

**文件：**
- [ ] 自述文件及使用说明
- [ ] NatSpec 对所有公共功能的评论
- [ ] 架构图
- [ ] 记录已知限制

---

## 高级模式

### 气体快照

```bash
# Create gas snapshot
forge snapshot

# Compare gas changes
forge snapshot --diff .gas-snapshot
```

### 形式验证（Halmos）

```bash
# Install Halmos
pip install halmos

# Run symbolic tests
halmos --contract TokenTest --function testMint
```

### 部署到多个网络

```bash
# Deploy to all testnets
forge script script/Deploy.s.sol --rpc-url sepolia --broadcast
forge script script/Deploy.s.sol --rpc-url goerli --broadcast
forge script script/Deploy.s.sol --rpc-url mumbai --broadcast
```

---

＃＃ 资源

- [铸造书籍](https://book.getfoundry.sh/)
- [Forge 标准库](https://github.com/foundry-rs/forge-std)
- [OpenZeppelin 合约](https://docs.openzeppelin.com/contracts/)
- [Solidity 文档](https://docs.soliditylang.org/)
- [Foundry 示例](https://github.com/foundry-rs/foundry/tree/master/testdata)
- [Awesome Foundry](https://github.com/crisgarner/awesome-foundry)
