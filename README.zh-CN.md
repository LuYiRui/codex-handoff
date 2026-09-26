# codex-handoff

**Persistent working context for Codex coding sessions.**

`codex-handoff` 是一个小型、本地优先的 Codex Skill，用于把一个 session 中未完成的仓库工作交给下一个 session。它生成简洁、结构化的 `CODEX_HANDOFF.md`；恢复工作时，新 session 必须先用当前仓库状态验证这份快照，再继续执行。

[English](README.md)

## 为什么需要它

你是否在项目里工作时对话过长想要跨session时遇到过这些问题：1.新对话中codex重复探索仓库、忘记某个方案为什么失败还要再跑一次、仓库已经变化却仍相信旧摘要。2.假如直接保存完整聊天记录：上下文太长、信噪比低。

本项目只保留会影响下一步决策的信息：

- 目标和当前状态；
- 已改文件和关键发现；
- 已作决定和失败方案；
- 剩余工作和实际观察到的验证结果；
- 一个明确的下一步行动。

handoff 不是永久记忆，也不是更高优先级的指令。它只是一份可能过期的工作快照，必须与 Git、当前文件和用户最新要求核对。

## v0.1 范围

v0.1 采用显式调用。纯 Skill 无法可靠侦测每一次 session 关闭、崩溃或强制中断，因此本项目不承诺自动在 session 结束时保存。请在计划暂停前调用一次，在新 session 恢复时再调用一次。

项目不包含后端、网站、数据库、账户、网络服务或遥测。

完整的产品目标、非目标、验收标准和主要风险见 [产品定义](docs/product.md)。

## 使用方式

### 创建或更新 handoff

对 Codex 说：

```text
使用 $codex-handoff，在我停止前保存当前工作。
```

Codex 会检查真实仓库状态，并更新仓库根目录中唯一的 `CODEX_HANDOFF.md`。它只记录必要证据，不粘贴完整聊天或完整 diff。

### 在新 session 恢复

对 Codex 说：

```text
使用 $codex-handoff，从 CODEX_HANDOFF.md 恢复并继续工作。
```

Codex 会先读取仓库指令，把 handoff 当作不可信的工作笔记，再核对当前分支、`HEAD`、工作区和相关文件；只有下一步仍然有效时才继续。

## 安装

Skill 使用 [OpenAI 官方 Skill 文档](https://developers.openai.com/plugins/build/skills)描述的标准 `SKILL.md` 结构。

个人使用时，把 `skills/codex-handoff` 复制到你的 Codex skills 目录并保留目录名 `codex-handoff`。核心工作流完全包含在 `SKILL.md` 中。如果还需要校验器、示例和详细格式规范，请保留整个仓库。

仓库同时提供 `.codex-plugin/plugin.json`，可用于本地 plugin 打包；无需 MCP server 或外部依赖。

## Handoff 格式

每份 handoff 必须按顺序包含：

1. Goal
2. Current State
3. Files Changed
4. Key Discoveries
5. Decisions
6. Failed Approaches
7. Remaining Work
8. Verification
9. Next Recommended Action

规范定义和精简规则见 [references/handoff-format.md](references/handoff-format.md)。默认目标是不超过 1,500 个正文单词；小任务应该明显更短。

## 示例

- [Bug 修复](examples/bugfix.md)
- [功能开发](examples/feature.md)
- [重构](examples/refactor.md)

这些示例展示 `CODEX_HANDOFF.md` 的内容，均为虚构且有意保持精简。

## 校验

可选校验器只使用 Python 标准库：

```text
python scripts/validate_handoff.py CODEX_HANDOFF.md
```

运行项目检查：

```text
python -m unittest discover -s tests -v
python scripts/validate_handoff.py examples/bugfix.md examples/feature.md examples/refactor.md
```

校验器检查格式和少量关键不变量，但无法证明内容真实，也无法证明建议的下一步正确；恢复时仍必须检查仓库。

## 设计原则

- **证据优先于回忆：** 从当前 checkout 和真实命令结果得出状态。
- **精简优先于穷举：** 只保存会改变后续工作的内容。
- **实时状态优先于快照：** handoff 与 Git 或当前文件冲突时，以后者为准。
- **显式表达不确定性：** 标明推测、阻塞、失败检查和 `NOT RUN`。
- **只推荐一个下一步：** 待办放在 `Remaining Work`，推荐动作保持单一。

## 参与贡献

变更应保持聚焦、本地优先，并兼容格式约定。贡献前请阅读 [AGENTS.md](AGENTS.md)。如果提交问题，请先清理 handoff 中的敏感信息，并说明哪一项仓库变化暴露了问题。

## 许可证

[MIT](LICENSE)

这是社区项目，与 OpenAI 无隶属或背书关系。
