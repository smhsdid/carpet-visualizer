# Carpet Visualizer

一个将地毯设计稿转换为实物效果图的通用 agent skill，内置 Codex 适配层。

当前版本面向设计评审和肌理筛选，固定输出：

- 肌理细节图（`material_detail`）
- 完整产品图（`product_overview`）

skill 统一采用严格保留图案关系的生成目标：当前设计稿是图案与颜色的唯一权威来源，真实肌理参考只用于纱线、织法、尺度、起伏、光照反应和边缘效果。无论画稿复杂度如何，都使用同一套生成流程：先生成固定左下角细节图，做一轮轻量检查，再自动生成全貌图。

预览分支和用户确认环节不再作为流程条件。图像生成能力不可用时，输出完整的外部执行包；生成后的视觉偏差写入检查记录，不把“看起来差不多”描述为制造确认。

每次运行都保存实际提交给生图后端的最终提示词、有效参数、参考图顺序与哈希、源图哈希、输出路径和检查结果。

## 当前状态

开发中。当前内置默认肌理为用户确认、并由任务实拍校准的威尔顿平织 `wilton-flatweave-01`。档案只描述照片可见的纱束、细交织线、低起伏和包边，不额外宣称纤维、密度或织机设置。生成结果仅用于视觉样品，不替代实物打样或生产确认。

## 目录

- `SKILL.md`：skill 主说明
- `CAPABILITIES.md`：图像生成能力与统一执行方式
- `agents/openai.yaml`：Codex skill 元数据
- `adapters/`：Codex 和其他智能体的运行适配说明
- `references/`：肌理档案、威尔顿平织生成分支、图案保真规则、提示词模板、质量标准和研究笔记
- `scripts/prepare_design_controls.py`：生成确定性图案控制包，固定左下角
- `scripts/validate_topology.py`：校验源坐标结构证据
- `scripts/validate_paired_mappings.py`：校验配对映射素材
- `assets/material-library/`：可复用的真实肌理参考及中性派生图

## 研究笔记

参见 [`references/research-application-notes.md`](references/research-application-notes.md)。

## 通过 Codex 安装

将下面这句话直接发给 Codex：

> 请从 GitHub 仓库 https://github.com/smhsdid/carpet-visualizer 安装名为 `carpet-visualizer` 的 skill。仓库根目录就是 skill，使用 `main` 分支。

如果 Codex 要求指定仓库路径，使用：

```text
仓库：smhsdid/carpet-visualizer
路径：.
分支：main
安装名称：carpet-visualizer
```

安装完成后，要求 Codex 使用 `$carpet-visualizer` 处理地毯设计稿即可。安装是否可用仍取决于所在 Codex 产品、账号和工作区的 skill 安装权限；团队工作区也可以由管理员从公开 GitHub 仓库导入并同步插件市场。

## 在其他编程智能体中使用

不同智能体没有统一的 skill 安装标准，但本仓库的核心流程不依赖 Codex 工具名。将整个仓库提供给目标智能体，或将 `SKILL.md` 作为该平台的指令入口，并要求它读取 [`adapters/generic-agent.md`](adapters/generic-agent.md)。

建议使用下面这句启动：

> 阅读此仓库的 `SKILL.md` 与 `adapters/generic-agent.md`，使用 Carpet Visualizer 处理我提供的地毯设计稿。固定生成左下角肌理细节图，完成轻量检查后自动生成全貌图；如果当前环境不能生成图片，请输出完整的外部执行包，不要声称已经生成。

`agents/openai.yaml` 只为 Codex 服务；肌理规则、提示词模板和质量标准以根目录 `SKILL.md` 与 `references/` 为唯一来源。

## 许可与素材

仓库中的肌理图片用于 skill 测试和视觉校准。使用或发布前，请确认图片与设计稿的授权范围。
