# CosmWasm 智能合约开发模板

使用 CosmWasm 和 Rust 为 Cosmos 生态系统进行生产级智能合约开发。

---

## 项目概况

该模板提供了一个完整的开发环境，用于使用以下方式构建、测试和部署 CosmWasm 智能合约：

- **CosmWasm** - Cosmos 智能合约平台
- **Rust** - 系统编程语言
- **货物生成** - 项目脚手架
- **cw-multi-test** - 多合约测试
- **CosmJS** - Cosmos 的 JavaScript 库

**用例：** DeFi 协议、DAO、NFT 市场、治理系统、支持 IBC 的合约

---

## 项目结构

```
cosmwasm-contract/
├── src/
│   ├── contract.rs          # Entry points (instantiate, execute, query, migrate)
│   ├── state.rs             # State definitions and storage
│   ├── msg.rs               # Message types (Instantiate, Execute, Query)
│   ├── error.rs             # Custom error types
│   ├── helpers.rs           # Utility functions
│   └── lib.rs               # Library exports
├── examples/
│   └── schema.rs            # JSON schema generator
├── tests/
│   ├── integration.rs       # Integration tests with cw-multi-test
│   └── helpers/
│       └── mock.rs          # Mock contracts and helpers
├── schema/                  # Generated JSON schemas
│   ├── instantiate_msg.json
│   ├── execute_msg.json
│   ├── query_msg.json
│   └── state.json
├── Cargo.toml
├── .cargo/
│   └── config             # Cargo configuration
└── README.md
```

---

## 环境设置

### 1. 安装先决条件

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup default stable
rustup target add wasm32-unknown-unknown

# Install cargo-generate (for project templates)
cargo install cargo-generate --features vendored-openssl

# Install cargo-run-script (for custom scripts)
cargo install cargo-run-script
```

### 2.创建新项目

```bash
# Using CosmWasm template
cargo generate --git https://github.com/CosmWasm/cw-template.git --name my-contract
cd my-contract

# Or manually create project
cargo new --lib my-contract
cd my-contract
```

### 3.配置Cargo.toml

**货物.toml：**
```toml
[package]
name = "my-contract"
version = "0.1.0"
authors = ["Your Name <your.email@example.com>"]
edition = "2021"

[lib]
crate-type = ["cdylib", "rlib"]

[profile.release]
opt-level = 3
debug = false
rpath = false
lto = true
debug-assertions = false
codegen-units = 1
panic = 'abort'
incremental = false
overflow-checks = true

[features]
# Use library feature to disable all instantiate/execute/query exports
library = []

[dependencies]
cosmwasm-std = "1.5"
cosmwasm-storage = "1.5"
cw-storage-plus = "1.2"
cw2 = "1.1"
schemars = "0.8"
serde = { version = "1.0", default-features = false, features = ["derive"] }
thiserror = "1.0"

[dev-dependencies]
cw-multi-test = "0.20"
cosmwasm-schema = "1.5"
```

---

## 基本合约执行

### 入口点 (contract.rs)

```rust
use cosmwasm_std::{
    entry_point, to_binary, Binary, Deps, DepsMut, Env, MessageInfo,
    Response, StdResult,
};

use crate::error::ContractError;
use crate::msg::{ExecuteMsg, InstantiateMsg, QueryMsg, CountResponse};
use crate::state::{State, CONFIG};

// Version info for migration
const CONTRACT_NAME: &str = "crates.io:my-contract";
const CONTRACT_VERSION: &str = env!("CARGO_PKG_VERSION");

#[entry_point]
pub fn instantiate(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    msg: InstantiateMsg,
) -> Result<Response, ContractError> {
    // Set contract version for migration
    cw2::set_contract_version(deps.storage, CONTRACT_NAME, CONTRACT_VERSION)?;

    let state = State {
        count: msg.count,
        owner: info.sender.clone(),
    };

    CONFIG.save(deps.storage, &state)?;

    Ok(Response::new()
        .add_attribute("method", "instantiate")
        .add_attribute("owner", info.sender)
        .add_attribute("count", msg.count.to_string()))
}

#[entry_point]
pub fn execute(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    msg: ExecuteMsg,
) -> Result<Response, ContractError> {
    match msg {
        ExecuteMsg::Increment {} => execute_increment(deps),
        ExecuteMsg::Reset { count } => execute_reset(deps, info, count),
        ExecuteMsg::Transfer { recipient, amount } => {
            execute_transfer(deps, info, recipient, amount)
        }
    }
}

#[entry_point]
pub fn query(deps: Deps, _env: Env, msg: QueryMsg) -> StdResult<Binary> {
    match msg {
        QueryMsg::GetCount {} => to_binary(&query_count(deps)?),
        QueryMsg::GetOwner {} => to_binary(&query_owner(deps)?),
    }
}

#[entry_point]
pub fn migrate(deps: DepsMut, _env: Env, _msg: MigrateMsg) -> Result<Response, ContractError> {
    // Perform migration logic here
    let version = cw2::get_contract_version(deps.storage)?;
    if version.contract != CONTRACT_NAME {
        return Err(ContractError::InvalidContractName {
            name: version.contract,
        });
    }

    cw2::set_contract_version(deps.storage, CONTRACT_NAME, CONTRACT_VERSION)?;

    Ok(Response::new()
        .add_attribute("method", "migrate")
        .add_attribute("new_version", CONTRACT_VERSION))
}

// Execute handlers
pub fn execute_increment(deps: DepsMut) -> Result<Response, ContractError> {
    CONFIG.update(deps.storage, |mut state| -> Result<_, ContractError> {
        state.count += 1;
        Ok(state)
    })?;

    Ok(Response::new().add_attribute("action", "increment"))
}

pub fn execute_reset(
    deps: DepsMut,
    info: MessageInfo,
    count: i32,
) -> Result<Response, ContractError> {
    CONFIG.update(deps.storage, |mut state| -> Result<_, ContractError> {
        if info.sender != state.owner {
            return Err(ContractError::Unauthorized {});
        }
        state.count = count;
        Ok(state)
    })?;

    Ok(Response::new()
        .add_attribute("action", "reset")
        .add_attribute("count", count.to_string()))
}

// Query handlers
fn query_count(deps: Deps) -> StdResult<CountResponse> {
    let state = CONFIG.load(deps.storage)?;
    Ok(CountResponse { count: state.count })
}

fn query_owner(deps: Deps) -> StdResult<OwnerResponse> {
    let state = CONFIG.load(deps.storage)?;
    Ok(OwnerResponse {
        owner: state.owner.to_string(),
    })
}
```

### 消息类型 (msg.rs)

```rust
use cosmwasm_schema::{cw_serde, QueryResponses};
use cosmwasm_std::Uint128;

#[cw_serde]
pub struct InstantiateMsg {
    pub count: i32,
}

#[cw_serde]
pub enum ExecuteMsg {
    Increment {},
    Reset { count: i32 },
    Transfer { recipient: String, amount: Uint128 },
}

#[cw_serde]
#[derive(QueryResponses)]
pub enum QueryMsg {
    #[returns(CountResponse)]
    GetCount {},
    #[returns(OwnerResponse)]
    GetOwner {},
}

#[cw_serde]
pub struct CountResponse {
    pub count: i32,
}

#[cw_serde]
pub struct OwnerResponse {
    pub owner: String,
}

#[cw_serde]
pub struct MigrateMsg {}
```

### 状态管理（state.rs）

```rust
use cosmwasm_schema::cw_serde;
use cosmwasm_std::Addr;
use cw_storage_plus::Item;

#[cw_serde]
pub struct State {
    pub count: i32,
    pub owner: Addr,
}

pub const CONFIG: Item<State> = Item::new("config");
```

### 错误处理 (error.rs)

```rust
use cosmwasm_std::StdError;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ContractError {
    #[error("{0}")]
    Std(#[from] StdError),

    #[error("Unauthorized")]
    Unauthorized {},

    #[error("Invalid contract name: {name}")]
    InvalidContractName { name: String },

    #[error("Semver parsing error: {0}")]
    SemVer(String),
}

impl From<semver::Error> for ContractError {
    fn from(err: semver::Error) -> Self {
        Self::SemVer(err.to_string())
    }
}
```

---

## 测试

### 单元测试 (contract.rs)

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use cosmwasm_std::testing::{mock_dependencies, mock_env, mock_info};
    use cosmwasm_std::{coins, from_binary};

    #[test]
    fn proper_initialization() {
        let mut deps = mock_dependencies();

        let msg = InstantiateMsg { count: 17 };
        let info = mock_info("creator", &coins(1000, "earth"));

        let res = instantiate(deps.as_mut(), mock_env(), info, msg).unwrap();
        assert_eq!(0, res.messages.len());

        // Query count
        let res = query(deps.as_ref(), mock_env(), QueryMsg::GetCount {}).unwrap();
        let value: CountResponse = from_binary(&res).unwrap();
        assert_eq!(17, value.count);
    }

    #[test]
    fn increment() {
        let mut deps = mock_dependencies();

        let msg = InstantiateMsg { count: 17 };
        let info = mock_info("creator", &coins(2, "token"));
        let _res = instantiate(deps.as_mut(), mock_env(), info, msg).unwrap();

        // Increment
        let info = mock_info("anyone", &coins(2, "token"));
        let msg = ExecuteMsg::Increment {};
        let _res = execute(deps.as_mut(), mock_env(), info, msg).unwrap();

        // Verify
        let res = query(deps.as_ref(), mock_env(), QueryMsg::GetCount {}).unwrap();
        let value: CountResponse = from_binary(&res).unwrap();
        assert_eq!(18, value.count);
    }

    #[test]
    fn reset() {
        let mut deps = mock_dependencies();

        let msg = InstantiateMsg { count: 17 };
        let info = mock_info("creator", &coins(2, "token"));
        let _res = instantiate(deps.as_mut(), mock_env(), info, msg).unwrap();

        // Reset as owner
        let info = mock_info("creator", &coins(2, "token"));
        let msg = ExecuteMsg::Reset { count: 5 };
        let _res = execute(deps.as_mut(), mock_env(), info, msg).unwrap();

        // Verify
        let res = query(deps.as_ref(), mock_env(), QueryMsg::GetCount {}).unwrap();
        let value: CountResponse = from_binary(&res).unwrap();
        assert_eq!(5, value.count);
    }

    #[test]
    fn unauthorized_reset() {
        let mut deps = mock_dependencies();

        let msg = InstantiateMsg { count: 17 };
        let info = mock_info("creator", &coins(2, "token"));
        let _res = instantiate(deps.as_mut(), mock_env(), info, msg).unwrap();

        // Unauthorized reset
        let info = mock_info("anyone", &coins(2, "token"));
        let msg = ExecuteMsg::Reset { count: 5 };
        let res = execute(deps.as_mut(), mock_env(), info, msg);

        match res {
            Err(ContractError::Unauthorized {}) => {}
            _ => panic!("Must return unauthorized error"),
        }
    }
}
```

### 集成测试 (tests/integration.rs)

```rust
use cosmwasm_std::{Addr, Coin, Empty, Uint128};
use cw_multi_test::{App, AppBuilder, Contract, ContractWrapper, Executor};

use my_contract::msg::{CountResponse, ExecuteMsg, InstantiateMsg, QueryMsg};

pub fn contract_template() -> Box<dyn Contract<Empty>> {
    let contract = ContractWrapper::new(
        my_contract::contract::execute,
        my_contract::contract::instantiate,
        my_contract::contract::query,
    )
    .with_migrate(my_contract::contract::migrate);
    Box::new(contract)
}

const USER: &str = "user";
const ADMIN: &str = "admin";
const NATIVE_DENOM: &str = "denom";

fn mock_app() -> App {
    AppBuilder::new().build(|router, _, storage| {
        router
            .bank
            .init_balance(
                storage,
                &Addr::unchecked(USER),
                vec![Coin {
                    denom: NATIVE_DENOM.to_string(),
                    amount: Uint128::new(1000),
                }],
            )
            .unwrap();
    })
}

fn proper_instantiate() -> (App, Addr) {
    let mut app = mock_app();
    let code_id = app.store_code(contract_template());

    let msg = InstantiateMsg { count: 1 };
    let contract_addr = app
        .instantiate_contract(
            code_id,
            Addr::unchecked(ADMIN),
            &msg,
            &[],
            "test",
            None,
        )
        .unwrap();

    (app, contract_addr)
}

#[test]
fn count() {
    let (mut app, contract_addr) = proper_instantiate();

    let msg = ExecuteMsg::Increment {};
    let cosmos_msg = my_contract::msg::ExecuteMsg::Increment {};
    app.execute_contract(Addr::unchecked(USER), contract_addr.clone(), &cosmos_msg, &[])
        .unwrap();

    let res: CountResponse = app
        .wrap()
        .query_wasm_smart(contract_addr, &QueryMsg::GetCount {})
        .unwrap();

    assert_eq!(res.count, 2);
}

#[test]
fn reset() {
    let (mut app, contract_addr) = proper_instantiate();

    let msg = ExecuteMsg::Reset { count: 5 };
    app.execute_contract(Addr::unchecked(ADMIN), contract_addr.clone(), &msg, &[])
        .unwrap();

    let res: CountResponse = app
        .wrap()
        .query_wasm_smart(contract_addr, &QueryMsg::GetCount {})
        .unwrap();

    assert_eq!(res.count, 5);
}
```

---

## 构建和部署

### 构建合约

```bash
# Optimize for production
docker run --rm -v "$(pwd)":/code \
  --mount type=volume,source="$(basename "$(pwd)")_cache",target=/code/target \
  --mount type=volume,source=registry_cache,target=/usr/local/cargo/registry \
  cosmwasm/rust-optimizer:0.15.0

# This produces optimized wasm in ./artifacts/
```

### 部署到测试网

```bash
# Set up wasmd CLI
CHAIN_ID="uni-6"
TESTNET_NAME="uni-6"
RPC="https://rpc.uni.junomint.com:443"
TXFLAG="--chain-id ${CHAIN_ID} --gas-prices 0.025ujunox --gas auto --gas-adjustment 1.3"

# Store contract
RES=$(junod tx wasm store artifacts/my_contract.wasm --from wallet $TXFLAG -y --output json -b block)
CODE_ID=$(echo $RES | jq -r '.logs[0].events[-1].attributes[0].value')

echo "Code ID: $CODE_ID"

# Instantiate contract
INIT='{"count":100}'
junod tx wasm instantiate $CODE_ID "$INIT" \
    --from wallet --label "my contract" $TXFLAG -y --no-admin

# Get contract address
CONTRACT=$(junod query wasm list-contract-by-code $CODE_ID --output json | jq -r '.contracts[-1]')
echo "Contract address: $CONTRACT"

# Query contract
junod query wasm contract-state smart $CONTRACT '{"get_count":{}}'

# Execute contract
junod tx wasm execute $CONTRACT '{"increment":{}}' \
    --from wallet $TXFLAG -y
```

---

## CosmJS 客户端集成

### TypeScript 客户端

```typescript
import { SigningCosmWasmClient } from "@cosmjs/cosmwasm-stargate";
import { DirectSecp256k1HdWallet } from "@cosmjs/proto-signing";
import { GasPrice } from "@cosmjs/stargate";
import fs from "fs";

const RPC_ENDPOINT = "https://rpc.uni.junomint.com:443";
const MNEMONIC = "your mnemonic here"; // NEVER commit this

async function main() {
  // Create wallet from mnemonic
  const wallet = await DirectSecp256k1HdWallet.fromMnemonic(MNEMONIC, {
    prefix: "juno",
  });

  const [account] = await wallet.getAccounts();
  console.log("Wallet address:", account.address);

  // Connect to chain
  const client = await SigningCosmWasmClient.connectWithSigner(
    RPC_ENDPOINT,
    wallet,
    {
      gasPrice: GasPrice.fromString("0.025ujunox"),
    }
  );

  // Upload contract
  const wasmCode = fs.readFileSync("./artifacts/my_contract.wasm");
  const uploadResult = await client.upload(
    account.address,
    wasmCode,
    "auto"
  );
  console.log("Code ID:", uploadResult.codeId);

  // Instantiate contract
  const instantiateMsg = { count: 100 };
  const instantiateResult = await client.instantiate(
    account.address,
    uploadResult.codeId,
    instantiateMsg,
    "My Contract",
    "auto"
  );
  console.log("Contract address:", instantiateResult.contractAddress);

  // Query contract
  const queryResult = await client.queryContractSmart(
    instantiateResult.contractAddress,
    { get_count: {} }
  );
  console.log("Count:", queryResult.count);

  // Execute contract
  const executeMsg = { increment: {} };
  const executeResult = await client.execute(
    account.address,
    instantiateResult.contractAddress,
    executeMsg,
    "auto"
  );
  console.log("Transaction hash:", executeResult.transactionHash);
}

main().catch(console.error);
```

---

## 有用的命令

＃＃＃ 发展

```bash
# Build contract
cargo build

# Run tests
cargo test

# Run clippy
cargo clippy -- -D warnings

# Format code
cargo fmt

# Generate schema
cargo run --example schema

# Check wasm size
ls -lh target/wasm32-unknown-unknown/release/*.wasm
```

＃＃＃ 优化

```bash
# Using rust-optimizer (recommended)
docker run --rm -v "$(pwd)":/code \
  --mount type=volume,source="$(basename "$(pwd)")_cache",target=/code/target \
  --mount type=volume,source=registry_cache,target=/usr/local/cargo/registry \
  cosmwasm/rust-optimizer:0.15.0

# Using workspace-optimizer (for workspaces)
docker run --rm -v "$(pwd)":/code \
  --mount type=volume,source="$(basename "$(pwd)")_cache",target=/code/target \
  --mount type=volume,source=registry_cache,target=/usr/local/cargo/registry \
  cosmwasm/workspace-optimizer:0.15.0
```

---

## 生产清单

在部署到主网之前：

**安全：**
- [ ] 所有地址均通过 `addr_validate()` 进行验证
- [ ] 检查算术（Uint128/Decimal）
- [ ] 所有失败案例的自定义错误
- [ ] 特权功能的访问控制
- [ ] 查询函数中没有状态变化
- [ ] 迁移功能得到保障
- [ ]专业安全审核完成

**测试：**
- [ ] 100% 单元测试覆盖率
- [ ] 与 CW-multi-test 的集成测试
- [ ] 负面测试用例
- [ ] 迁移测试
- [ ] 气体基准记录

**部署：**
- [ ] 使用 Rust-optimizer 优化合约
- [ ] 生成并记录模式
- [ ] 管理/迁移权限得到保障
- [ ] 在测试网上测试部署
- [ ] 合约在链浏览器上验证

**文件：**
- [ ] 自述文件及使用说明
- [ ] API 文档
- [ ] 架构图
- [ ] 记录已知限制

---

＃＃ 资源

- [CosmWasm 文档](https://docs.cosmwasm.com/)
- [CosmWasm 书](https://book.cosmwasm.com/)
- [CosmWasm Plus](https://github.com/CosmWasm/cw-plus)
- [CosmWasm 模板](https://github.com/CosmWasm/cw-template)
- [CosmJS Documentation](https://cosmos.github.io/cosmjs/)
- [Cosmos SDK](https://docs.cosmos.network/)
- [朱诺网络](https://docs.junonetwork.io/)
