---
name: android-clean-architecture
description: "适用于 Android 和 Kotlin 多平台 (KMP) 项目的整洁架构 (Clean Architecture) 模式 —— 包括模块结构、依赖规则、UseCase、Repository 以及数据层模式。"
origin: ECC
---

# Android 整洁架构 (Android Clean Architecture)

适用于 Android 和 KMP 项目的整洁架构模式。涵盖模块边界、依赖倒置、UseCase/Repository 模式，以及使用 Room、SQLDelight 和 Ktor 进行的数据层设计。

## 何时激活

- 规划 Android 或 KMP 项目的模块结构
- 实现 UseCase、Repository 或 DataSource
- 设计各层（领域层、数据层、表现层）之间的数据流
- 使用 Koin 或 Hilt 设置依赖注入
- 在分层架构中使用 Room、SQLDelight 或 Ktor

## 模块结构 (Module Structure)

### 推荐布局

```
project/
├── app/                  # Android 入口点、依赖注入配置、Application 类
├── core/                 # 共享工具类、基类、错误类型
├── domain/               # UseCase、领域模型、Repository 接口（纯 Kotlin）
├── data/                 # Repository 实现、DataSource、数据库、网络
├── presentation/         # 界面、ViewModel、UI 模型、导航
├── design-system/        # 可重用的 Compose 组件、主题、排版
31	└── feature/              # 功能模块（可选，用于大型项目）
32	    ├── auth/
33	    ├── settings/
34	    └── profile/
```

### 依赖规则

```
app → presentation, domain, data, core
presentation → domain, design-system, core
data → domain, core
domain → core (或无依赖)
core → (无)
```

**关键原则**：`domain` 层绝不能依赖 `data` 层、`presentation` 层或任何框架。它应仅包含纯 Kotlin 代码。

## 领域层 (Domain Layer)

### UseCase 模式

每个 UseCase 代表一个业务操作。使用 `operator fun invoke` 使调用更简洁：

```kotlin
class GetItemsByCategoryUseCase(
    private val repository: ItemRepository
) {
    suspend operator fun invoke(category: String): Result<List<Item>> {
        return repository.getItemsByCategory(category)
    }
}

// 基于 Flow 的 UseCase，用于响应式流
class ObserveUserProgressUseCase(
    private val repository: UserRepository
) {
    operator fun invoke(userId: String): Flow<UserProgress> {
        return repository.observeProgress(userId)
    }
}
```

### 领域模型 (Domain Models)

领域模型是纯 Kotlin 数据类 —— 无需任何框架注解：

```kotlin
data class Item(
    val id: String,
    val title: String,
    val description: String,
    val tags: List<String>,
    val status: Status,
    val category: String
)

enum class Status { DRAFT, ACTIVE, ARCHIVED }
```

### Repository 接口

在领域层定义，在数据层实现：

```kotlin
interface ItemRepository {
    suspend fun getItemsByCategory(category: String): Result<List<Item>>
    suspend fun saveItem(item: Item): Result<Unit>
    fun observeItems(): Flow<List<Item>>
}
```

## 数据层 (Data Layer)

### Repository 实现

负责协调本地和远程数据源：

```kotlin
class ItemRepositoryImpl(
    private val localDataSource: ItemLocalDataSource,
    private val remoteDataSource: ItemRemoteDataSource
) : ItemRepository {

    override suspend fun getItemsByCategory(category: String): Result<List<Item>> {
        return runCatching {
            val remote = remoteDataSource.fetchItems(category)
            localDataSource.insertItems(remote.map { it.toEntity() })
            localDataSource.getItemsByCategory(category).map { it.toDomain() }
        }
    }

    override suspend fun saveItem(item: Item): Result<Unit> {
        return runCatching {
            localDataSource.insertItems(listOf(item.toEntity()))
        }
    }

    override fun observeItems(): Flow<List<Item>> {
        return localDataSource.observeAll().map { entities ->
            entities.map { it.toDomain() }
        }
    }
}
```

### 映射器 (Mapper) 模式

将映射逻辑作为扩展函数保留在数据模型附近：

```kotlin
// 在数据层中
fun ItemEntity.toDomain() = Item(
    id = id,
    title = title,
    description = description,
    tags = tags.split("|"),
    status = Status.valueOf(status),
    category = category
)

fun ItemDto.toEntity() = ItemEntity(
    id = id,
    title = title,
    description = description,
    tags = tags.joinToString("|"),
    status = status,
    category = category
)
```

### Room 数据库 (Android)

```kotlin
@Entity(tableName = "items")
data class ItemEntity(
    @PrimaryKey val id: String,
    val title: String,
    val description: String,
    val tags: String,
    val status: String,
    val category: String
)

@Dao
interface ItemDao {
    @Query("SELECT * FROM items WHERE category = :category")
    suspend fun getByCategory(category: String): List<ItemEntity>

    @Upsert
    suspend fun upsert(items: List<ItemEntity>)

    @Query("SELECT * FROM items")
    fun observeAll(): Flow<List<ItemEntity>>
}
```

### SQLDelight (KMP)

```sql
-- Item.sq
CREATE TABLE ItemEntity (
    id TEXT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    tags TEXT NOT NULL,
    status TEXT NOT NULL,
    category TEXT NOT NULL
);

getByCategory:
SELECT * FROM ItemEntity WHERE category = ?;

upsert:
INSERT OR REPLACE INTO ItemEntity (id, title, description, tags, status, category)
VALUES (?, ?, ?, ?, ?, ?);

observeAll:
SELECT * FROM ItemEntity;
```

### Ktor 网络客户端 (KMP)

```kotlin
class ItemRemoteDataSource(private val client: HttpClient) {

    suspend fun fetchItems(category: String): List<ItemDto> {
        return client.get("api/items") {
            parameter("category", category)
        }.body()
    }
}

// 包含内容协商 (Content Negotiation) 的 HttpClient 设置
val httpClient = HttpClient {
    install(ContentNegotiation) { json(Json { ignoreUnknownKeys = true }) }
    install(Logging) { level = LogLevel.HEADERS }
    defaultRequest { url("https://api.example.com/") }
}
```

## 依赖注入 (Dependency Injection)

### Koin (对 KMP 友好)

```kotlin
// Domain 模块
val domainModule = module {
    factory { GetItemsByCategoryUseCase(get()) }
    factory { ObserveUserProgressUseCase(get()) }
}

// Data 模块
val dataModule = module {
    single<ItemRepository> { ItemRepositoryImpl(get(), get()) }
    single { ItemLocalDataSource(get()) }
    single { ItemRemoteDataSource(get()) }
}

// Presentation 模块
val presentationModule = module {
    viewModelOf(::ItemListViewModel)
    viewModelOf(::DashboardViewModel)
}
```

### Hilt (仅限 Android)

```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    abstract fun bindItemRepository(impl: ItemRepositoryImpl): ItemRepository
}

@HiltViewModel
class ItemListViewModel @Inject constructor(
    private val getItems: GetItemsByCategoryUseCase
) : ViewModel()
```

## 错误处理

### Result/Try 模式

使用 `Result<T>` 或自定义密封类型进行错误传播：

```kotlin
sealed interface Try<out T> {
    data class Success<T>(val value: T) : Try<T>
    data class Failure(val error: AppError) : Try<Nothing>
}

sealed interface AppError {
    data class Network(val message: String) : AppError
    data class Database(val message: String) : AppError
    data object Unauthorized : AppError
}

// 在 ViewModel 中 —— 映射到 UI 状态
viewModelScope.launch {
    when (val result = getItems(category)) {
        is Try.Success -> _state.update { it.copy(items = result.value, isLoading = false) }
        is Try.Failure -> _state.update { it.copy(error = result.error.toMessage(), isLoading = false) }
    }
}
```

## 约定插件 (Convention Plugins, Gradle)

对于 KMP 项目，使用约定插件来减少构建文件的重复：

```kotlin
// build-logic/src/main/kotlin/kmp-library.gradle.kts
plugins {
    id("org.jetbrains.kotlin.multiplatform")
}

kotlin {
    androidTarget()
    iosX64(); iosArm64(); iosSimulatorArm64()
    sourceSets {
        commonMain.dependencies { /* 共享依赖 */ }
        commonTest.dependencies { implementation(kotlin("test")) }
    }
}
```

在模块中应用：

```kotlin
// domain/build.gradle.kts
plugins { id("kmp-library") }
```

## 应当避免的错误模式 (Anti-Patterns)

- 在 `domain` 层导入 Android 框架类 —— 保持领域层纯净。
- 将数据库实体或 DTO 直接暴露给 UI 层 —— 始终映射为领域模型。
- 将业务逻辑放入 ViewModel —— 应提取到 UseCase 中。
- 使用 `GlobalScope` 或非结构化协程 —— 请使用 `viewModelScope` 或结构化并发。
- 过于臃肿的 Repository 实现 —— 将其拆分为聚焦的 DataSource。
- 循环模块依赖 —— 如果 A 依赖 B，则 B 绝不能依赖 A。

## 参考资料

界面模式请参考技能：`compose-multiplatform-patterns`。
异步模式请参考技能：`kotlin-coroutines-flows`。
