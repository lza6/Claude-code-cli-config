# TON 智能合约开发 — FunC + 蓝图模板

使用 FunC 语言和 Blueprint 框架进行生产级 TON 智能合约开发。

---

## 项目概述

该模板提供了一个完整的开发环境，用于使用以下方式构建、测试和部署 TON 区块链智能合约：

- **FunC** - TON 的智能合约语言（类似于 C）
- **蓝图** - TON 的现代开发框架
- **TypeScript** - 测试和部署脚本
- **TON SDK** - TON 的 JavaScript/TypeScript 库
- **沙箱** - 用于测试的本地区块链

**用例：** Jettons（代币）、NFT、DeFi 协议、钱包、DAO、游戏

---

## 项目结构

```
ton-contract/
├── contracts/
│   ├── main.fc              # Main contract code
│   ├── imports/
│   │   ├── stdlib.fc        # Standard library
│   │   └── utils.fc         # Utility functions
│   └── jetton.fc            # Jetton (token) example
├── wrappers/
│   ├── MainContract.ts      # TypeScript wrapper
│   └── JettonMinter.ts      # Jetton wrapper
├── tests/
│   ├── MainContract.spec.ts # Contract tests
│   └── JettonMinter.spec.ts # Token tests
├── scripts/
│   ├── deploy.ts            # Deployment script
│   └── interact.ts          # Interaction script
├── build/
│   └── main.compiled.json   # Compiled contract
├── blueprint.config.ts
├── tsconfig.json
└── package.json
```

---

## 环境设置

### 1. 安装先决条件

```bash
# Install Node.js (v18+)
# Install npm or yarn

# Create new Blueprint project
npm create ton@latest

# Or manually:
npm init
npm install --save-dev @ton/blueprint @ton/core @ton/crypto @ton/ton @ton/test-utils
npm install --save-dev @types/node typescript ts-node
```

### 2.初始化蓝图项目

```bash
# Create new contract
npx blueprint create Counter

# This creates:
# - contracts/counter.fc
# - wrappers/Counter.ts
# - tests/Counter.spec.ts
```

### 3.配置蓝图

**蓝图.config.ts：**
```typescript
import { Config } from '@ton/blueprint';

export const config: Config = {
    network: {
        endpoint: 'https://testnet.toncenter.com/api/v2/jsonRPC',
        apiKey: process.env.TONCENTER_API_KEY,
    },
};
```

---

## 基本柜台合约（FunC）

### 合约代码 (contracts/counter.fc)

```func
;; Counter contract - stores and manages a counter value

#include "imports/stdlib.fc";

;; Storage layout:
;; counter: uint64
;; owner: MsgAddressInt

(int, slice) load_data() inline {
    slice ds = get_data().begin_parse();
    return (
        ds~load_uint(64),    ;; counter
        ds~load_msg_addr()   ;; owner
    );
}

() save_data(int counter, slice owner) impure inline {
    set_data(begin_cell()
        .store_uint(counter, 64)
        .store_slice(owner)
        .end_cell());
}

;; recv_internal is the main entry point for internal messages
() recv_internal(int my_balance, int msg_value, cell in_msg_full, slice in_msg_body) impure {
    if (in_msg_body.slice_empty?()) { ;; Ignore empty messages
        return ();
    }

    slice cs = in_msg_full.begin_parse();
    int flags = cs~load_uint(4);

    if (flags & 1) { ;; Bounced messages
        return ();
    }

    slice sender_address = cs~load_msg_addr();

    int op = in_msg_body~load_uint(32);
    int query_id = in_msg_body~load_uint(64);

    (int counter, slice owner) = load_data();

    if (op == 1) { ;; Increment
        counter += 1;
        save_data(counter, owner);
        return ();
    }

    if (op == 2) { ;; Reset (owner only)
        throw_unless(401, equal_slices(sender_address, owner));
        int new_counter = in_msg_body~load_uint(64);
        save_data(new_counter, owner);
        return ();
    }

    if (op == 3) { ;; Get counter (query)
        ;; Send response with counter value
        cell msg = begin_cell()
            .store_uint(0x18, 6)
            .store_slice(sender_address)
            .store_coins(0)
            .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)
            .store_uint(op, 32)
            .store_uint(query_id, 64)
            .store_uint(counter, 64)
            .end_cell();
        send_raw_message(msg, 64); ;; Send all remaining balance
        return ();
    }

    throw(0xffff); ;; Unknown operation
}

;; Get methods (for off-chain queries)
int get_counter() method_id {
    (int counter, _) = load_data();
    return counter;
}

slice get_owner() method_id {
    (_, slice owner) = load_data();
    return owner;
}
```

---

## Jetton（代币）合约示例

### Jetton Minter (contracts/jetton-minter.fc)

```func
#include "imports/stdlib.fc";
#include "imports/params.fc";
#include "imports/jetton-utils.fc";

;; Storage:
;; total_supply: Coins
;; admin_address: MsgAddressInt
;; content: Cell (metadata)
;; jetton_wallet_code: Cell

(int, slice, cell, cell) load_data() inline {
    slice ds = get_data().begin_parse();
    return (
        ds~load_coins(),     ;; total_supply
        ds~load_msg_addr(),  ;; admin_address
        ds~load_ref(),       ;; content
        ds~load_ref()        ;; jetton_wallet_code
    );
}

() save_data(int total_supply, slice admin_address, cell content, cell jetton_wallet_code) impure inline {
    set_data(begin_cell()
        .store_coins(total_supply)
        .store_slice(admin_address)
        .store_ref(content)
        .store_ref(jetton_wallet_code)
        .end_cell());
}

() mint_tokens(slice to_address, cell jetton_wallet_code, int amount, cell master_msg) impure {
    cell state_init = calculate_jetton_wallet_state_init(to_address, my_address(), jetton_wallet_code);
    slice to_wallet_address = calculate_address_by_state_init(state_init);

    cell msg = begin_cell()
        .store_uint(0x18, 6)
        .store_slice(to_wallet_address)
        .store_coins(amount)
        .store_uint(4 + 2 + 1, 1 + 4 + 4 + 64 + 32 + 1 + 1 + 1)
        .store_ref(state_init)
        .store_ref(master_msg)
        .end_cell();

    send_raw_message(msg, 1); ;; Pay transfer fees separately
}

() recv_internal(int my_balance, int msg_value, cell in_msg_full, slice in_msg_body) impure {
    if (in_msg_body.slice_empty?()) {
        return ();
    }

    slice cs = in_msg_full.begin_parse();
    int flags = cs~load_uint(4);
    if (flags & 1) {
        return ();
    }

    slice sender_address = cs~load_msg_addr();

    int op = in_msg_body~load_uint(32);
    int query_id = in_msg_body~load_uint(64);

    (int total_supply, slice admin_address, cell content, cell jetton_wallet_code) = load_data();

    if (op == op::mint()) { ;; Mint tokens
        throw_unless(73, equal_slices(sender_address, admin_address));

        slice to_address = in_msg_body~load_msg_addr();
        int amount = in_msg_body~load_coins();
        cell master_msg = in_msg_body~load_ref();

        mint_tokens(to_address, jetton_wallet_code, amount, master_msg);

        save_data(total_supply + amount, admin_address, content, jetton_wallet_code);
        return ();
    }

    if (op == op::burn_notification()) { ;; Burn notification from wallet
        int jetton_amount = in_msg_body~load_coins();
        slice from_address = in_msg_body~load_msg_addr();

        ;; Verify sender is a valid jetton wallet
        cell state_init = calculate_jetton_wallet_state_init(from_address, my_address(), jetton_wallet_code);
        slice expected_wallet = calculate_address_by_state_init(state_init);
        throw_unless(74, equal_slices(sender_address, expected_wallet));

        save_data(total_supply - jetton_amount, admin_address, content, jetton_wallet_code);
        return ();
    }

    if (op == op::change_admin()) { ;; Change admin
        throw_unless(73, equal_slices(sender_address, admin_address));
        slice new_admin_address = in_msg_body~load_msg_addr();
        save_data(total_supply, new_admin_address, content, jetton_wallet_code);
        return ();
    }

    throw(0xffff);
}

;; Get methods
(int, int, slice, cell, cell) get_jetton_data() method_id {
    (int total_supply, slice admin_address, cell content, cell jetton_wallet_code) = load_data();
    return (total_supply, -1, admin_address, content, jetton_wallet_code);
}

slice get_wallet_address(slice owner_address) method_id {
    (_, _, _, cell jetton_wallet_code) = load_data();
    return calculate_user_jetton_wallet_address(owner_address, my_address(), jetton_wallet_code);
}
```

---

## TypeScript 包装器

### 计数器包装器 (wrappers/Counter.ts)

```typescript
import { Address, beginCell, Cell, Contract, contractAddress, ContractProvider, Sender, SendMode } from '@ton/core';

export type CounterConfig = {
    counter: number;
    owner: Address;
};

export function counterConfigToCell(config: CounterConfig): Cell {
    return beginCell()
        .storeUint(config.counter, 64)
        .storeAddress(config.owner)
        .endCell();
}

export class Counter implements Contract {
    constructor(
        readonly address: Address,
        readonly init?: { code: Cell; data: Cell }
    ) {}

    static createFromAddress(address: Address) {
        return new Counter(address);
    }

    static createFromConfig(config: CounterConfig, code: Cell, workchain = 0) {
        const data = counterConfigToCell(config);
        const init = { code, data };
        return new Counter(contractAddress(workchain, init), init);
    }

    async sendDeploy(provider: ContractProvider, via: Sender, value: bigint) {
        await provider.internal(via, {
            value,
            sendMode: SendMode.PAY_GAS_SEPARATELY,
            body: beginCell().endCell(),
        });
    }

    async sendIncrement(
        provider: ContractProvider,
        via: Sender,
        opts: {
            value: bigint;
            queryID?: number;
        }
    ) {
        await provider.internal(via, {
            value: opts.value,
            sendMode: SendMode.PAY_GAS_SEPARATELY,
            body: beginCell()
                .storeUint(1, 32) // op
                .storeUint(opts.queryID ?? 0, 64)
                .endCell(),
        });
    }

    async sendReset(
        provider: ContractProvider,
        via: Sender,
        opts: {
            value: bigint;
            newCounter: number;
            queryID?: number;
        }
    ) {
        await provider.internal(via, {
            value: opts.value,
            sendMode: SendMode.PAY_GAS_SEPARATELY,
            body: beginCell()
                .storeUint(2, 32) // op
                .storeUint(opts.queryID ?? 0, 64)
                .storeUint(opts.newCounter, 64)
                .endCell(),
        });
    }

    async getCounter(provider: ContractProvider): Promise<number> {
        const result = await provider.get('get_counter', []);
        return result.stack.readNumber();
    }

    async getOwner(provider: ContractProvider): Promise<Address> {
        const result = await provider.get('get_owner', []);
        return result.stack.readAddress();
    }
}
```

---

## 测试

### 测试文件 (tests/Counter.spec.ts)

```typescript
import { Blockchain, SandboxContract, TreasuryContract } from '@ton/sandbox';
import { Cell, toNano } from '@ton/core';
import { Counter } from '../wrappers/Counter';
import '@ton/test-utils';
import { compile } from '@ton/blueprint';

describe('Counter', () => {
    let code: Cell;

    beforeAll(async () => {
        code = await compile('Counter');
    });

    let blockchain: Blockchain;
    let deployer: SandboxContract<TreasuryContract>;
    let counter: SandboxContract<Counter>;

    beforeEach(async () => {
        blockchain = await Blockchain.create();

        deployer = await blockchain.treasury('deployer');

        counter = blockchain.openContract(
            Counter.createFromConfig(
                {
                    counter: 0,
                    owner: deployer.address,
                },
                code
            )
        );

        const deployResult = await counter.sendDeploy(deployer.getSender(), toNano('0.05'));

        expect(deployResult.transactions).toHaveTransaction({
            from: deployer.address,
            to: counter.address,
            deploy: true,
            success: true,
        });
    });

    it('should deploy', async () => {
        // Already checked in beforeEach
    });

    it('should increment counter', async () => {
        const counterBefore = await counter.getCounter();
        expect(counterBefore).toBe(0);

        await counter.sendIncrement(deployer.getSender(), {
            value: toNano('0.05'),
        });

        const counterAfter = await counter.getCounter();
        expect(counterAfter).toBe(1);
    });

    it('should reset counter (owner)', async () => {
        await counter.sendIncrement(deployer.getSender(), { value: toNano('0.05') });
        await counter.sendIncrement(deployer.getSender(), { value: toNano('0.05') });

        expect(await counter.getCounter()).toBe(2);

        await counter.sendReset(deployer.getSender(), {
            value: toNano('0.05'),
            newCounter: 10,
        });

        expect(await counter.getCounter()).toBe(10);
    });

    it('should reject reset from non-owner', async () => {
        const notOwner = await blockchain.treasury('notOwner');

        const result = await counter.sendReset(notOwner.getSender(), {
            value: toNano('0.05'),
            newCounter: 100,
        });

        expect(result.transactions).toHaveTransaction({
            from: notOwner.address,
            to: counter.address,
            success: false,
            exitCode: 401, // Unauthorized
        });
    });
});
```

---

## 部署

### 部署脚本 (scripts/deploy.ts)

```typescript
import { toNano } from '@ton/core';
import { Counter } from '../wrappers/Counter';
import { compile, NetworkProvider } from '@ton/blueprint';

export async function run(provider: NetworkProvider) {
    const counter = provider.open(
        Counter.createFromConfig(
            {
                counter: 0,
                owner: provider.sender().address!,
            },
            await compile('Counter')
        )
    );

    await counter.sendDeploy(provider.sender(), toNano('0.05'));

    await provider.waitForDeploy(counter.address);

    console.log('Counter deployed at:', counter.address);
    console.log('Initial counter:', await counter.getCounter());
}
```

**运行部署：**
```bash
# Deploy to testnet
npx blueprint run

# Deploy to mainnet
npx blueprint run --mainnet

# Deploy to custom network
npx blueprint run --custom https://your-node.com/api
```

---

## 有用的命令

＃＃＃ 发展

```bash
# Compile contracts
npx blueprint build

# Run tests
npx blueprint test

# Run specific test
npx blueprint test Counter

# Watch mode
npx blueprint test --watch

# Deploy
npx blueprint run

# Interact with deployed contract
npx blueprint run interact
```

### TON CLI

```bash
# Install TON CLI
npm install -g ton

# Get account info
ton account <address>

# Send transaction
ton send <from> <to> <amount>

# Get transaction
ton gettx <address> <lt>
```

---

## 生产清单

在部署到主网之前：

**安全：**
- [ ] 所有操作都有适当的授权检查
- [ ] 实施退回消息处理
- [ ] 考虑气体限制
- [ ] 整数溢出保护
- [ ]专业安全审核完成

**测试：**
- [ ] 100% 测试覆盖率
- [ ] 负面测试用例
- [ ] 测量气体消耗量
- [ ] 在测试网上测试

**部署：**
- [ ] 合约优化编译
- [ ] 初始状态配置正确
- [ ] 在测试网上测试部署
- [ ] 所有者/管理员密钥受到保护
- [ ] 监控设置

**文件：**
- [ ] 自述文件及使用说明
- [ ] API 文档
- [ ] 记录已知限制

---

＃＃ 资源

- [TON 文档](https://docs.ton.org/)
- [FunC 文档](https://docs.ton.org/develop/func/overview)
- [蓝图文档](https://github.com/ton-org/blueprint)
- [TON SDK](https://github.com/ton-org/ton)
- [TON 沙盒](https://github.com/ton-org/sandbox)
- [Jetton 标准](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md)
- [NFT 标准](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)
- [TON Connect](https://docs.ton.org/develop/dapps/ton-connect/overview)
