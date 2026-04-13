# 请求示例

## 请求示例

### 创建资源

```http
POST /api/users
Content-Type: application/json

{
  "email": "john@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "role": "admin"
}

Response: 201 Created
Location: /api/users/789
{
  "id": "789",
  "email": "john@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "role": "admin",
  "createdAt": "2025-01-15T10:30:00Z",
  "updatedAt": "2025-01-15T10:30:00Z"
}
```

### 更新资源

```http
PATCH /api/users/789
Content-Type: application/json

{
  "firstName": "Jonathan"
}

Response: 200 OK
{
  "id": "789",
  "email": "john@example.com",
  "firstName": "Jonathan",
  "lastName": "Doe",
  "role": "admin",
  "updatedAt": "2025-01-15T11:00:00Z"
}
```
