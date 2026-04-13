---
name: e2e-test-builder
description: E2E测试构建器 - 使用Playwright或Cypress为关键用户流程构建端到端浏览器测试。包括选择器策略、测试数据管理、页面对象和视觉回归测试。适用于"E2E测试"、"浏览器测试"、"Playwright"或"Cypress测试"。
---

# E2E 测试构建器

为关键用户流程构建可靠的端到端测试。

## Playwright 测试设置

```typescript
// playwright.config.ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html",
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
    {
      name: "Mobile Chrome",
      use: { ...devices["Pixel 5"] },
    },
  ],
  webServer: {
    command: "npm run dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
});
```

## 关键流程测试

```typescript
// e2e/checkout-flow.spec.ts
import { test, expect } from "@playwright/test";

test.describe("结账流程", () => {
  test.beforeEach(async ({ page }) => {
    // 导航到首页
    await page.goto("/");

    // 登录
    await page.getByRole("button", { name: "Login" }).click();
    await page.getByLabel("Email").fill("test@example.com");
    await page.getByLabel("Password").fill("password123");
    await page.getByRole("button", { name: "Sign In" }).click();

    // 等待仪表板
    await expect(page).toHaveURL("/dashboard");
  });

  test("应成功完成结账", async ({ page }) => {
    // 1. 浏览商品
    await page.getByRole("link", { name: "Products" }).click();
    await expect(page).toHaveURL("/products");

    // 2. 添加商品到购物车
    await page.getByRole("button", { name: "Add to Cart" }).first().click();
    await expect(page.getByText("Added to cart")).toBeVisible();

    // 3. 进入购物车
    await page.getByRole("link", { name: "Cart" }).click();
    await expect(page).toHaveURL("/cart");
    await expect(
      page.getByRole("heading", { name: "Shopping Cart" })
    ).toBeVisible();

    // 4. 进入结账
    await page.getByRole("button", { name: "Checkout" }).click();
    await expect(page).toHaveURL("/checkout");

    // 5. 填写配送信息
    await page.getByLabel("Full Name").fill("张三");
    await page.getByLabel("Address").fill("北京市朝阳区某某路123号");
    await page.getByLabel("City").fill("北京");
    await page.getByLabel("ZIP Code").fill("100001");

    // 6. 填写支付信息
    await page.getByLabel("Card Number").fill("4242424242424242");
    await page.getByLabel("Expiry Date").fill("12/25");
    await page.getByLabel("CVC").fill("123");

    // 7. 提交订单
    await page.getByRole("button", { name: "Place Order" }).click();

    // 8. 验证成功
    await expect(page).toHaveURL(/\/order\/\d+/);
    await expect(page.getByText("Order confirmed!")).toBeVisible();
    await expect(page.getByText(/Order #\d+/)).toBeVisible();
  });

  test("应显示空字段的验证错误", async ({ page }) => {
    // 导航到结账页
    await page.goto("/checkout");

    // 尝试不填写字段就提交
    await page.getByRole("button", { name: "Place Order" }).click();

    // 验证错误提示
    await expect(page.getByText("Name is required")).toBeVisible();
    await expect(page.getByText("Address is required")).toBeVisible();
    await expect(page.getByText("Card number is required")).toBeVisible();
  });

  test("应处理支付失败", async ({ page }) => {
    // 添加商品并进入结账
    await page.goto("/products");
    await page.getByRole("button", { name: "Add to Cart" }).first().click();
    await page.goto("/checkout");

    // 填写会失败的卡号
    await page.getByLabel("Card Number").fill("4000000000000002");
    await page.getByLabel("Expiry Date").fill("12/25");
    await page.getByLabel("CVC").fill("123");

    // 提交
    await page.getByRole("button", { name: "Place Order" }).click();

    // 验证错误消息
    await expect(page.getByText("Payment failed")).toBeVisible();
    await expect(page.getByText("Please try a different card")).toBeVisible();
  });
});
```

## 页面对象模式

```typescript
// e2e/pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto("/login");
  }

  async login(email: string, password: string) {
    await this.page.getByLabel("Email").fill(email);
    await this.page.getByLabel("Password").fill(password);
    await this.page.getByRole("button", { name: "Sign In" }).click();
  }

  async expectLoginSuccess() {
    await expect(this.page).toHaveURL("/dashboard");
  }

  async expectLoginError(message: string) {
    await expect(this.page.getByText(message)).toBeVisible();
  }
}

// e2e/pages/ProductPage.ts
export class ProductPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto("/products");
  }

  async addToCart(productName: string) {
    const product = this.page.locator(`[data-product="${productName}"]`);
    await product.getByRole("button", { name: "Add to Cart" }).click();
  }

  async expectProductVisible(productName: string) {
    await expect(
      this.page.getByRole("heading", { name: productName })
    ).toBeVisible();
  }
}

// 在测试中使用
test("应登录并添加商品", async ({ page }) => {
  const loginPage = new LoginPage(page);
  const productPage = new ProductPage(page);

  await loginPage.goto();
  await loginPage.login("test@example.com", "password123");
  await loginPage.expectLoginSuccess();

  await productPage.goto();
  await productPage.addToCart("MacBook Pro");
});
```

## 选择器策略

```typescript
// 首选选择器优先级：
// 1. 基于角色（最有弹性）
await page.getByRole("button", { name: "Submit" });
await page.getByRole("link", { name: "Products" });
await page.getByRole("textbox", { name: "Email" });

// 2. 基于标签（语义化）
await page.getByLabel("Email address");
await page.getByLabel("Password");

// 3. 测试 ID（用于复杂情况）
await page.getByTestId("user-menu");
await page.getByTestId("product-card-123");

// 4. 文本内容（用于唯一文本）
await page.getByText("Welcome back!");
await page.getByText(/Order #\d+/);

// ❌ 避免：CSS 选择器（脆弱）
// await page.locator('.btn.btn-primary');
// await page.locator('#submit-button');
```

## 测试数据管理

```typescript
// e2e/fixtures/test-data.ts
export const testData = {
  users: {
    admin: {
      email: "admin@example.com",
      password: "admin123",
    },
    customer: {
      email: "customer@example.com",
      password: "customer123",
    },
  },
  products: {
    laptop: {
      name: "MacBook Pro",
      price: 2499.99,
    },
    phone: {
      name: "iPhone 15",
      price: 999.99,
    },
  },
  cards: {
    valid: "4242424242424242",
    declined: "4000000000000002",
    insufficientFunds: "4000000000009995",
  },
};

// e2e/setup/seed-test-data.ts
export async function seedTestData() {
  const prisma = new PrismaClient();

  // 创建测试用户
  await prisma.user.upsert({
    where: { email: testData.users.customer.email },
    create: {
      email: testData.users.customer.email,
      password: await hash(testData.users.customer.password),
    },
    update: {},
  });

  // 创建测试商品
  await prisma.product.upsert({
    where: { name: testData.products.laptop.name },
    create: testData.products.laptop,
    update: {},
  });

  await prisma.$disconnect();
}
```

## 视觉回归测试

```typescript
// e2e/visual/homepage.spec.ts
test("首页应与截图匹配", async ({ page }) => {
  await page.goto("/");

  // 截取全页面截图
  await expect(page).toHaveScreenshot("homepage.png", {
    fullPage: true,
    maxDiffPixels: 100, // 允许微小差异
  });
});

test("商品卡片应与截图匹配", async ({ page }) => {
  await page.goto("/products");

  const productCard = page.locator('[data-testid="product-card"]').first();

  // 截取元素截图
  await expect(productCard).toHaveScreenshot("product-card.png");
});
```

## 移动端测试

```typescript
// e2e/mobile/checkout-mobile.spec.ts
test.use({ viewport: { width: 375, height: 667 } }); // iPhone SE

test("应完成移动端结账", async ({ page }) => {
  await page.goto("/");

  // 打开移动菜单
  await page.getByRole("button", { name: "Menu" }).click();
  await page.getByRole("link", { name: "Products" }).click();

  // 添加到购物车
  await page.getByRole("button", { name: "Add to Cart" }).first().click();

  // 继续结账
  // ...
});
```

## 网络模拟

```typescript
// e2e/mocked/payment-api.spec.ts
test("应处理支付 API 超时", async ({ page }) => {
  // 模拟慢速支付 API
  await page.route("**/api/payment", async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 5000));
    await route.fulfill({
      status: 200,
      body: JSON.stringify({ success: true }),
    });
  });

  // 继续结账
  await page.goto("/checkout");
  // ... 填写表单 ...
  await page.getByRole("button", { name: "Place Order" }).click();

  // 应显示加载状态
  await expect(page.getByText("Processing payment...")).toBeVisible();
});
```

## 最佳实践

1. **测试用户流程**：而不是单个组件
2. **使用基于角色的选择器**：更有弹性
3. **页面对象**：可复用且可维护
4. **等待元素**：不要使用固定延迟
5. **测试关键路径**：登录、结账、注册
6. **管理测试数据**：每个测试隔离
7. **视觉回归**：仅关键页面

## 输出检查清单

- [ ] Playwright/Cypress 已配置
- [ ] 关键流程已识别
- [ ] 页面对象已创建
- [ ] 选择器策略已定义（基于角色）
- [ ] 测试数据管理已设置
- [ ] 设置/清理钩子已配置
- [ ] 身份验证流程已测试
- [ ] 错误状态已测试
- [ ] 移动端视口测试已添加
- [ ] CI 集成已配置
