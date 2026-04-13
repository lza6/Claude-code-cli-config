# 测试文档

这是一个测试 Markdown 文件，存在一些问题。

## 缺少图像替代文本

![](https://example.com/image.png)

## 线长

该行太长，应该会触发行长度警告，因为它超出了默认的 80 个字符限制相当多。

## 尾随空白

该行有尾随空格。

## 不一致的列表

- 第 1 项
* 第 2 项
- 第 3 项

## 没有语言的代码块

```
print("hello")
```

## 空链接

[空网址]()
[空文本](https://example.com)

## 重复的标头

# 测试文档

## 内部链接

[链接到不存在的锚点](#nonexistent)

## 外部链接

[好的链接](https://httpbin.org/status/200)
[错误链接](https://httpbin.org/status/404)