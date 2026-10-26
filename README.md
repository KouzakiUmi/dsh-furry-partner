# DSH Furry Partner · 呜咪

[English](README.en.md) · [文档入口](docs/README.md) · [身份与升级迁移](docs/runtime-identity.md)

DeepSeek Harness（DSH）专用的呜咪全动态桌宠，提供中文／English 界面、29 个已批准动画片段（含待机与进出过渡变体）、真实工具与会话状态跟随、主动陪伴和可选角色口吻。当前源码版本 **2.5.1-preview.7**；尚未创建 Release，也未发布到 npm。

## 安装与升级

### 从本仓库构建包

```powershell
python -m pip install -r tools/requirements-validation.txt
npm run build
npm test
npm run pack:release
```

保存工作并退出旧插件后，安装生成的 tgz：

```powershell
dsh plugin --profile <profile> add "./dsh-furry-partner-2.5.1-preview.7.tgz"
```

桌面应用的 `desktop` profile 由应用自身独占管理（CLI 会拒绝该 profile），请在应用的插件页面安装本地包，不要使用上面的命令。

### 直接从 Git 安装

仓库已提交构建产物 `lib/client.js`，因此不必先构建；但仓库包含已批准的源素材，完整克隆约 1.8 GB：

```powershell
dsh plugin --profile <profile> add "github:KouzakiUmi/dsh-furry-partner"
```

安装后重新启动 DSH。默认仅提供插画全动态外观，旧像素设置归一化为插画。构建、测试和打包不会代你修改本机 DSH 配置或安装插件。

## 统一运行时命名

| 项目 | 当前值 |
| --- | --- |
| 仓库、包、Host、客户端模块 ID | `dsh-furry-partner` |
| 客户端插件名 | `dsh-furry-partner/client` |
| Cordis 条目 id / name | `dsh-furry-partner` / `dsh-furry-partner` |
| Host API 前缀 | `/api/dsh-furry-partner/` |
| 配置面板注册键 | `plugins.bundle.config:dsh-furry-partner` |
| 浏览器偏好 | `dsh-furry-partner:ui:v2`、`dsh-furry-partner:settings:v2` |

旧条目需停用后替换为本包的 Cordis 条目，不保留两份插件同时加载。Host 与 Client 要一起更新并重新加载；旧 API 不作为别名继续开放。已有 DSH 浏览器偏好键保持不变，文件配置请先备份。完整步骤见[迁移说明](docs/runtime-identity.md)。

## 开发与验证

使用 Node.js 24 和 Python。运行时不依赖其他宿主 SDK、相邻仓库或 work 历史目录。`npm run build` 从模块与源码生成 `lib/client.js`；不要手改生成文件。`npm test` 覆盖 Host／Client、会话跟随、动作时钟、失败反馈、原生互动、身份／路由及来源验证。`npm run pack:release` 生成独立 tgz、SHA-256 与逐项回读报告。

## 来源与版权

代码与文档为 Apache-2.0；呜咪素材按 [ASSET_LICENSE.md](ASSET_LICENSE.md) 保留全部权利。`SOURCE-PROVENANCE.json` 保留原始来源哈希；授权改名后的代码另绑定当前哈希，素材和批准记录不改写。文件中的原始仓库名称属于来源事实，不是运行时身份。未使用的旧宿主系统提示词保存在 `docs/history/source-prompts/`，不进入运行包。

本项目从 [原始项目](https://github.com/KouzakiUmi/pi-furry-partner) 独立维护；原资源版与终端 HD 的开发、安装及发布请查该项目。两个仓库不共享可变运行时代码。
