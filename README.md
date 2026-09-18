# Carpet Visualizer

一个将地毯设计稿转换为实物效果图的通用 agent skill，内置 Codex 适配层。

当前版本面向设计评审和肌理筛选，输出：

- 肌理细节图（material detail）
- 完整产品图（product overview）

skill 会将当前设计稿作为图案与颜色的唯一权威来源，将真实肌理参考用于纱线、织法、尺度、起伏、光照反应和边缘效果。参考式语义生图默认记录为 `topology_mode: approximate`；只有具备独立结构控制和对齐证明时才使用 `exact`。生成流程会按后端能力选择本地可控策略或输出 `external_execution_required`，并把结构、肌理与局部修复分开记录。

## 当前状态

开发中。当前内置默认肌理为用户确认、并由任务实拍校准的威尔顿平织 `wilton-flatweave-01`。默认方向包括纵向梭形/椭圆纱束、尖端尾部穿入经纬线下方形成自然暗隙、统一低起伏织面，以及带近大远小收敛的真实人拍全貌视角。档案只描述照片可见的纱束、细交织线、低起伏和包边，不额外宣称纤维、密度或织机设置。生成结果仅用于视觉样品，不替代实物打样或生产确认。

## 目录

- `SKILL.md`：skill 主说明
- `AGENTS.md`：本仓库的技能开发约定、长期反馈规则和产物卫生规则
- `CAPABILITIES.md`：图像生成与编辑后端的能力约定和降级方式
- `agents/openai.yaml`：Codex skill 元数据
- `adapters/`：Codex 和其他智能体的运行适配说明
- `references/`：肌理档案、威尔顿平织生成分支、图案拓扑锁、提示词模板、质量标准和研究笔记
- `scripts/prepare_design_controls.py`：生成确定性图案控制包
- `scripts/validate_topology.py`：校验源坐标结构证明的区域与边界
- `assets/material-library/`：可复用的真实肌理参考及中性派生图

## 产物卫生

仓库只保存可复用的技能源码、引用、脚本、资产、适配器和 agent 元数据。生成图片、每次运行的 JSON/Markdown 记录、临时控制图和 Python 缓存放在仓库外的 Codex 数据/临时目录；`output/`、`outputs/`、`generated/`、`tmp/` 以及 `__pycache__/` 已加入忽略规则。历史运行产物如需保留，应放入仓库外的归档目录。

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

不同智能体没有统一的 skill 安装标准，但本仓库的核心流程不依赖 Codex 工具名。将整个仓库提供给目标智能体，或将 `SKILL.md` 与 `AGENTS.md` 作为该平台的指令入口，并要求它读取 [`adapters/generic-agent.md`](adapters/generic-agent.md)。

建议使用下面这句启动：

> 阅读此仓库的 `SKILL.md` 与 `adapters/generic-agent.md`，使用 Carpet Visualizer 处理我提供的地毯设计稿。先确认可用的图像能力；若当前环境不能生成图片，请输出完整的外部执行包，而不要声称已经生成。

`agents/openai.yaml` 和 `adapters/codex.md` 只为 Codex 服务；肌理规则、提示词模板和质量标准以根目录 `SKILL.md` 与 `references/` 为唯一来源。

## 许可与素材

仓库中的肌理图片用于 skill 测试和视觉校准。使用或发布前，请确认图片与设计稿的授权范围。
