# Deck Builder（幻灯片构建器）

把任意素材变成一份可演示的幻灯片：从笔记、网址、文档、代码到一个粗略的想法，产出**演示主线、生产 prompt、视觉方向、配图、演讲备注**，以及一份成品 deck。

这是一个面向 [Claude Code](https://docs.claude.com/en/docs/claude-code) / [Codex](https://github.com/openai/codex) 的 **skill（技能）**。

---

## 这是什么

`deck-builder` 是一个**编排型 skill**：它本身不直接渲染幻灯片，而是先把素材梳理成一条清晰的演示主线，再把具体的制作工作路由给已安装的下游工具去完成。

换句话说，它负责「想清楚这份 deck 要讲什么、怎么讲、长什么样」，然后调度合适的工具把它真正做出来。

## 能做什么

- **吃进各种素材**：粘贴的笔记、文件 / 文件夹、网址、代码、转录稿、PDF、文档，或已有的旧 deck。
- **提炼演示主线**：找到核心冲突 / 决策 / 转变 / 教学弧线，搭出一条「有锋芒的主线」，而不是流水账式的内容摘要。
- **生成任务专属的生产 prompt**：明确受众、目的、输出格式、长度，以及选用的工具路线。
- **输出幻灯片大纲**：每页包含版式、标题、精炼文案、视觉方案、演讲备注。
- **给出视觉方向与配图计划**：按内容（产品 / 技术 / 战略 / 研究 / 品牌故事）选择合适的视觉系统，逐页规划配图角色，并在有图像工具时直接生成。
- **产出成品**：优先生成自包含的 HTML deck；需要可编辑的 PowerPoint 时使用 PPTX 工具；也支持「只要一份可复用的 prompt」的纯 prompt 模式。

## 工作流程

1. **Ingest（吸收素材）** — 先读用户给的原始素材，只在缺少关键信息时追问最少的问题（受众、目的、时长、输出格式、品牌约束）。
2. **路由到真实工具** — 根据任务选择下游 skill 来真正干活，而不是凭记忆复刻它们的行为。
3. **提炼演示主线** — 找到这份 deck 的「论点」，搭出 slide spine。
4. **生成生产 prompt** — 写一份点名了具体工具路线的、任务专属的生产 brief。
5. **构建幻灯片大纲并产出** — 逐页给出版式、文案、视觉方案、演讲备注，并在交付前做质量校验。

幻灯片数量参考：短讲解 5–8 页；多数演讲 / pitch / 战略 deck 8–12 页；素材很密或用户要求深度时才用 12–20 页。

## 依赖的下游 skill（可选）

下面这些 skill **装上后会被自动调用**；没装时 `deck-builder` 会显式说明缺失并降级处理，而不会假装知道它们的行为：

| Skill | 作用 |
| --- | --- |
| `humanize-ppt` | 把原始素材变成大纲 / AST / 幻灯片计划 / 路由方案的「导演」 |
| `guizang-ppt-skill` | 中文 PPT 生产：杂志风 / 瑞士风、横向翻页 HTML deck、配图、封面 |
| `humanizer-zh` | 仅用于中文文案去 AI 味、润色（不负责排版或大纲） |
| `frontend-slides` | 通用 HTML deck 生产，覆盖上面没覆盖到的路线 |

## 如何安装

把本仓库克隆到你的 skills 目录即可。

**Claude Code：**

```bash
git clone https://github.com/HannibalLeo/deck-builder.git ~/.claude/skills/deck-builder
```

**Codex：**

```bash
git clone https://github.com/HannibalLeo/deck-builder.git ~/.codex/skills/deck-builder
```

安装后，当你让 AI「做个 PPT / 幻灯片 / pitch deck」「把这些材料做成演示文稿」「生成一份做 PPT 的 prompt」时，这个 skill 就会被触发。

## 如何使用

直接用自然语言描述需求即可，例如：

> 用 deck-builder 把这份材料做成一份给投资人看的 pitch deck，要有大纲、配图和可运行的 deck。

## 文件结构

```
deck-builder/
├── SKILL.md            # skill 主体：触发条件、完整工作流、工具路由、质量标准
└── agents/
    └── openai.yaml     # Codex / OpenAI 的接口配置（显示名、默认 prompt）
```
