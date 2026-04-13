# Bitcoin Development — Bitcoin Core & Lightning Network Template

使用比特币核心、闪电网络和脚本进行生产级比特币开发。

---

## 项目概述

该模板为比特币开发提供了指导，使用：

- **比特币核心** - 比特币的参考实现
- **比特币脚本** - 基于堆栈的脚本语言
- **闪电网络** - 第 2 层支付通道
- **BDK（比特币开发套件）** - 用于钱包开发的 Rust 库
- **Electrum/Electrs** - SPV 钱包服务器
- **BTCPay 服务器** - 自托管支付处理器

**用例：** 钱包、支付处理器、闪电应用程序、多重签名、时间锁合约、DLC

---

## 项目结构

```
bitcoin-project/
├── bitcoin-core/
│   ├── bitcoin.conf         # Node configuration
│   └── scripts/
│       ├── multisig.sh      # Multisig wallet scripts
│       └── timelock.sh      # Timelock scripts
├── wallet/
│   ├── src/
│   │   ├── main.rs          # BDK wallet implementation
│   │   ├── descriptors.rs   # Output descriptors
│   │   └── psbt.rs          # PSBT handling
│   └── Cargo.toml
├── lightning/
│   ├── lnd.conf             # LND configuration
│   └── node/
│       ├── channels.ts      # Channel management
│       └── invoices.ts      # Invoice handling
└── scripts/
    ├── deploy-node.sh       # Node deployment
    └── backup.sh            # Backup scripts
```

---

## 环境设置

### 1.安装比特币核心

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install bitcoind bitcoin-cli

# macOS (Homebrew)
brew install bitcoin

# Or download from bitcoin.org
wget https://bitcoincore.org/bin/bitcoin-core-25.0/bitcoin-25.0-x86_64-linux-gnu.tar.gz
tar -xzf bitcoin-25.0-x86_64-linux-gnu.tar.gz
sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-25.0/bin/*
```

### 2.配置比特币核心

**~/.bitcoin/bitcoin.conf:**
```conf
# Network
testnet=1              # Use testnet (remove for mainnet)
# signet=1             # Or use signet for testing

# RPC
server=1
rpcuser=your_username
rpcpassword=your_secure_password
rpcallowip=127.0.0.1
rpcport=18332          # 8332 for mainnet

# Indexing (optional, needed for some features)
txindex=1              # Index all transactions
addressindex=1         # Index addresses
timestampindex=1       # Index timestamps
spentindex=1           # Index spent outputs

# Mempool
maxmempool=300         # MB
mempoolexpiry=72       # hours

# Pruning (for space-constrained nodes)
# prune=550            # Keep only 550MB of blocks
```

### 3.启动比特币节点

```bash
# Start daemon
bitcoind -daemon

# Check status
bitcoin-cli getblockchaininfo

# Stop daemon
bitcoin-cli stop
```

---

## 比特币脚本

### 基本脚本

**支付到公钥哈希（P2PKH）：**
```
OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
```

**支付脚本哈希（P2SH）：**
```
OP_HASH160 <scriptHash> OP_EQUAL
```

**支付见证公钥哈希（P2WPKH - SegWit）：**
```
OP_0 <pubKeyHash>
```

**支付给 Taproot (P2TR):**
```
OP_1 <taproot_output_key>
```

### 多重签名脚本（3 中的 2）

```bash
#!/bin/bash
# Create 2-of-3 multisig address

# Generate 3 addresses
ADDR1=$(bitcoin-cli getnewaddress)
ADDR2=$(bitcoin-cli getnewaddress)
ADDR3=$(bitcoin-cli getnewaddress)

# Get public keys
PUBKEY1=$(bitcoin-cli getaddressinfo $ADDR1 | jq -r '.pubkey')
PUBKEY2=$(bitcoin-cli getaddressinfo $ADDR2 | jq -r '.pubkey')
PUBKEY3=$(bitcoin-cli getaddressinfo $ADDR3 | jq -r '.pubkey')

# Create multisig address
bitcoin-cli createmultisig 2 "[\"$PUBKEY1\",\"$PUBKEY2\",\"$PUBKEY3\"]"
```

**输出：**
```json
{
  "address": "2N...",
  "redeemScript": "5221...53ae",
  "descriptor": "wsh(multi(2,[...],...))#..."
}
```

### 时间锁定脚本（CSV - CheckSequenceVerify）

```
# Script: Coins can be spent after 144 blocks (~24 hours)
<144> OP_CHECKSEQUENCEVERIFY OP_DROP
<pubKey> OP_CHECKSIG
```

**创建时间锁交易：**
```bash
# Create raw transaction with sequence number
bitcoin-cli createrawtransaction \
  '[{"txid":"<txid>","vout":0,"sequence":144}]' \
  '{"<recipient_address>":0.01}'

# Sign and broadcast
bitcoin-cli signrawtransactionwithwallet <raw_tx>
bitcoin-cli sendrawtransaction <signed_tx>
```

---

## 使用 BDK 进行钱包开发

### Rust 钱包实现

**货物.toml：**
```toml
[dependencies]
bdk = { version = "0.29", features = ["electrum"] }
bitcoin = "0.30"
```

**src/main.rs:**
```rust
use bdk::{
    bitcoin::{Address, Network},
    blockchain::ElectrumBlockchain,
    database::MemoryDatabase,
    electrum_client::Client,
    wallet::AddressIndex,
    KeychainKind, SyncOptions, Wallet,
};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Create wallet with descriptor
    let external_descriptor = "wpkh([c258d2e4/84h/1h/0h]tpubD...)";
    let internal_descriptor = "wpkh([c258d2e4/84h/1h/0h]tpubD...)";

    let wallet = Wallet::new(
        external_descriptor,
        Some(internal_descriptor),
        Network::Testnet,
        MemoryDatabase::default(),
    )?;

    // Connect to Electrum server
    let client = Client::new("ssl://electrum.blockstream.info:60002")?;
    let blockchain = ElectrumBlockchain::from(client);

    // Sync wallet
    wallet.sync(&blockchain, SyncOptions::default())?;

    // Get balance
    let balance = wallet.get_balance()?;
    println!("Balance: {} sats", balance);

    // Get new address
    let address = wallet.get_address(AddressIndex::New)?;
    println!("New address: {}", address);

    // Create transaction
    let mut tx_builder = wallet.build_tx();
    tx_builder
        .add_recipient(Address::from_str("tb1...")?.script_pubkey(), 50_000)
        .fee_rate(bdk::FeeRate::from_sat_per_vb(1.0));

    let (mut psbt, _) = tx_builder.finish()?;

    // Sign transaction
    let finalized = wallet.sign(&mut psbt, Default::default())?;
    println!("Transaction signed: {}", finalized);

    // Extract and broadcast
    if finalized {
        let tx = psbt.extract_tx();
        blockchain.broadcast(&tx)?;
        println!("Transaction broadcast: {}", tx.txid());
    }

    Ok(())
}
```

---

## 闪电网络集成

### LND 设置

**安装LND：**
```bash
# Download LND
wget https://github.com/lightningnetwork/lnd/releases/download/v0.17.0/lnd-linux-amd64-v0.17.0.tar.gz
tar -xzf lnd-linux-amd64-v0.17.0.tar.gz
sudo install -m 0755 -o root -g root -t /usr/local/bin lnd-linux-amd64-v0.17.0/*
```

**lnd.conf：**
```conf
[Application Options]
debuglevel=info
alias=MyLightningNode
color=#3399FF

[Bitcoin]
bitcoin.active=1
bitcoin.testnet=1
bitcoin.node=bitcoind

[Bitcoind]
bitcoind.rpcuser=your_username
bitcoind.rpcpass=your_password
bitcoind.zmqpubrawblock=tcp://127.0.0.1:28332
bitcoind.zmqpubrawtx=tcp://127.0.0.1:28333
```

**启动 LND：**
```bash
lnd
```

### 渠道管理

```bash
# Create wallet
lncli create

# Get node info
lncli getinfo

# Connect to peer
lncli connect 03..@host:port

# Open channel (1,000,000 sats)
lncli openchannel --node_key=03... --local_amt=1000000

# List channels
lncli listchannels

# Close channel
lncli closechannel <funding_txid> <output_index>
```

### 发票和付款

```bash
# Create invoice (10,000 sats)
lncli addinvoice --amt=10000 --memo="Coffee"

# Decode invoice
lncli decodepayreq <payment_request>

# Pay invoice
lncli payinvoice <payment_request>

# List invoices
lncli listinvoices

# List payments
lncli listpayments
```

### LND gRPC 客户端（TypeScript）

```typescript
import * as fs from 'fs';
import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';

const lndCert = fs.readFileSync('/path/to/tls.cert');
const macaroon = fs.readFileSync('/path/to/admin.macaroon').toString('hex');

const packageDefinition = protoLoader.loadSync('lightning.proto');
const lnrpc = grpc.loadPackageDefinition(packageDefinition).lnrpc;

const credentials = grpc.credentials.createSsl(lndCert);
const macaroonCreds = grpc.credentials.createFromMetadataGenerator((args, callback) => {
    const metadata = new grpc.Metadata();
    metadata.add('macaroon', macaroon);
    callback(null, metadata);
});

const combinedCreds = grpc.credentials.combineChannelCredentials(
    credentials,
    macaroonCreds
);

const lightning = new lnrpc.Lightning('localhost:10009', combinedCreds);

// Get node info
lightning.getInfo({}, (err, response) => {
    if (err) console.error(err);
    else console.log('Node info:', response);
});

// Create invoice
lightning.addInvoice({ value: 10000, memo: 'Coffee' }, (err, response) => {
    if (err) console.error(err);
    else console.log('Invoice:', response.payment_request);
});

// Pay invoice
lightning.sendPaymentSync({
    payment_request: 'lnbc...'
}, (err, response) => {
    if (err) console.error(err);
    else console.log('Payment sent:', response);
});
```

---

## PSBT（部分签名的比特币交易）

### 创建并签署 PSBT

```bash
# Create PSBT
bitcoin-cli walletcreatefundedpsbt \
  '[]' \
  '[{"<address>":0.01}]' \
  | jq -r '.psbt' > unsigned.psbt

# Sign PSBT (wallet 1)
bitcoin-cli -rpcwallet=wallet1 walletprocesspsbt $(cat unsigned.psbt) \
  | jq -r '.psbt' > partially_signed.psbt

# Sign PSBT (wallet 2)
bitcoin-cli -rpcwallet=wallet2 walletprocesspsbt $(cat partially_signed.psbt) \
  | jq -r '.psbt' > fully_signed.psbt

# Finalize and broadcast
bitcoin-cli finalizepsbt $(cat fully_signed.psbt) \
  | jq -r '.hex' | xargs bitcoin-cli sendrawtransaction
```

---

## 输出描述符

### 描述符类型

```
# Single key P2WPKH
wpkh(xpub.../0/*)

# Multisig P2WSH (2-of-3)
wsh(multi(2,xpub1.../0/*,xpub2.../0/*,xpub3.../0/*))

# Nested SegWit (P2SH-P2WPKH)
sh(wpkh(xpub.../0/*))

# Taproot
tr(xpub.../0/*)

# With checksum
wpkh([fingerprint/derivation]xpub...)#checksum
```

### 导入描述符

```bash
# Import watch-only descriptor
bitcoin-cli importdescriptors '[{
  "desc": "wpkh([c258d2e4/84h/1h/0h]tpubD...)#checksum",
  "timestamp": "now",
  "range": [0, 1000],
  "watchonly": true
}]'
```

---

## 有用的命令

### 节点操作

```bash
# Get blockchain info
bitcoin-cli getblockchaininfo

# Get mempool info
bitcoin-cli getmempoolinfo

# Get network info
bitcoin-cli getnetworkinfo

# Get peer info
bitcoin-cli getpeerinfo

# Add node
bitcoin-cli addnode "<ip>:port" "add"

# Generate blocks (regtest only)
bitcoin-cli -regtest generatetoaddress 101 <address>
```

### 钱包操作

```bash
# Create wallet
bitcoin-cli createwallet "my_wallet"

# Load wallet
bitcoin-cli loadwallet "my_wallet"

# Get new address
bitcoin-cli getnewaddress "" "bech32"

# Get balance
bitcoin-cli getbalance

# Send transaction
bitcoin-cli sendtoaddress <address> 0.01

# List transactions
bitcoin-cli listtransactions

# List unspent outputs
bitcoin-cli listunspent

# Dump private key
bitcoin-cli dumpprivkey <address>

# Import private key
bitcoin-cli importprivkey <privkey>
```

### 交易操作

```bash
# Get raw transaction
bitcoin-cli getrawtransaction <txid> true

# Decode raw transaction
bitcoin-cli decoderawtransaction <hex>

# Test mempool accept
bitcoin-cli testmempoolaccept '["<hex>"]'

# Get transaction out
bitcoin-cli gettxout <txid> <vout>
```

---

## 使用 Regtest 进行测试

```bash
# Start regtest node
bitcoind -regtest -daemon

# Create wallet
bitcoin-cli -regtest createwallet "test"

# Get new address
ADDR=$(bitcoin-cli -regtest getnewaddress)

# Mine 101 blocks (coinbase maturity)
bitcoin-cli -regtest generatetoaddress 101 $ADDR

# Check balance
bitcoin-cli -regtest getbalance

# Send transaction
bitcoin-cli -regtest sendtoaddress <recipient> 1.0

# Mine block to confirm
bitcoin-cli -regtest generatetoaddress 1 $ADDR
```

---

## 生产清单

在生产环境中运行之前：

**安全：**
- [ ] 使用强 RPC 密码
- [ ] 已配置防火墙（仅允许 localhost 进行 RPC）
- [ ] 定期备份wallet.dat
- [ ] 加密钱包（`bitcoin-cli encryptwallet`）
- [ ] 监控安全更新

**性能：**
- [ ] 足够的磁盘空间（全节点 500GB+）
- [ ] 推荐 8GB+ 内存
- [ ] 链态首选 SSD
- [ ] 监控同步状态

**可靠性：**
- [ ] 自动备份
- [ ] 监控和警报
- [ ] 已配置冗余对等点
- [ ] 定期软件更新

**闪电（如果适用）：**
- [ ] 通道自动备份
- [ ] 了望塔已配置
- [ ] 充足的流入流动性
- [ ] 适当设定收费政策

---

＃＃ 资源

- [比特币核心文档](https://bitcoin.org/en/bitcoin-core/)
- [比特币开发者指南](https://developer.bitcoin.org/)
- [BDK 文档](https://bitcoindevkit.org/)
- [闪电网络规范](https://github.com/lightning/bolts)
- [LND 文档](https://docs.lightning.engineering/)
- [掌握比特币](https://github.com/bitcoinbook/bitcoinbook)
- [比特币脚本](https://en.bitcoin.it/wiki/Script)
- [BIPs（比特币改进提案）](https://github.com/bitcoin/bips)
