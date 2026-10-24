# DSH Furry Partner · 呜咪

DeepSeek Harness（DSH）专用的呜咪全动态桌宠，提供中文／English、完整动作、工具状态跟随和可选角色口吻。

本项目从 [pi-furry-partner](https://github.com/KouzakiUmi/pi-furry-partner) 独立维护。Pi 高清／全动态版与 Legacy 旧资源版继续由原仓库维护；本仓库不包含 Pi 扩展入口或 Pi 安装器。

## 安装与升级

下载本仓库 Release 的 `dsh-furry-partner-<版本>.tgz`，保存工作并退出 DSH 后，在附件所在目录安装：

```powershell
dsh plugin --profile desktop add "./dsh-furry-partner-<版本>.tgz"
```

重新启动 DSH。默认提供插画全动态外观；旧像素设置会迁移到插画。

仓库名和包名为 `dsh-furry-partner`，Cordis patch 的包引用也指向这个新名称。为兼容已安装版本，Host／Client 的内部插件 ID 仍为 `pi-furry-partner`，Cordis 行 ID 仍为 `furry-partner`，API 路径及设置存储键保持原样。升级时先停用旧组合包的 bundle，再启用本包，不同时启用两个相同行 ID 的包；保留配置和旧包作为回退。此拆分没有代你修改本机 DSH 配置。

## 开发与验证

需要 Node.js 24 和 Python。运行时不依赖 Pi SDK，也不需要相邻仓库或本机 work 历史目录。

```powershell
python -m pip install -r tools/requirements-validation.txt
npm run build
npm test
npm run pack:release
```

`npm test` 覆盖 DSH Host／Client、会话跟随、动作驻留、连续播放、失败反馈、开场与互动、资源来源及已批准色彩导数。打包生成独立 TGZ、SHA-256 和逐文件校验报告。CI 单独验证构建、测试与包；推送匹配 package 版本的 `v` 标签后走本仓库自己的发布流程。

## 资源、兼容与署名

当前动作与调度来自原仓库已恢复的高清／全动态基线，未引入 Legacy 的简单帧准备调度。源提交与复制文件哈希记录在 `SOURCE-PROVENANCE.json`；原始提交历史保留在来源仓库。

保留原项目贡献者署名，包括 [srcres258](https://github.com/srcres258) 的贡献。代码与文档遵循 Apache-2.0；角色、插画和动画素材按 `ASSET_LICENSE.md` 保留版权，拆分不改变授权。

English: this is the standalone DSH project. It retains existing internal plugin IDs and settings keys for upgrades, has no Pi SDK dependency, and builds/tests/packages independently. The original repository continues to maintain the Pi and Legacy products. See `SOURCE-PROVENANCE.json`, `LICENSE`, `NOTICE`, and `ASSET_LICENSE.md` for provenance and licensing.
