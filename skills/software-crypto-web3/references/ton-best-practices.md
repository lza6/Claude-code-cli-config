# TON 最佳实践 - FunC、Tact 和 TVM 开发

用于在开放网络 (TON) 上进行安全、高效的智能合约开发的生产级模式。

---

＃＃ 目录

1. [TON架构](#ton-architecture)
2. [TVM 特定模式](#tvm-specific-patterns)
3. [消息处理](#message-handling)
4. [Gas优化](#gas-optimization)
5. [Jetton（代币）标准](#jetton-token-standards)
6. [NFT 标准](#nft-standards)
7. [TON Connect 集成](#ton-connect-integration)
8. [安全模式](#security-patterns)
9. [测试策略](#testing-strategies)
10. [常见陷阱](#common-pitfalls)

---

## TON 架构

### 演员模型

TON 使用**异步参与者模型**，其中：
- 每个合约都是一个独立的参与者
- 通过消息进行沟通（无直接呼叫）
- 每个合约按顺序处理消息
- 没有重入攻击（与以太坊不同）

**与以太坊的主要区别：**

|特色|以太坊 |吨 |
|---------|----------|-----|
|执行 |同步|异步 |
|合约调用 |直接（CALL 操作码）|基于消息 |
|可重入 |可能 |不可能|
|状态变化 |交易内|跨消息|
|气体模型| EVM 气体 | TVM Gas（计算+存储）|

### 分片架构

TON 使用**无限分片**（分片链）：
- 工作链 0：主链（用于验证者）
- Workchain -1：Basechain（用于用户合约）
- 每个帐户可以位于不同的分片中
- 跨分片消息有延迟

**最佳实践：** 设计合约时假设消息传递不是即时的。

---

## TVM 特定模式

### 基于堆栈的操作

TVM 是一个基于堆栈的虚拟机（类似于 Bitcoin Script，但更强大）。

**FunC 堆栈操作：**
```func
;; Stack manipulation
int a = 10;
int b = 20;
int sum = a + b;  // Pushes a, b, adds, stores in sum

;; Tuple operations (multiple return values)
(int, int) swap(int a, int b) {
    return (b, a);
}

;; Inline functions (no stack overhead)
int add(int a, int b) inline {
    return a + b;
}
```

**最佳实践：** 对小型辅助函数使用“内联”以避免函数调用开销。

### 单元操作

TON 中的所有内容都存储在**单元格**中（最大 1023 位 + 4 个引用）。

```func
;; Build cell
cell data = begin_cell()
    .store_uint(123, 32)
    .store_slice(address)
    .store_ref(another_cell)
    .end_cell();

;; Parse cell
slice ds = data.begin_parse();
int value = ds~load_uint(32);
slice addr = ds~load_msg_addr();
cell ref = ds~load_ref();

;; [OK] GOOD: Check slice is fully consumed
ds.end_parse();  // Throws if extra data remains
```

**最佳实践：** 加载后始终调用 `end_parse()` 以确保没有额外数据。

### 切片安全

```func
;; VULNERABLE: No bounds checking
int load_uint_unsafe(slice s) {
    return s~load_uint(64);  // May fail if slice too short
}

;; SECURE: Check slice size first
int load_uint_safe(slice s) {
    throw_unless(100, s.slice_bits() >= 64);
    return s~load_uint(64);
}
```

---

## 消息处理

### 消息结构

每条消息都有：
- **标头：** 标志、源、目的地、值、反弹、已反弹
- **Body:**操作码(op) + query_id + data

**Standard Message Format:**
```func
int op = in_msg_body~load_uint(32);      ;; Operation code
int query_id = in_msg_body~load_uint(64); ;; Query ID (for tracking)
;; ... remaining data
```

### 消息模式

```func
;; Common send modes
const int SEND_MODE_REGULAR = 0;              ;; Pay fees separately
const int SEND_MODE_PAY_FEES_SEPARATELY = 1;  ;; Pay transfer fees separately
const int SEND_MODE_IGNORE_ERRORS = 2;        ;; Ignore send errors
const int SEND_MODE_CARRY_REMAINING_BALANCE = 64;  ;; Send all remaining balance
const int SEND_MODE_CARRY_ALL_BALANCE = 128;  ;; Send all balance and destroy

;; [OK] GOOD: Pay fees separately, ignore errors
send_raw_message(msg, 1 + 2);

;; [OK] GOOD: Return all remaining value to sender
send_raw_message(msg, 64);
```

**最佳实践：** 使用模式“64”（携带剩余余额）进行响应，以避免灰尘堆积。

### 弹跳处理

在以下情况下会发生退回邮件：
- 收件人不存在
- 接收者合约抛出错误
- 接收者气体不足

```func
() recv_internal(int balance, int msg_value, cell in_msg, slice in_msg_body) {
    slice cs = in_msg.begin_parse();
    int flags = cs~load_uint(4);

    ;; Check if bounced
    if (flags & 1) {
        ;; Handle bounced message
        ;; DO NOT throw here (creates bounce loop)
        return ();
    }

    ;; Normal message handling
    int op = in_msg_body~load_uint(32);
    ;; ...
}
```

**最佳实践：** 始终首先检查反弹标志并优雅地处理（不抛出）。

### 获取方法与内部消息

```func
;; BAD: Get method that modifies state
int get_and_increment() method_id {
    int counter = get_data().begin_parse().preload_uint(64);
    counter += 1;  // WRONG: Get methods can't modify state
    return counter;
}

;; [OK] GOOD: Get method is read-only
int get_counter() method_id {
    return get_data().begin_parse().preload_uint(64);
}

;; [OK] GOOD: State modification via internal message
() recv_internal(...) {
    if (op == op::increment()) {
        int counter = get_data().begin_parse().preload_uint(64);
        counter += 1;
        set_data(begin_cell().store_uint(counter, 64).end_cell());
    }
}
```

---

## 气体优化

### 气体成分

TON 气体有两部分：
1. **计算gas** - CPU操作
2. **存储费用** - 随着时间的推移数据存储

**仓储费计算公式：**
```
storage_fee = cells * cell_price + bits * bit_price
```

### 尽量减少细胞计数

```func
;; [FAIL] EXPENSIVE: Multiple cells
cell data = begin_cell()
    .store_ref(
        begin_cell()
            .store_uint(a, 32)
            .end_cell()
    )
    .store_ref(
        begin_cell()
            .store_uint(b, 32)
            .end_cell()
    )
    .end_cell();

;; [OK] OPTIMIZED: Single cell (if fits)
cell data = begin_cell()
    .store_uint(a, 32)
    .store_uint(b, 32)
    .end_cell();
```

**最佳实践：** 将数据打包到尽可能少的单元中（每个单元最多 1023 位）。

### 避免不必要的负载

```func
;; [FAIL] EXPENSIVE: Load data multiple times
() bad_example() {
    slice ds = get_data().begin_parse();
    int counter = ds~load_uint(64);
    ;; ... some logic ...
    ds = get_data().begin_parse();  // LOAD AGAIN
    int owner = ds~load_msg_addr();
}

;; [OK] OPTIMIZED: Load once
() good_example() {
    slice ds = get_data().begin_parse();
    int counter = ds~load_uint(64);
    slice owner = ds~load_msg_addr();
    ;; Use both values
}
```

### 使用内联函数

```func
;; [FAIL] EXPENSIVE: Regular function call
int add(int a, int b) {
    return a + b;
}

;; [OK] OPTIMIZED: Inline (no call overhead)
int add(int a, int b) inline {
    return a + b;
}

;; [OK] OPTIMIZED: Inline_ref (balance between code size and speed)
int complex_calculation(int a, int b) inline_ref {
    ;; Complex logic here
    return result;
}
```

**何时使用：**
- `inline` - 小函数（<10 次操作）
- `inline_ref` - 中等函数（10-50 次操作）
- 常规 - 大型函数或很少调用

---

## Jetton（代币）标准

### TEP-74：杰顿标准

**Jetton Minter（主合同）：**
```func
;; Required get methods
(int, int, slice, cell, cell) get_jetton_data() method_id {
    return (
        total_supply,      ;; Total supply
        -1,                ;; Mintable flag (-1 = true, 0 = false)
        admin_address,     ;; Admin address
        content,           ;; Metadata cell
        jetton_wallet_code ;; Wallet code
    );
}

slice get_wallet_address(slice owner_address) method_id {
    return calculate_user_jetton_wallet_address(
        owner_address,
        my_address(),
        jetton_wallet_code
    );
}
```

**Jetton 钱包（用户钱包）：**
```func
;; Required get methods
(int, slice, slice, cell) get_wallet_data() method_id {
    return (
        balance,           ;; Jetton balance
        owner,             ;; Owner address
        jetton_master,     ;; Minter address
        jetton_wallet_code ;; Wallet code
    );
}
```

### 链下元数据

**元数据格式 (TEP-64)：**
```json
{
  "name": "My Token",
  "description": "Description of token",
  "symbol": "MTK",
  "decimals": "9",
  "image": "https://example.com/logo.png",
  "image_data": "<base64_encoded_image>"
}
```

**链上参考：**
```func
;; Store IPFS link
cell content = begin_cell()
    .store_uint(0x01, 8)  ;; Off-chain content tag
    .store_slice("https://ipfs.io/ipfs/Qm..."^^)
    .end_cell();
```

---

## NFT 标准

### TEP-62：NFT 标准

**NFT 集合：**
```func
;; Required get methods
(int, cell, slice) get_collection_data() method_id {
    return (
        next_item_index,   ;; Next NFT index
        collection_content,;; Collection metadata
        owner_address      ;; Owner
    );
}

slice get_nft_address_by_index(int index) method_id {
    return calculate_nft_item_address(index);
}
```

**NFT 项目：**
```func
;; Required get methods
(int, int, slice, slice, cell) get_nft_data() method_id {
    return (
        init?,             ;; -1 if initialized, 0 otherwise
        index,             ;; NFT index
        collection_address,;; Collection address
        owner_address,     ;; Current owner
        individual_content ;; NFT-specific metadata
    );
}
```

### SBT（灵魂绑定代币）

**TEP-85：SBT 标准（不可转让的 NFT）：**
```func
;; Transfer blocked
() recv_internal(...) {
    if (op == op::transfer()) {
        throw(413);  ;; SBTs cannot be transferred
    }
    ;; ... other ops
}

;; Revoke method (only authority)
() recv_internal(...) {
    if (op == op::revoke()) {
        throw_unless(401, equal_slices(sender, authority));
        ;; Destroy SBT
        set_data(begin_cell().end_cell());
        return ();
    }
}
```

---

## TON Connect 集成

### DApp 身份验证流程

1. **生成二维码/深层链接：**
```typescript
import TonConnect from '@tonconnect/sdk';

const connector = new TonConnect({
    manifestUrl: 'https://myapp.com/tonconnect-manifest.json'
});

const walletConnectionSource = {
    universalLink: 'https://app.tonkeeper.com/ton-connect',
    bridgeUrl: 'https://bridge.tonapi.io/bridge'
};

const link = connector.connect(walletConnectionSource);
console.log('Connection link:', link);
```

2. **手柄连接：**
```typescript
connector.onStatusChange(wallet => {
    if (wallet) {
        console.log('Connected wallet:', wallet.account.address);
        console.log('Public key:', wallet.account.publicKey);
    }
});
```

3. **发送交易：**
```typescript
const transaction = {
    validUntil: Math.floor(Date.now() / 1000) + 60, // 60 sec
    messages: [
        {
            address: "EQ...",
            amount: "1000000000", // 1 TON in nanotons
            payload: "te6cckEBAQEA..." // base64 encoded cell
        }
    ]
};

const result = await connector.sendTransaction(transaction);
```

### 清单文件

**tonconnect-manifest.json：**
```json
{
  "url": "https://myapp.com",
  "name": "My DApp",
  "iconUrl": "https://myapp.com/icon.png",
  "termsOfUseUrl": "https://myapp.com/terms",
  "privacyPolicyUrl": "https://myapp.com/privacy"
}
```

---

## 安全模式

### 访问控制

```func
;; SECURE: Check sender is owner
() recv_internal(...) {
    slice sender_address = cs~load_msg_addr();

    if (op == op::admin_action()) {
        (slice owner) = load_data();
        throw_unless(401, equal_slices(sender_address, owner));
        ;; Perform admin action
    }
}
```

### 整数溢出保护

FunC 具有自动溢出检查（溢出时抛出）：

```func
;; [OK] SAFE: Automatically checks overflow
int result = a + b;  ;; Throws if overflows

;; For explicit control:
int safe_add(int a, int b) {
    int result = a + b;
    ;; Overflow check is automatic
    return result;
}
```

### 消息值验证

```func
;; SECURE: Ensure sufficient value sent
const int MIN_TON_FOR_STORAGE = 50000000;  ;; 0.05 TON

() recv_internal(int msg_value, ...) {
    throw_unless(
        402,
        msg_value >= MIN_TON_FOR_STORAGE
    );
    ;; Process message
}
```

### 防止重复重播

```func
;; Use query_id to prevent replays
cell processed_queries;  ;; Store processed query_ids

() recv_internal(...) {
    int query_id = in_msg_body~load_uint(64);

    ;; Check if already processed
    throw_if(403, is_processed(query_id));

    ;; Mark as processed
    mark_processed(query_id);

    ;; Process message
}
```

---

## 测试策略

### 蓝图测试 (TypeScript)

```typescript
import { Blockchain } from '@ton/sandbox';

describe('Counter', () => {
    let blockchain: Blockchain;
    let counter: SandboxContract<Counter>;

    beforeEach(async () => {
        blockchain = await Blockchain.create();
        counter = blockchain.openContract(...);
    });

    it('should handle insufficient value', async () => {
        const result = await counter.sendIncrement({
            value: toNano('0.001'), // Too small
        });

        expect(result.transactions).toHaveTransaction({
            success: false,
            exitCode: 402, // Insufficient value
        });
    });

    it('should handle bounce', async () => {
        // Send to non-existent contract
        const result = await counter.sendTo({
            to: Address.parse('EQBadAddress...'),
            value: toNano('1'),
        });

        expect(result.transactions).toHaveTransaction({
            from: recipient,
            to: counter.address,
            bounced: true,
        });
    });
});
```

### 气体分析

```typescript
it('should measure gas consumption', async () => {
    const result = await counter.sendIncrement({
        value: toNano('0.1'),
    });

    const tx = result.transactions[1]; // Internal transaction
    console.log('Gas used:', tx.gasUsed);
    console.log('Storage fees:', tx.storageFees);
});
```

---

## 常见陷阱

### 1. 忘记弹跳标志

```func
;; VULNERABLE: No bounce check
() recv_internal(...) {
    int op = in_msg_body~load_uint(32);
    ;; Process op without checking if bounced
}

;; SECURE: Always check bounce
() recv_internal(...) {
    int flags = cs~load_uint(4);
    if (flags & 1) {  ;; Bounced message
        return ();
    }
    int op = in_msg_body~load_uint(32);
}
```

### 2. 地址比较不正确

```func
;; [FAIL] WRONG: Direct equality (doesn't work)
if (addr1 == addr2) { ... }

;; [OK] CORRECT: Use equal_slices
if (equal_slices(addr1, addr2)) { ... }
```

### 3. 不处理空消息

```func
;; VULNERABLE: Assumes body exists
() recv_internal(...) {
    int op = in_msg_body~load_uint(32);  ;; May fail if empty
}

;; SECURE: Check for empty
() recv_internal(...) {
    if (in_msg_body.slice_empty?()) {
        return ();  ;; Ignore empty messages
    }
    int op = in_msg_body~load_uint(32);
}
```

### 4. 气体计算不正确

```func
;; [FAIL] WRONG: Sending all value (leaves nothing for gas)
send_raw_message(msg, 128);  ;; Sends all, contract may freeze

;; [OK] CORRECT: Leave balance for storage fees
send_raw_message(msg, 64);   ;; Send remaining, keep initial balance
```

### 5. 单细胞中的大数据

```func
;; [FAIL] WRONG: Too much data (>1023 bits)
cell data = begin_cell()
    .store_uint(value1, 256)
    .store_uint(value2, 256)
    .store_uint(value3, 256)
    .store_uint(value4, 256)  ;; 1024 bits - FAILS
    .end_cell();

;; [OK] CORRECT: Use references
cell data = begin_cell()
    .store_uint(value1, 256)
    .store_uint(value2, 256)
    .store_ref(
        begin_cell()
            .store_uint(value3, 256)
            .store_uint(value4, 256)
            .end_cell()
    )
    .end_cell();
```

---

## 生产清单

在部署到主网之前：

**安全：**
- [ ] 实施跳出处理
- [ ] 特权操作的访问控制
- [ ] 整数溢出处理（FunC 中自动）
- [ ] 消息值验证
- [ ] 查询 ID 跟踪以防止重放
- [ ]专业安全审核完成

**气体优化：**
- [ ] 数据打包到最小单元格中
- [ ] 用于帮助程序的内联函数
- [ ] 消除不必要的负载
- [ ] 按合同有效期计算的存储费

**符合标准：**
- [ ] 遵循 Jetton/NFT 标准（如果适用）
- [ ] 元数据格式正确 (TEP-64)
- [ ] 必需的 get 方法已实现
- [ ] 钱包地址计算符合标准

**测试：**
- [ ] 所有操作的单元测试
- [ ] 已测试跳出场景
- [ ] 测试的价值场景不足
- [ ] 测量气体消耗量
- [ ] 测试网部署已验证

**TON 连接：**
- [ ] 托管且可访问的清单文件
- [ ] 交易构建已测试
- [ ] 钱包兼容性已验证
- [ ] 实施错误处理

---

＃＃ 资源

- [TON 文档](https://docs.ton.org/)
- [FunC 文档](https://docs.ton.org/develop/func/overview)
- [Tact 文档](https://docs.tact-lang.org/)
- [TEP（TON 增强提案）](https://github.com/ton-blockchain/TEPs)
- [TON Connect](https://docs.ton.org/develop/dapps/ton-connect/overview)
- [蓝图框架](https://github.com/ton-org/blueprint)
- [TON 食谱](https://docs.ton.org/develop/smart-contracts/)
- [TON 社区](https://t.me/tondev_eng)
