---
name: database-migrations
description: 数据库迁移的最佳实践，涵盖架构更改、数据迁移、回滚以及跨 PostgreSQL、MySQL 和常用 ORM（Prisma、Drizzle、Kysely、Django、TypeORM、golang-migrate）的零停机部署。
origin: ECC
---

# 数据库迁移模式

为生产系统提供安全、可逆的数据库架构更改。

## 何时激活

- 创建或更改数据库表
- 添加/删除列或索引
- 运行数据迁移（回填、转换）
- 规划零停机架构更改
- 为新项目设置迁移工具

## 核心原则

1. **每一次更改都是一次迁移** —— 绝不要手动更改生产数据库
2. **生产环境中的迁移仅限向前** —— 回滚需使用新的向前迁移
3. **架构迁移和数据迁移是分离的** —— 绝不要在一次迁移中混合 DDL 和 DML
4. **针对生产规模的数据测试迁移** —— 在 100 行数据上可行的迁移在 1000 万行上可能会导致锁定
5. **迁移一旦部署即不可变** —— 绝不要编辑已在生产环境中运行过的迁移

## 迁移安全检查清单

在应用任何迁移之前：

- [ ] 迁移同时具备 UP 和 DOWN（或明确标记为不可逆）
- [ ] 大型表上没有全表锁定（使用并发操作）
- [ ] 新列具有默认值或可为空（绝不要在没有默认值的情况下添加 NOT NULL）
- [ ] 索引是并发创建的（对于现有表，不要在 CREATE TABLE 中内联创建）
- [ ] 数据回填是与架构更改分离的迁移
- [ ] 已针对生产数据的副本进行过测试
- [ ] 已记录回滚计划

## PostgreSQL 模式

### 安全添加列

```sql
-- 推荐：可为空的列，无锁定
ALTER TABLE users ADD COLUMN avatar_url TEXT;

-- 推荐：带有默认值的列（Postgres 11+ 是即时的，无需重写）
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT true;

-- 不推荐：在现有表上添加不带默认值的 NOT NULL（需要完整重写）
ALTER TABLE users ADD COLUMN role TEXT NOT NULL;
-- 这会锁定表并重写每一行
```

### 无停机添加索引

```sql
-- 不推荐：在大型表上会阻塞写入
CREATE INDEX idx_users_email ON users (email);

-- 推荐：非阻塞，允许并发写入
CREATE INDEX CONCURRENTLY idx_users_email ON users (email);

-- 注意：CONCURRENTLY 不能在事务块内运行
-- 大多数迁移工具需要对此进行特殊处理
```

### 重命名列（零停机）

绝不要在生产环境中直接重命名。使用“扩展-收缩”模式：

```sql
-- 第 1 步：添加新列（迁移 001）
ALTER TABLE users ADD COLUMN display_name TEXT;

-- 第 2 步：回填数据（迁移 002，数据迁移）
UPDATE users SET display_name = username WHERE display_name IS NULL;

-- 第 3 步：更新应用程序代码以同时读取/写入这两个列
-- 部署应用程序更改

-- 第 4 步：停止写入旧列，将其删除（迁移 003）
ALTER TABLE users DROP COLUMN username;
```

### 安全删除列

```sql
-- 第 1 步：删除应用程序中对该列的所有引用
-- 第 2 步：部署不带该列引用的应用程序
-- 第 3 步：在下一次迁移中删除列
ALTER TABLE orders DROP COLUMN legacy_status;

-- 对于 Django：使用 SeparateDatabaseAndState 从模型中删除
-- 而不生成 DROP COLUMN（然后在下一次迁移中删除）
```

### 大型数据迁移

```sql
-- 不推荐：在一次事务中更新所有行（会锁定表）
UPDATE users SET normalized_email = LOWER(email);

-- 推荐：带进度的批量更新
DO $$
DECLARE
  batch_size INT := 10000;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE users
    SET normalized_email = LOWER(email)
    WHERE id IN (
      SELECT id FROM users
      WHERE normalized_email IS NULL
      LIMIT batch_size
      FOR UPDATE SKIP LOCKED
    );
    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    RAISE NOTICE 'Updated % rows', rows_updated;
    EXIT WHEN rows_updated = 0;
    COMMIT;
  END LOOP;
END $$;
```

## Prisma (TypeScript/Node.js)

### 工作流

```bash
# 从架构更改创建迁移
npx prisma migrate dev --name add_user_avatar

# 在生产环境中应用待处理的迁移
npx prisma migrate deploy

# 重置数据库（仅限开发环境）
npx prisma migrate reset

# 架构更改后生成客户端
npx prisma generate
```

### 架构示例

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  avatarUrl String?  @map("avatar_url")
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  orders    Order[]

  @@map("users")
  @@index([email])
}
```

### 自定义 SQL 迁移

对于 Prisma 无法表达的操作（并发索引、数据回填）：

```bash
# 创建仅限创建的迁移，然后手动编辑 SQL
npx prisma migrate dev --create-only --name add_email_index
```

```sql
-- migrations/20240115_add_email_index/migration.sql
-- Prisma 无法生成 CONCURRENTLY，因此我们手动编写它
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users (email);
```

## Drizzle (TypeScript/Node.js)

### 工作流

```bash
# 从架构更改生成迁移
npx drizzle-kit generate

# 应用迁移
npx drizzle-kit migrate

# 直接推送架构（仅限开发环境，无迁移文件）
npx drizzle-kit push
```

### 架构示例

```typescript
import { pgTable, text, timestamp, uuid, boolean } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  email: text("email").notNull().unique(),
  name: text("name"),
  isActive: boolean("is_active").notNull().default(true),
  createdAt: timestamp("created_at").notNull().defaultNow(),
  updatedAt: timestamp("updated_at").notNull().defaultNow(),
});
```

## Kysely (TypeScript/Node.js)

### 工作流 (kysely-ctl)

```bash
# 初始化配置文件 (kysely.config.ts)
kysely init

# 创建新的迁移文件
kysely migrate make add_user_avatar

# 应用所有待处理的迁移
kysely migrate latest

# 回滚上一个迁移
kysely migrate down

# 显示迁移状态
kysely migrate list
```

### 迁移文件

```typescript
// migrations/2024_01_15_001_create_user_profile.ts
import { type Kysely, sql } from 'kysely'

// 重要：始终使用 Kysely<any>，而不是您的类型化 DB 接口。
// 迁移在时间上是冻结的，不得依赖当前的架构类型。
export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable('user_profile')
    .addColumn('id', 'serial', (col) => col.primaryKey())
    .addColumn('email', 'varchar(255)', (col) => col.notNull().unique())
    .addColumn('avatar_url', 'text')
    .addColumn('created_at', 'timestamp', (col) =>
      col.defaultTo(sql`now()`).notNull()
    )
    .execute()

  await db.schema
    .createIndex('idx_user_profile_avatar')
    .on('user_profile')
    .column('avatar_url')
    .execute()
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable('user_profile').execute()
}
```

### 程序化迁移器

```typescript
import { Migrator, FileMigrationProvider } from 'kysely'
import { promises as fs } from 'fs'
import * as path from 'path'
// 仅限 ESM —— CJS 可以直接使用 __dirname
import { fileURLToPath } from 'url'
const migrationFolder = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  './migrations',
)

// `db` 是您的 Kysely<any> 数据库实例
const migrator = new Migrator({
  db,
  provider: new FileMigrationProvider({
    fs,
    path,
    migrationFolder,
  }),
  // 警告：仅在开发环境中启用。禁用时间戳排序验证，这可能会导致环境之间的架构漂移。
  // allowUnorderedMigrations: true,
})

const { error, results } = await migrator.migrateToLatest()

results?.forEach((it) => {
  if (it.status === 'Success') {
    console.log(`迁移 "${it.migrationName}" 执行成功`)
  } else if (it.status === 'Error') {
    console.error(`执行迁移 "${it.migrationName}" 失败`)
  }
})

if (error) {
  console.error('迁移失败', error)
  process.exit(1)
}
```

## Django (Python)

### 工作流

```bash
# 从模型更改生成迁移
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 显示迁移状态
python manage.py showmigrations

# 为自定义 SQL 生成空迁移
python manage.py makemigrations --empty app_name -n description
```

### 数据迁移

```python
from django.db import migrations

def backfill_display_names(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    batch_size = 5000
    users = User.objects.filter(display_name="")
    while users.exists():
        batch = list(users[:batch_size])
        for user in batch:
            user.display_name = user.username
        User.objects.bulk_update(batch, ["display_name"], batch_size=batch_size)

def reverse_backfill(apps, schema_editor):
    pass  # 数据迁移，无需反向操作

class Migration(migrations.Migration):
    dependencies = [("accounts", "0015_add_display_name")]

    operations = [
        migrations.RunPython(backfill_display_names, reverse_backfill),
    ]
```

### SeparateDatabaseAndState

在不立即从数据库中删除列的情况下从 Django 模型中删除列：

```python
class Migration(migrations.Migration):
    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(model_name="user", name="legacy_field"),
            ],
            database_operations=[],  # 暂不触动数据库
        ),
    ]
```

## golang-migrate (Go)

### 工作流

```bash
# 创建迁移对
migrate create -ext sql -dir migrations -seq add_user_avatar

# 应用所有待处理的迁移
migrate -path migrations -database "$DATABASE_URL" up

# 回滚上一个迁移
migrate -path migrations -database "$DATABASE_URL" down 1

# 强制版本（修复脏状态）
migrate -path migrations -database "$DATABASE_URL" force VERSION
```

### 迁移文件

```sql
-- migrations/000003_add_user_avatar.up.sql
ALTER TABLE users ADD COLUMN avatar_url TEXT;
CREATE INDEX CONCURRENTLY idx_users_avatar ON users (avatar_url) WHERE avatar_url IS NOT NULL;

-- migrations/000003_add_user_avatar.down.sql
DROP INDEX IF EXISTS idx_users_avatar;
ALTER TABLE users DROP COLUMN IF EXISTS avatar_url;
```

## 零停机迁移策略

对于关键的生产更改，请遵循“扩展-收缩”模式：

```
第 1 阶段：扩展 (EXPAND)
  - 添加新列/表（可为空或带有默认值）
  - 部署：应用程序同时向旧列和新列写入
  - 回填现有数据

第 2 阶段：迁移 (MIGRATE)
  - 部署：应用程序从新列读取，向两列写入
  - 验证数据一致性

第 3 阶段：收缩 (CONTRACT)
  - 部署：应用程序仅使用新列
  - 在单独的迁移中删除旧列/表
```

### 时间线示例

```
第 1 天：迁移添加 new_status 列（可为空）
第 1 天：部署应用 v2 —— 同时向 status 和 new_status 写入
第 2 天：运行现有行的回填迁移
第 3 天：部署应用 v3 —— 仅从 new_status 读取
第 7 天：迁移删除旧的 status 列
```

## 反模式

| 反模式 | 失败原因 | 更好的方法 |
|-------------|-------------|-----------------|
| 在生产中使用手动 SQL | 无审计轨迹，不可重复 | 始终使用迁移文件 |
| 编辑已部署的迁移 | 导致环境之间的漂移 | 创建新的迁移 |
| 不带默认值的 NOT NULL | 锁定表，重写所有行 | 添加可为空的列，回填，然后添加约束 |
| 在大型表上使用内联索引 | 在构建期间阻塞写入 | 使用 CREATE INDEX CONCURRENTLY |
| 在一次迁移中混合架构和数据 | 难以回滚，长事务 | 将迁移分离 |
| 在移除代码前删除列 | 应用程序因缺少列而报错 | 先移除代码，在下一次部署中删除列 |
