# Deck Builder：专业 PPT 制作技能

面向 Claude Code 和 Codex 的共享技能。用户说“做 PPT”时，默认交付真正的 PPTX；也保留明确指定的 HTML 演示和仅提示词模式。

## 方法

1. **先看参考的表达方式。** 同时读文字和渲染页，拆解层次、密度、图文比例、配色作用与机制图形式。
2. **先把关系讲清楚。** 每页明确问题、参与者、输入、处理、产出和必要的反馈，区分串行流程、并行应用和共享基础。
3. **按内容选择视觉。** 流程用机制图，证据用真实图表或截图，比较用对照结构。多个版本需要版式或表达策略的区别。
4. **按用途保留编辑能力。** 支持原生可编辑、可编辑正文搭配高清示意图，以及用户明确接受的图片版。不会把图片版宣称为全可编辑。
5. **检查真正交付的文件。** 分别验收内容逻辑、逐页渲染和文件结构，修正后重建并复查。

一次成功的方案汇报采用了“标题和建设逻辑、紧凑机制说明、主体信息图、底部成果句”的结构。这是参考驱动的一种模式；技能不会把所有主题强制做成蓝白工程图。

## 使用

Claude Code：

```text
/deck-builder 把这份材料做成 8 页 PPT，参考附件的表达形式，正文可编辑。
```

Codex：

```text
$deck-builder 重新设计这 4 页 PPT，先分析参考，补强逻辑和机制图。
```

也可直接说“用 deck-builder 做 PPT”。风格和范围足够清楚时直接制作；只有关键信息缺失才追问。

## 安装与共享

仓库地址：[HannibalLeo/deck-builder](https://github.com/HannibalLeo/deck-builder)。

只使用 Claude Code：

```bash
git clone https://github.com/HannibalLeo/deck-builder.git ~/.claude/skills/deck-builder
```

只使用 Codex：

```bash
git clone https://github.com/HannibalLeo/deck-builder.git ~/.codex/skills/deck-builder
```

macOS / Linux 上同时使用两端，可以将 Codex 目录作为实体目录，再让 Claude 指向它：

```bash
mkdir -p ~/.codex/skills ~/.claude/skills
git clone https://github.com/HannibalLeo/deck-builder.git ~/.codex/skills/deck-builder
ln -s ~/.codex/skills/deck-builder ~/.claude/skills/deck-builder
```

上面的命令用于目标目录尚不存在的首次安装。已有安装应先检查实际路径与本地修改，不覆盖现有目录。两端读取同一份技能后，只维护实体目录即可。安装后新开会话以刷新技能发现。

更新实体目录前确认工作区没有尚未保存的修改，再运行：

```bash
git -C ~/.codex/skills/deck-builder pull --ff-only
```

若仅安装在 Claude 目录，将上面的路径换成 `~/.claude/skills/deck-builder`。

共享的是流程和资料；Claude 与 Codex 使用各自可用的工具。本技能不会自动安装 PowerPoint 库、图像服务或渲染器，也不包含这些上游工具的实现。只读环境探测：

```bash
python3 ~/.codex/skills/deck-builder/scripts/preflight.py
```

探测只列出本地模块、运行时和渲染器，不安装依赖，也不代表已成功制作 PPT。仅在 Claude 目录安装时，替换为相应脚本路径。

## 调研与整合

已检查 8 组上游方案，覆盖图解型、HTML 型、原生 PPTX 型与工程验收型。保留其有价值的方法，使用原创说明整合，没有整体安装或复制上游实现。具体来源、版本、输出限制与许可证见 [source-review.md](references/source-review.md)。

## 文件导航

- [SKILL.md](SKILL.md)：主入口与完整流程
- [reference-driven.md](references/reference-driven.md)：参考分析、重设计和图解提示词
- [composition-playbook.md](references/composition-playbook.md)：按传播任务选择结构
- [pptx-production.md](references/pptx-production.md)：PPTX 制作与编辑能力合同
- [runtime-and-qa.md](references/runtime-and-qa.md)：跨端环境、中文字体、生成素材及验收
- [source-review.md](references/source-review.md)：上游研究及采用边界
- [scripts/preflight.py](scripts/preflight.py)：只读环境探测
