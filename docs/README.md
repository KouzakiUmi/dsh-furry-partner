# DSH 文档入口

- [中文首页](../README.md) / [English](../README.en.md)：版本 2.5.1-preview.8、构建和安装。
- [身份与升级迁移](runtime-identity.md)：当前标识、API、Cordis 和设置键。
- [架构与接入](dsh-adaptation-design.md)：独立 Host、Client、事件桥和动作核心。
- [桌宠互动](dsh-companion-interactions.md)、[显示标定](dsh-display-calibration.md)、[标题图](dsh-branding.md)：各自功能与验收边界。
- [历史设计](history/dsh-adaptation-design-before-identity-migration.md) 与 source-prompts：仅作来源记录，不是当前安装说明。

2.5.1-preview.8 已作为预发布 Release 提供 `dsh-furry-partner` 包；尚未发布到 npm。CI 在 main 验证，推送 `v<package版本>` 标签由 [release.yml](../.github/workflows/release.yml) 重建产物并创建 Release，与原项目的 hd-v / v 发布规则分开。
