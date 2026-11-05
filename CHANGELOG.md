# DSH 更新记录

## 2.5.1-preview.9 · 2026-11-06

- 兼容声明适配 DSH 0.2.2-rc.1 的判定机制：旧 `dsh.compatibility.dshReleases` 逐版本表（0.2.1-alpha.1～0.2.1-rc.2）在新版宿主已无消费方，迁移为顶层 `engines.dsh: ">=0.2.1-alpha.1 <0.3.0"`。范围经宿主同版本 semver（7.8.5，`includePrerelease`）逐版本验证：覆盖旧声明全部版本、0.2.2-rc.1 与 0.2.x 后续，排除 0.3.0+。
- 移除与顶层 `engines.node: ">=22.19.0"` 矛盾的 `dsh.compatibility.node: ">=18"`；`manifestVersion`、`bundle`、`client` 等仍被消费的 manifest 字段保留。
- Host/Client 全部宿主契约在 0.2.2-rc.1 逐项核对一致（systemPrompt 服务、settings.configure、connection.fetch.register、system-prompt/assemble、客户端 slot、sessions/eventSource/输入壳/commandUi、会话事件与 chunk 字段）；npm test 27 组全过。

## 2.5.1-preview.8 · 2026-10-28

- 经用户授权，3048 帧 896px 高清帧由无损 WebP 重编码为有损 q90：该层 718 MB → 180 MB（4.00×）。alpha 通道与批准像素逐字节相同；可见区按 alpha 加权 PSNR 最低 35.6 dB、ΔE 最高 1.94。发布包 tgz 由 1.01 GB 降至 467 MB。
- 批准原件未丢失：`Hi-Res/` 保留冻结基线，`assets/animated/provenance/lossy-q90-reencode.json` 逐帧记录重编码前后的哈希与 PSNR。校验器改为先由基线重建批准像素再比对，并新增 `--check-gpu` 自证 GPU 路径与冻结实现逐位一致。
- 新增 `scripts/reencode-approved-hires.py`（重编码，含逐帧 alpha 校验）与 `scripts/sync-adapted-hashes.mjs`（改编文件哈希同步），允许在不丢失批准证据的前提下重复执行该流程。
- 已创建预发布 Release 并提供 tgz、SHA-256 与逐项回读报告；尚未发布到 npm。

## 2.5.1-preview.7 · 2026-10-27

- 按用户要求统一 Host、Client、Cordis、设置面板与缓存身份为 dsh-furry-partner，API 改为 /api/dsh-furry-partner/。
- Host 与 Client 同步更新，移除运行时旧宿主命名和未使用的提示精简辅助函数；角色口吻模板直接使用 DSH 身份。
- 保留 dsh-furry-partner:*:v2 浏览器偏好；旧 Cordis 条目需按迁移说明替换，未自动修改本机安装。
- 原素材与批准记录不变。来源清单保留原哈希并为授权适配代码绑定当前哈希，未使用系统提示词移至历史目录。
- 发布包不再包含两个运行时用不到的资源：休眠的 `umi-title-wave.webp`（`title.json` 标记 `qa.accepted: false`，加载器因此从不读取）与 `assets/animated/provenance/**`（批准证据链，仅测试读取）。两者仍保留在仓库。
- 已创建预发布 Release 并提供 tgz、SHA-256 与逐项回读报告；尚未发布到 npm。

## 2.5.1-preview.6 · 独立仓库基线

从原始项目分离 DSH 源码、构建、测试和分发包，保存源文件与素材哈希。该基线为兼容旧安装保留过旧 Host／Client 身份；此策略已由 preview.7 的显式命名迁移替代。
