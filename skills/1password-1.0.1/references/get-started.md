# 1Password CLI入门（摘要）

- 适用于macOS、Windows和Linux。
  - macOS/Linux shell ： bash、zsh、sh、fish。
  - Windows shell：PowerShell。
-需要1个密码订阅和桌面应用程序才能使用应用程序集成。
- macOS要求：Big Sur 11.0.0或更高版本。
- Linux应用程序集成需要PolKit +身份验证代理。
-根据操作系统的官方文档安装CLI。
-在1Password应用中启用桌面应用集成：
  -打开并解锁应用程序，然后选择您的账号/收藏。
  - macOS ：设置>开发人员>与1Password CLI集成（Touch ID任选）。
  - Windows ：打开 Windows Hello ，然后依次打开“设置” > “开发人员” > “集成”。
  - Linux ：“设置”>“安全”>“使用系统身份验证解锁”，然后“设置”>“开发人员”>“集成”
-集成后，运行任何登录命令（例如在docs: PH0中）。
-如果有多个账号：使用 PH1 选择一个账号，或使用 PH2 / PH3 。
- 对于非集成身份验证，请使用“op account add”。