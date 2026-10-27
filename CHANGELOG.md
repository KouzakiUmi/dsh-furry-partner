# DSH 更新记录

## 2.5.1-preview.7 · 2026-10-27

- 按用户要求统一 Host、Client、Cordis、设置面板与缓存身份为 dsh-furry-partner，API 改为 /api/dsh-furry-partner/。
- Host 与 Client 同步更新，移除运行时旧宿主命名和未使用的提示精简辅助函数；角色口吻模板直接使用 DSH 身份。
- 保留 dsh-furry-partner:*:v2 浏览器偏好；旧 Cordis 条目需按迁移说明替换，未自动修改本机安装。
- 原素材与批准记录不变。来源清单保留原哈希并为授权适配代码绑定当前哈希，未使用系统提示词移至历史目录。
- 发布包不再包含两个运行时用不到的资源，tgz 由 1.08 GB 降至约 1.01 GB：休眠的 `umi-title-wave.webp`（`title.json` 标记 `qa.accepted: false`，加载器因此从不读取）与 `assets/animated/provenance/**`（批准证据链，仅测试读取）。两者仍保留在仓库。
- 已创建预发布 Release 并提供 tgz、SHA-256 与逐项回读报告；尚未发布到 npm。

## 2.5.1-preview.6 · 独立仓库基线

从原始项目分离 DSH 源码、构建、测试和分发包，保存源文件与素材哈希。该基线为兼容旧安装保留过旧 Host／Client 身份；此策略已由 preview.7 的显式命名迁移替代。
