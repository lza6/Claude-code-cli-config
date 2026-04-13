# release minimal

将此用作首次公开发布的安全最小发布界面。

## 保留
- `技能.md`
- `参考文献/rules.md`
- `references/report-format.md`
- `references/file-roles.md`
- `参考文献/move-guidelines.md`
-`脚本/context_linter.py`

## 可选
- 仅当发布目标或存储库工作流程真正需要它们时才保留：
  - `自述文件.md`
  - `变更日志.md`

## 排除
- 工作区私有日志
- `内存/`
- `日志/审计/`
- `<openclaw-local-dir>/`
- `.venv*`
- `tmp/`
- 不相关的测试输出

## 规则
更喜欢从技能目录本身发布。保持第一个公共表面最小化，并仅在实际使用证明合理时才允许后续版本扩展。
