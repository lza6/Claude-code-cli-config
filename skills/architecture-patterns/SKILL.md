---
name: architecture-patterns
model: reasoning
description: 架构模式 - 后端架构模式，用于构建可维护、可测试的系统：整洁架构、六边形架构和领域驱动设计。适用于设计新后端系统、重构单体、建立架构标准、创建可测试代码库或规划微服务分解。
---

# 架构模式

## 是什么
用于构建可维护、可测试系统的后端架构模式：整洁架构（Clean Architecture）、六边形架构（Hexagonal Architecture）和领域驱动设计（Domain-Driven Design）。

## 何时使用
- 从零设计新的后端系统
- 重构单体以提高可维护性
- 为团队建立架构标准
- 创建可测试、可模拟的代码库
- 规划微服务拆分

## 关键词
clean architecture, hexagonal, ports and adapters, DDD, domain-driven design, layers, entities, use cases, repositories, aggregates, bounded contexts

---

## 决策框架：选择哪种模式？

| 场景 | 推荐模式 |
|-----------|---------------------|
| 简单的 CRUD 应用 | 不需要（过度设计） |
| 中等复杂度，团队标准化 | 整洁架构 |
| 多个频繁变化的外部集成 | 六边形架构（端口与适配器） |
| 具有大量业务规则的复杂业务领域 | 领域驱动设计 |
| 多团队的大型系统 | DDD + 限界上下文 |

## 快速参考

### 整洁架构分层

```
┌──────────────────────────────────────┐
│      框架与驱动层（UI、DB）           │  ← 最外层：可以变更
├──────────────────────────────────────┤
│      接口适配器层                     │  ← 控制器、网关
├──────────────────────────────────────┤
│      用例层                          │  ← 应用逻辑
├──────────────────────────────────────┤
│      实体层                          │  ← 核心业务规则
└──────────────────────────────────────┘
```

**依赖规则**：依赖只能指向内层。内层永远不能导入外层。

### 六边形架构

```
         ┌─────────────┐
    ┌────│   适配器     │────┐    （REST API）
    ▼                       ▼
┌──────┐              ┌──────────┐
│ 端口  │◄────────────►│   领域    │
└──────┘              └──────────┘
    ▲                       ▲
    │    ┌─────────────┐    │
    └────│   适配器     │────┘    （数据库）
         └─────────────┘
```

**端口**：定义领域需要的接口
**适配器**：具体实现（可替换以进行测试）

---

## 目录结构

```
app/
├── domain/           # 实体与业务规则（最内层）
│   ├── entities/
│   │   └── user.py
│   ├── value_objects/
│   │   └── email.py
│   └── interfaces/   # 端口
│       └── user_repository.py
├── use_cases/        # 应用业务规则
│   └── create_user.py
├── adapters/         # 接口实现
│   ├── repositories/
│   │   └── postgres_user_repository.py
│   └── controllers/
│       └── user_controller.py
└── infrastructure/   # 框架与外部关注点
    ├── database.py
    └── config.py
```

---

## 模式 1：整洁架构

### 实体（领域层）

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """核心实体 - 无框架依赖。"""
    id: str
    email: str
    name: str
    created_at: datetime
    is_active: bool = True

    def deactivate(self):
        """实体中的业务规则。"""
        self.is_active = False

    def can_place_order(self) -> bool:
        return self.is_active
```

### 端口（接口）

```python
from abc import ABC, abstractmethod
from typing import Optional

class IUserRepository(ABC):
    """端口：定义契约，无具体实现。"""

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass
```

### 用例（应用层）

```python
@dataclass
class CreateUserRequest:
    email: str
    name: str

@dataclass
class CreateUserResponse:
    user: Optional[User]
    success: bool
    error: Optional[str] = None

class CreateUserUseCase:
    """用例：编排业务逻辑。"""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository  # 注入的依赖

    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        # 业务验证
        existing = await self.user_repository.find_by_email(request.email)
        if existing:
            return CreateUserResponse(user=None, success=False, error="Email exists")

        # 创建实体
        user = User(
            id=str(uuid.uuid4()),
            email=request.email,
            name=request.name,
            created_at=datetime.now()
        )

        saved = await self.user_repository.save(user)
        return CreateUserResponse(user=saved, success=True)
```

### 适配器（实现）

```python
class PostgresUserRepository(IUserRepository):
    """适配器：PostgreSQL 实现。"""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def find_by_id(self, user_id: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1", user_id
            )
            return self._to_entity(row) if row else None

    async def save(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO users (id, email, name, created_at, is_active)
                   VALUES ($1, $2, $3, $4, $5)
                   ON CONFLICT (id) DO UPDATE SET email=$2, name=$3, is_active=$5""",
                user.id, user.email, user.name, user.created_at, user.is_active
            )
            return user
```

---

## 模式 2：六边形架构（端口与适配器）

适用于有多个可能变化的外部集成。

```python
# 领域服务（核心）
class OrderService:
    def __init__(
        self,
        order_repo: OrderRepositoryPort,      # 端口
        payment: PaymentGatewayPort,          # 端口
        notifications: NotificationPort       # 端口
    ):
        self.orders = order_repo
        self.payments = payment
        self.notifications = notifications

    async def place_order(self, order: Order) -> OrderResult:
        # 纯业务逻辑 - 无基础设施细节
        if not order.is_valid():
            return OrderResult(success=False, error="Invalid order")

        payment = await self.payments.charge(order.total, order.customer_id)
        if not payment.success:
            return OrderResult(success=False, error="Payment failed")

        order.mark_as_paid()
        saved = await self.orders.save(order)
        await self.notifications.send(order.customer_email, "Order confirmed")

        return OrderResult(success=True, order=saved)

# 适配器（可替换以进行测试或更换提供商）
class StripePaymentAdapter(PaymentGatewayPort):
    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        # 真实的 Stripe 实现
        ...

class MockPaymentAdapter(PaymentGatewayPort):
    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        return PaymentResult(success=True, transaction_id="mock-123")
```

---

## 模式 3：领域驱动设计

适用于具有大量业务规则的复杂业务领域。

### 值对象（不可变）

```python
@dataclass(frozen=True)
class Email:
    """值对象：经过验证的、不可变的。"""
    value: str

    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError("Invalid email")

@dataclass(frozen=True)
class Money:
    amount: int  # 分
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)
```

### 聚合（一致性边界）

```python
class Order:
    """聚合根：强制不变量。"""

    def __init__(self, id: str, customer: Customer):
        self.id = id
        self.customer = customer
        self.items: List[OrderItem] = []
        self.status = OrderStatus.PENDING
        self._events: List[DomainEvent] = []

    def add_item(self, product: Product, quantity: int):
        """聚合中的业务逻辑。"""
        if quantity > product.max_quantity:
            raise ValueError(f"Max {product.max_quantity} allowed")

        item = OrderItem(product, quantity)
        self.items.append(item)
        self._events.append(ItemAddedEvent(self.id, item))

    def submit(self):
        """状态转换与不变量检查。"""
        if not self.items:
            raise ValueError("Cannot submit empty order")
        if self.status != OrderStatus.PENDING:
            raise ValueError("Order already submitted")

        self.status = OrderStatus.SUBMITTED
        self._events.append(OrderSubmittedEvent(self.id))
```

### 仓储模式

```python
class OrderRepository:
    """持久化/检索聚合，发布领域事件。"""

    async def save(self, order: Order):
        await self._persist(order)
        await self._publish_events(order._events)
        order._events.clear()
```

---

## 测试优势

所有模式都支持相同的测试方法：

```python
# 使用模拟适配器进行测试
async def test_create_user():
    mock_repo = MockUserRepository()
    use_case = CreateUserUseCase(user_repository=mock_repo)

    result = await use_case.execute(CreateUserRequest(
        email="test@example.com",
        name="Test User"
    ))

    assert result.success
    assert result.user.email == "test@example.com"
```

---

## 绝对不要做

- **贫血领域模型**：只有数据没有行为的实体（把逻辑放入实体）
- **框架耦合**：业务逻辑导入 Flask、FastAPI、Django ORM
- **臃肿控制器**：HTTP 处理器中的业务逻辑
- **泄漏抽象**：仓储返回 ORM 对象而不是领域实体
- **跨层调用**：控制器直接访问数据库
- **过度设计**：对简单 CRUD 应用使用整洁架构
- **循环依赖**：用例导入控制器
