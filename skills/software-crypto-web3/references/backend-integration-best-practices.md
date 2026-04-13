# 后端加密集成最佳实践

在 .NET/C# 中构建企业级加密货币集成平台的模式。基于与 TON、Fireblocks 和其他区块链提供商集成的生产系统。

---

＃＃ 目录

1.[架构模式](#architecture-patterns)
2. [CQRS 与 MediatR](#cqrs-with-mediatr)
3. [使用 FluentResults 进行面向铁路的编程](#railway-oriented-programming-with-fluentresults)
4. [多提供商架构](#multi-provider-architecture)
5. [Webhook 处理](#webhook-handling)
6. [Kafka 事件驱动架构](#event-driven-architecture-with-kafka)
7. [交易生命周期管理](#transaction-lifecycle-management)
8. [钱包管理](#wallet-management)
9. [HTTP 客户端弹性](#http-client-resilience)
10. [配置模式](#configuration-patterns)
11. [测试模式](#testing-patterns)
12. [安全检查表](#security-checklist)
13.[可观察性](#observability)

## 架构模式

### 分层架构

**加密集成的标准项目结构：**

```
sources/
├── core/                    # Business logic & domain models
│   ├── Data/               # Enums, constants, domain models
│   ├── Services/           # Command handlers, service implementations
│   └── Parties/            # Crypto party creation & management
├── infrastructure/          # Technical integration & data access
│   ├── Kafka/              # Message publishing/consuming
│   ├── BlockchainApi/      # Blockchain client integrations
│   └── CustodialApi/       # Custodial provider integrations (Fireblocks)
├── presentation/            # API endpoints
│   ├── PublicApi/          # User-facing endpoints
│   ├── PrivateApi/         # Internal service endpoints
│   └── Contracts/          # Shared DTOs
└── tests/
    ├── UnitTests/          # NUnit + Moq + AutoFixture
    ├── Api.Tests/          # Integration tests
    └── Utils/              # Test helpers, Wiremock
```

---

## CQRS 与 MediatR

**基于命令的加密操作设计：**

```csharp
// Command definition
public record OnboardUserCommand(
    string UserId,
    Currency Currency,
    CryptoNetwork Network
) : IRequest<Result<OnboardCommandResult>>;

// Handler with provider selection
public class OnboardUserCommandHandler : IRequestHandler<OnboardUserCommand, Result<OnboardCommandResult>>
{
    private readonly IMediator _mediator;
    private readonly ICalculateProviderService _calculateProviderService;

    public async Task<Result<OnboardCommandResult>> Handle(
        OnboardUserCommand request,
        CancellationToken cancellationToken)
    {
        var provider = await _calculateProviderService.GetCryptoProviderAsync(
            request.Currency, request.Network);

        return provider switch
        {
            CryptoProvider.TonDirect => await _mediator.Send(
                new TonApiOnboardUserCommand(request.UserId), cancellationToken),
            CryptoProvider.Fireblocks => await _mediator.Send(
                new FireblocksOnboardUserCommand(request.UserId, request.Currency), cancellationToken),
            _ => Result.Fail<OnboardCommandResult>("Unsupported provider")
        };
    }
}
```

**好处：**
- 清晰的关注点分离
- 轻松切换提供商
- 可使用模拟 MediatR 进行测试

---

## 使用 FluentResults 进行面向铁路的编程

**无异常的错误处理：**

```csharp
// Service returning Result
public async Task<Result<PaymentInfo>> CreatePaymentAsync(CreatePaymentRequest request)
{
    var walletResult = await _walletService.GetWalletAsync(request.UserId);
    if (walletResult.IsFailed)
        return walletResult.ToResult<PaymentInfo>();

    var validationResult = ValidatePayment(request);
    if (validationResult.IsFailed)
        return validationResult;

    var payment = new PaymentInfo
    {
        Id = Guid.NewGuid(),
        Amount = request.Amount,
        Currency = request.Currency
    };

    await _unitOfWork.Get<PaymentInfo>().AddAsync(payment);
    await _unitOfWork.SaveChangesAsync();

    return Result.Ok(payment);
}

// Controller converting Result to HTTP response
[HttpPost]
public async Task<IActionResult> CreatePayment([FromBody] CreatePaymentRequest request)
{
    var result = await _mediator.Send(new CreatePaymentCommand(request));

    return result.ToApiResult(
        onSuccess: payment => Ok(new { PaymentId = payment.Id }),
        onFailure: errors => BadRequest(new { Errors = errors.Select(e => e.Message) })
    );
}
```

**HTTP 响应扩展：**
```csharp
public static class ResultExtensions
{
    public static IActionResult ToApiResult<T>(
        this Result<T> result,
        Func<T, IActionResult> onSuccess,
        Func<IEnumerable<IError>, IActionResult> onFailure)
    {
        return result.IsSuccess
            ? onSuccess(result.Value)
            : onFailure(result.Errors);
    }
}
```

---

## 多提供商架构

**抽象提供者接口：**

```csharp
public interface ICryptoProvider
{
    CryptoProvider ProviderType { get; }
    Task<Result<WalletInfo>> CreateWalletAsync(string userId, Currency currency);
    Task<Result<TransactionInfo>> CreatePayoutAsync(PayoutRequest request);
    Task<Result<decimal>> GetBalanceAsync(string address, Currency currency);
}

// Provider implementations
public class TonDirectProvider : ICryptoProvider
{
    public CryptoProvider ProviderType => CryptoProvider.TonDirect;

    public async Task<Result<WalletInfo>> CreateWalletAsync(string userId, Currency currency)
    {
        // Direct blockchain wallet creation via TonCenter API
        var wallet = await _tonApiClient.CreateWalletAsync(userId);
        return Result.Ok(new WalletInfo(wallet.Address, wallet.PublicKey));
    }
}

public class FireblocksProvider : ICryptoProvider
{
    public CryptoProvider ProviderType => CryptoProvider.Fireblocks;

    public async Task<Result<WalletInfo>> CreateWalletAsync(string userId, Currency currency)
    {
        // Custodial wallet via Fireblocks vault
        var vault = await _fireblocksClient.CreateVaultAccountAsync(userId);
        return Result.Ok(new WalletInfo(vault.DepositAddress, vault.VaultId));
    }
}
```

**提供商选择服务：**

```csharp
public class CalculateProviderService : ICalculateProviderService
{
    public async Task<CryptoProvider> GetCryptoProviderAsync(
        Currency currency,
        CryptoNetwork network,
        ProviderSelectionCriteria? criteria = null)
    {
        // Provider routing logic based on:
        // - Currency/network support
        // - Fee optimization
        // - Compliance requirements
        // - User preferences (custodial vs non-custodial)

        return (currency, network) switch
        {
            (Currency.TON, CryptoNetwork.TON) => CryptoProvider.TonDirect,
            (Currency.USDT, CryptoNetwork.TON) => CryptoProvider.TonDirect,  // Jetton
            (Currency.ETH, CryptoNetwork.Ethereum) => CryptoProvider.Fireblocks,
            (Currency.USDT, CryptoNetwork.Ethereum) => CryptoProvider.Fireblocks,  // ERC-20
            _ => CryptoProvider.Fireblocks  // Default to custodial
        };
    }
}
```

---

## Webhook 处理

**Webhook 安全性签名验证：**

```csharp
public class FireblocksWebhookSignatureValidator : IWebhookSignatureValidator
{
    private readonly string _webhookSecret;

    public bool ValidateSignature(string payload, string signature, string timestamp)
    {
        var expectedSignature = ComputeHmacSha256(
            $"{timestamp}.{payload}",
            _webhookSecret);

        return CryptographicOperations.FixedTimeEquals(
            Encoding.UTF8.GetBytes(signature),
            Encoding.UTF8.GetBytes(expectedSignature));
    }

    private static string ComputeHmacSha256(string data, string secret)
    {
        using var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(secret));
        var hash = hmac.ComputeHash(Encoding.UTF8.GetBytes(data));
        return Convert.ToBase64String(hash);
    }
}

// Authentication handler for webhook endpoints
public class WebhookSignatureAuthenticationHandler : AuthenticationHandler<AuthenticationSchemeOptions>
{
    protected override async Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        if (!Request.Headers.TryGetValue("X-Signature", out var signature))
            return AuthenticateResult.Fail("Missing signature header");

        Request.EnableBuffering();
        using var reader = new StreamReader(Request.Body, leaveOpen: true);
        var body = await reader.ReadToEndAsync();
        Request.Body.Position = 0;

        if (!_validator.ValidateSignature(body, signature, timestamp))
            return AuthenticateResult.Fail("Invalid signature");

        var claims = new[] { new Claim(ClaimTypes.Name, "webhook") };
        var identity = new ClaimsIdentity(claims, Scheme.Name);
        return AuthenticateResult.Success(new AuthenticationTicket(
            new ClaimsPrincipal(identity), Scheme.Name));
    }
}
```

**Webhook 控制器：**

```csharp
[ApiController]
[Route("v1/webhooks")]
public class WebhookController : ControllerBase
{
    [HttpPost("fireblocks/transactions")]
    [Authorize(AuthenticationSchemes = "FireblocksWebhook")]
    public async Task<IActionResult> HandleFireblocksTransaction(
        [FromBody] FireblocksTransactionWebhook webhook)
    {
        // Publish to Kafka for async processing
        await _kafkaProducer.PublishAsync(new FireblocksTransactionMessage
        {
            TransactionId = webhook.Data.Id,
            Status = webhook.Data.Status,
            TxHash = webhook.Data.TxHash
        });

        return Ok();  // Always return 200 to acknowledge receipt
    }
}
```

---

## Kafka 的事件驱动架构

**消息合约（Protobuf）：**

```protobuf
syntax = "proto3";

message CryptoPaymentReceivedMessage {
    string payment_id = 1;
    string user_id = 2;
    string amount = 3;
    string currency = 4;
    string tx_hash = 5;
    int64 timestamp = 6;
}

message CryptoUserWalletCreatedMessage {
    string wallet_id = 1;
    string user_id = 2;
    string address = 3;
    string network = 4;
}
```

**生产者模式：**

```csharp
public class CryptoPaymentNotificationHandler
    : INotificationHandler<CryptoPaymentCompletedNotification>
{
    private readonly IKafkaProducer<string, CryptoPaymentReceivedMessage> _producer;

    public async Task Handle(
        CryptoPaymentCompletedNotification notification,
        CancellationToken cancellationToken)
    {
        var message = new CryptoPaymentReceivedMessage
        {
            PaymentId = notification.PaymentId.ToString(),
            UserId = notification.UserId,
            Amount = notification.Amount.ToString(),
            Currency = notification.Currency.ToString(),
            TxHash = notification.TxHash,
            Timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds()
        };

        await _producer.PublishAsync(
            topic: "crypto.payments.received",
            key: notification.PaymentId.ToString(),
            value: message,
            cancellationToken);
    }
}
```

**消费模式：**

```csharp
public class FireblocksTransactionMessageHandler
    : IMessageHandler<FireblocksTransactionWebhookMessage>
{
    private readonly IMediator _mediator;

    public async Task HandleAsync(
        ConsumeResult<string, FireblocksTransactionWebhookMessage> message,
        CancellationToken cancellationToken)
    {
        var result = await _mediator.Send(
            new ProcessFireblocksTransactionCommand(
                message.Message.Value.TransactionId,
                message.Message.Value.Status),
            cancellationToken);

        if (result.IsFailed)
        {
            _logger.LogError("Failed to process transaction: {Errors}",
                result.Errors);
            throw new MessageProcessingException(result.Errors.First().Message);
        }
    }
}
```

---

## 交易生命周期管理

**交易状态机：**

```csharp
public enum TransactionStatus
{
    Created,
    Pending,
    Confirming,
    Completed,
    Failed,
    Cancelled
}

public class TransactionStateMachine
{
    private static readonly Dictionary<(TransactionStatus, TransactionEvent), TransactionStatus>
        _transitions = new()
    {
        { (TransactionStatus.Created, TransactionEvent.Submitted), TransactionStatus.Pending },
        { (TransactionStatus.Pending, TransactionEvent.Broadcast), TransactionStatus.Confirming },
        { (TransactionStatus.Confirming, TransactionEvent.Confirmed), TransactionStatus.Completed },
        { (TransactionStatus.Pending, TransactionEvent.Rejected), TransactionStatus.Failed },
        { (TransactionStatus.Confirming, TransactionEvent.Reverted), TransactionStatus.Failed },
    };

    public Result<TransactionStatus> TryTransition(
        TransactionStatus current,
        TransactionEvent evt)
    {
        if (_transitions.TryGetValue((current, evt), out var next))
            return Result.Ok(next);

        return Result.Fail($"Invalid transition: {current} + {evt}");
    }
}
```

**交易监控服务：**

```csharp
public class TransactionMonitoringService : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            var pendingTransactions = await _repository
                .GetPendingTransactionsAsync(stoppingToken);

            foreach (var tx in pendingTransactions)
            {
                var status = await _blockchainClient
                    .GetTransactionStatusAsync(tx.TxHash);

                if (status != tx.Status)
                {
                    await _mediator.Send(new UpdateTransactionStatusCommand(
                        tx.Id, status), stoppingToken);
                }
            }

            await Task.Delay(TimeSpan.FromSeconds(10), stoppingToken);
        }
    }
}
```

---

## 钱包管理

**具有多网络支持的钱包实体：**

```csharp
public class CryptoWallet
{
    public Guid Id { get; set; }
    public string UserId { get; set; }
    public string Address { get; set; }
    public CryptoNetwork Network { get; set; }
    public WalletType Type { get; set; }  // Custodial, NonCustodial
    public CryptoProvider Provider { get; set; }
    public WalletStatus Status { get; set; }
    public DateTime CreatedAt { get; set; }

    // Provider-specific data
    public string? VaultAccountId { get; set; }  // Fireblocks
    public int? SubWalletId { get; set; }  // TON
}

public enum WalletType
{
    Custodial,      // Provider holds keys (Fireblocks)
    NonCustodial,   // User holds keys
    Embedded        // App-embedded wallet
}
```

**TON 的地址推导：**

```csharp
public class TonWalletAddressService
{
    public string DeriveWalletAddress(byte[] publicKey, int subWalletId, WalletVersion version)
    {
        return version switch
        {
            WalletVersion.V4R2 => DeriveV4R2Address(publicKey, subWalletId),
            WalletVersion.V5R1 => DeriveV5R1Address(publicKey, subWalletId),
            _ => throw new NotSupportedException($"Wallet version {version} not supported")
        };
    }

    private string DeriveV4R2Address(byte[] publicKey, int subWalletId)
    {
        // TON address derivation logic
        var stateInit = BuildWalletV4StateInit(publicKey, subWalletId);
        var hash = ComputeStateInitHash(stateInit);
        return EncodeAddress(hash, workchain: 0, bounceable: true);
    }
}
```

---

## HTTP 客户端弹性

**基于 Polly 的弹性政策：**

```csharp
public static class HttpClientExtensions
{
    public static IHttpClientBuilder AddCryptoResilienceHandler(
        this IHttpClientBuilder builder,
        HttpClientResilienceOptions options)
    {
        return builder.AddResilienceHandler("crypto-resilience", pipeline =>
        {
            // Retry policy
            pipeline.AddRetry(new HttpRetryStrategyOptions
            {
                MaxRetryAttempts = options.Retry.MaxRetryAttempts,
                BackoffType = DelayBackoffType.Exponential,
                UseJitter = true,
                Delay = TimeSpan.FromSeconds(1),
                ShouldHandle = new PredicateBuilder<HttpResponseMessage>()
                    .Handle<HttpRequestException>()
                    .HandleResult(r => r.StatusCode >= HttpStatusCode.InternalServerError)
            });

            // Circuit breaker
            pipeline.AddCircuitBreaker(new HttpCircuitBreakerStrategyOptions
            {
                FailureRatio = options.CircuitBreaker.FailureRatio,
                SamplingDuration = TimeSpan.FromSeconds(30),
                MinimumThroughput = 10,
                BreakDuration = TimeSpan.FromSeconds(30)
            });

            // Timeout
            pipeline.AddTimeout(options.AttemptTimeout.Timeout);
        });
    }
}

// Usage in DI
services.AddHttpClient<ITonCenterClient, TonCenterClient>(client =>
{
    client.BaseAddress = new Uri(configuration["TonCenter:BaseUrl"]);
})
.AddCryptoResilienceHandler(options);
```

---

## 配置模式

**强类型选项：**

```csharp
public sealed record CryptoPayoutOptions
{
    public required TimeSpan ResendDelay { get; init; }
    public required TimeSpan RetryTimeout { get; init; }
    public required int MaxRetryAttempts { get; init; }
}

public sealed record TonWalletOptions
{
    public required string MasterSeedVaultKey { get; init; }  // Vault reference
    public required WalletVersion DefaultVersion { get; init; }
    public required Dictionary<string, JettonConfig> Jettons { get; init; }
}

public sealed record JettonConfig
{
    public required string MasterAddress { get; init; }
    public required int Decimals { get; init; }
}
```

**appsettings.json 结构：**

```json
{
  "CryptoPayoutOptions": {
    "ResendDelay": "00:05:00",
    "RetryTimeout": "1.00:00:00",
    "MaxRetryAttempts": 3
  },
  "TonWalletOptions": {
    "MasterSeedVaultKey": "crypto/ton/master-seed",
    "DefaultVersion": "V4R2",
    "Jettons": {
      "USDT": {
        "MasterAddress": "EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs",
        "Decimals": 6
      }
    }
  },
  "FireblocksOptions": {
    "ApiKey": "${FIREBLOCKS_API_KEY}",
    "ApiSecretVaultKey": "crypto/fireblocks/api-secret",
    "BaseUrl": "https://api.fireblocks.io"
  }
}
```

---

## 测试模式

**使用装置进行单元测试：**

```csharp
[TestFixture]
public class CreatePaymentCommandHandlerTests
{
    private CreatePaymentCommandHandlerFixture _fixture;

    [SetUp]
    public void SetUp() => _fixture = new CreatePaymentCommandHandlerFixture();

    [Test]
    public async Task Handle_WhenValidRequest_ShouldCreatePayment()
    {
        // Arrange
        var command = _fixture.CreateValidCommand();
        _fixture.SetupWalletExists();
        _fixture.SetupProviderSuccess();

        // Act
        var result = await _fixture.Handler.Handle(command, CancellationToken.None);

        // Assert
        result.IsSuccess.Should().BeTrue();
        result.Value.PaymentId.Should().NotBeEmpty();
        _fixture.VerifyPaymentSaved();
    }
}

public class CreatePaymentCommandHandlerFixture
{
    public Mock<ICryptoUnitOfWork> UnitOfWorkMock { get; } = new();
    public Mock<IWalletService> WalletServiceMock { get; } = new();
    public CreatePaymentCommandHandler Handler { get; }

    public CreatePaymentCommandHandlerFixture()
    {
        Handler = new CreatePaymentCommandHandler(
            UnitOfWorkMock.Object,
            WalletServiceMock.Object);
    }

    public CreatePaymentCommand CreateValidCommand() =>
        new AutoFixture.Fixture().Create<CreatePaymentCommand>();

    public void SetupWalletExists() =>
        WalletServiceMock
            .Setup(x => x.GetWalletAsync(It.IsAny<string>()))
            .ReturnsAsync(Result.Ok(new WalletInfo()));
}
```

**与 Wiremock 集成测试：**

```csharp
[TestFixture]
public class TonCenterClientIntegrationTests
{
    private WireMockServer _server;
    private TonCenterClient _client;

    [SetUp]
    public void SetUp()
    {
        _server = WireMockServer.Start();
        _client = new TonCenterClient(new HttpClient
        {
            BaseAddress = new Uri(_server.Urls[0])
        });
    }

    [Test]
    public async Task GetBalance_ShouldReturnBalance()
    {
        // Arrange
        _server
            .Given(Request.Create()
                .WithPath("/v2/getAddressBalance")
                .WithParam("address", "EQ..."))
            .RespondWith(Response.Create()
                .WithStatusCode(200)
                .WithBody(@"{""result"": ""1000000000""}"));

        // Act
        var balance = await _client.GetBalanceAsync("EQ...");

        // Assert
        balance.Should().Be(1_000_000_000);
    }
}
```

---

## 安全检查表

**对于加密集成后端：**

- [ ] Webhook 签名通过恒定时间比较进行验证
- [ ] 私钥存储在保管库中（绝不在配置文件中）
- [ ] 对所有公共端点进行速率限制
- [ ] 对所有地址和金额进行输入验证
- [ ] 不同资产的小数精度处理
- [ ] 用于创建支付的幂等键
- [ ] 每个网络的交易确认阈值
- [ ] AML/KYC 集成以确保合规性
- [ ] 所有财务操作的审计记录
- [ ] 外部提供商调用的断路器
- [ ] 失败消息处理的死信队列
- [ ] 所有外部依赖项的健康检查

---

## 可观察性

**结构化日志记录：**

```csharp
public class PaymentService
{
    public async Task<Result<PaymentInfo>> ProcessPaymentAsync(ProcessPaymentRequest request)
    {
        using var scope = _logger.BeginScope(new Dictionary<string, object>
        {
            ["PaymentId"] = request.PaymentId,
            ["UserId"] = request.UserId,
            ["Amount"] = request.Amount,
            ["Currency"] = request.Currency
        });

        _logger.LogInformation("Processing payment");

        try
        {
            var result = await ProcessInternalAsync(request);

            if (result.IsSuccess)
                _logger.LogInformation("Payment processed successfully");
            else
                _logger.LogWarning("Payment processing failed: {Errors}", result.Errors);

            return result;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Payment processing exception");
            throw;
        }
    }
}
```

**指标：**

```csharp
public class CryptoMetricsService
{
    private readonly Counter<long> _paymentsProcessed;
    private readonly Histogram<double> _paymentDuration;

    public CryptoMetricsService(IMeterFactory meterFactory)
    {
        var meter = meterFactory.Create("Crypto.Payments");

        _paymentsProcessed = meter.CreateCounter<long>(
            "crypto.payments.processed",
            description: "Number of payments processed");

        _paymentDuration = meter.CreateHistogram<double>(
            "crypto.payments.duration",
            unit: "ms",
            description: "Payment processing duration");
    }

    public void RecordPaymentProcessed(Currency currency, PaymentStatus status)
    {
        _paymentsProcessed.Add(1,
            new KeyValuePair<string, object?>("currency", currency.ToString()),
            new KeyValuePair<string, object?>("status", status.ToString()));
    }
}
```
