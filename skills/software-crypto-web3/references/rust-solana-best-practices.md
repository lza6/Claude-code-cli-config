# Rust + Solana 最佳实践 - Anchor 框架

使用 Anchor 框架进行安全、高效的 Solana 程序 (Program) 开发的生产级模式。

---

## 目录

1. [Anchor 框架设计模式](#anchor-框架设计模式)
2. [账户安全 (Account Security)](#账户安全)
3. [程序派生地址 (PDA)](#程序派生地址-pda)
4. [跨程序调用 (CPI)](#跨程序调用-cpi)
5. [SPL Token 集成](#spl-token-集成)
6. [错误处理](#错误处理)
7. [测试策略](#测试策略)
8. [性能优化 (计算单元 CU)](#性能优化-计算单元-cu)
9. [常见陷阱防范](#常见陷阱防范)

---

## Anchor 框架设计模式

### 基础程序结构

```rust
use anchor_lang::prelude::*;

declare_id!("此处为您的程序 ID");

#[program]
pub mod my_program {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, data: u64) -> Result<()> {
        let account = &mut ctx.accounts.account;
        account.data = data;
        account.authority = ctx.accounts.authority.key();
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,             // 初始化新账户
        payer = authority, // 由谁支付租金
        space = 8 + 8 + 32 // 8 字节鉴别器 + 数据长度 + 权限 Key
    )]
    pub account: Account<'info, MyAccount>,
    #[account(mut)]
    pub authority: Signer<'info>, // 签名者
    pub system_program: Program<'info, System>,
}

#[account]
pub struct MyAccount {
    pub data: u64,
    pub authority: Pubkey,
}
```

### 账户空间计算 (Space Calculation)
**关键点**：务必精确计算并显式声明账户所需的空间大小。
- Anchor 账户鉴别器：固定占用 **8 字节**。
- `Pubkey`：32 字节。
- `Vec<T>`：4 字节长度前缀 + (元素数量 * 元素大小)。
- `String`：4 字节长度前缀 + 字符内容字节。

---

## 账户安全

### 签名者校验 (Signer Validation)
**推荐做法**：使用 `Signer<'info>` 类型来强制要求该账户必须签署交易。

### 所有权与约束检查
```rust
#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(
        mut,
        has_one = authority, // 自动验证 account.authority == authority.key()
        constraint = vault.amount >= amount @ ErrorCode::InsufficientFunds // 自定义约束
    )]
    pub vault: Account<'info, Vault>,
    pub authority: Signer<'info>,
}
```

---

## 程序派生地址 (PDA)

PDA 是没有私钥、由程序控制的确定性地址，是 Solana 应用的核心。

### PDA 初始化模式
```rust
#[derive(Accounts)]
#[instruction(id: u64)]
pub struct CreateVault<'info> {
    #[account(
        init,
        payer = user,
        space = 8 + 32,
        seeds = [b"vault", user.key().as_ref(), id.to_le_bytes().as_ref()],
        bump // 自动计算并存储 bump
    )]
    pub vault: Account<'info, Vault>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}
```

---

## 跨程序调用 (CPI)

用于在一个程序中调用另一个程序（如 SPL Token 程序）。

### 调用 SPL Token 转账
```rust
use anchor_spl::token::{self, Transfer};

pub fn transfer_tokens(ctx: Context<TransferTokens>, amount: u64) -> Result<()> {
    token::transfer(
        CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.from.to_account_info(),
                to: ctx.accounts.to.to_account_info(),
                authority: ctx.accounts.authority.to_account_info(),
            },
        ),
        amount,
    )?;
    Ok(())
}
```

---

## 错误处理

使用 `#[error_code]` 宏定义清晰、有意义的自定义错误：

```rust
#[error_code]
pub enum MyError {
    #[msg("提供的金额超过了最大允许值")]
    AmountTooLarge,
    #[msg("金库余额不足")]
    InsufficientFunds,
}

// 逻辑中使用 require! 宏
require!(amount <= MAX, MyError::AmountTooLarge);
```

---

## 性能优化 (计算单元 CU)

Solana 对单笔交易的计算量有限制（通常为 200,000 CU，可请求增加）。
- **优化点 1**：尽量减少循环次数。
- **优化点 2**：使用 `Zero Copy` 模式处理超大型账户（> 10KB），避免昂贵的内存复制。
- **监控工具**：在代码中使用 `sol_log_compute_units()` 打印当前的 CU 消耗。

---

## 常见陷阱防范

1. **重新初始化攻击 (Re-initialization Attack)**：严禁在自定义逻辑中手动初始化账户。请始终使用 Anchor 提供的 `init` 约束，它会自动检查账户是否已存在。
2. **整数溢出**：Rust 在编译时通常不开启溢出检查。**推荐做法**：始终使用 `checked_add`, `checked_sub` 等安全算术方法。
3. **缺少账户验证**：攻击者可能会传入属于其它程序或不匹配的 Mint 账户。**防御**：在 `Accounts` 结构体中通过 `constraint` 明确验证 `mint`, `owner` 等关键字段。

---

## 生产环境部署检查清单

- [ ] 所有特权操作均已通过 `Signer` 进行签名验证。
- [ ] 所有数学运算均使用了 `checked_arithmetic`。
- [ ] 账户初始化严格使用了 `init` 约束以防重跑攻击。
- [ ] 为所有失败分支定义了自定义错误代码。
- [ ] 已针对高频调用的指令进行了 CU 性能分析。
- [ ] 升级权限 (Upgrade Authority) 已托管至多签钱包。
- [ ] 程序源代码已在 Solscan 上完成验证发布。
