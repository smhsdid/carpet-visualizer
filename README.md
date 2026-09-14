# Carpet Visualizer

一个用于将地毯设计稿转换为实物效果图的 Codex skill。

当前版本面向设计评审和材质筛选，输出：

- 材质细节图（material detail）
- 完整产品图（product overview）

skill 会将当前设计稿作为图案与颜色的权威来源，将真实材质参考用于纱线、织法、密度、起伏和边缘效果，并通过质量门槛检查图案拓扑、材质一致性和颜色泄漏。

## 当前状态

开发中。当前内置默认材质为低矮型提花织物 `jacquard-01`，生成结果仅用于视觉样品，不替代实物打样或生产确认。

## 目录

- `SKILL.md`：skill 主说明
- `agents/openai.yaml`：Codex skill 元数据
- `references/`：材质档案、提示词模板、质量标准和研究笔记
- `assets/material-library/`：可复用的真实材质参考及中性派生图

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

## 许可与素材

仓库中的材质图片用于 skill 测试和视觉校准。使用或发布前，请确认图片与设计稿的授权范围。
