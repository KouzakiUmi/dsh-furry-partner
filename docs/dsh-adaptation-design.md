# DSH 独立接入架构

[文档入口](README.md) · [身份迁移](runtime-identity.md) · [历史设计](history/dsh-adaptation-design-before-identity-migration.md)

本仓库只提供 DSH 产品。lib/index.js 为 Host，lib/client.js 为生成的浏览器模块；两者身份均为 dsh-furry-partner，客户端插件为 dsh-furry-partner/client，Cordis id/name 同名。生产包无其他宿主入口、安装器或 SDK。

## 数据流

Host 注册 /api/dsh-furry-partner/ 下的资源和设置接口，并按 persona 开关向 system-prompt/assemble 插入 dsh-furry-partner:persona。Client 订阅实际会话，lib/dsh-session-observer.mjs 负责选择会话和读取快照，lib/dsh-bridge.mjs 把 DSH turn/tool/live-chunk 等事件转为本地活动状态。lib/activity.mjs 维护真实事实和交互；lib/approved-motion.mjs 选择完整动作及可见时钟。

Client 源位于 lib/dsh-client-source.js，由 scripts/build-dsh-client.mjs 生成 lib/client.js。构建同时写入 dsh-furry-partner 模块 ID 和插件名；设置面板注册在 plugins.bundle.config:dsh-furry-partner。源码和生成物都必须测试。

## 资源与状态边界

29 个完整片段来自本仓库冻结素材，索引格式与高清帧各有自己的校验和。普通最短展示从首帧可见起算，工具结果即时结束真实状态；2000ms 工具间隙和显示驻留不伪造工具仍在执行。等待、回答、取消、报错、会话切换和显式互动有相应抢占规则。双片段缓存和加载截止有界，不排过期动作队列。

lib/dsh-companion.mjs 管理本地陪伴与抚摸，lib/dsh-presentation.mjs 管理显示几何；它们不提交模型请求或改写输入。浏览器偏好使用现有 dsh-furry-partner:*:v2 键。Host 的 config.json 相对包根目录读取，升级前保留备份。

## 验证与发布

npm run build 重建客户端；npm test 验证真实模块注册、全部新路由、设置面板、会话跟随、动作、互动及来源记录；npm run pack:release 回读每个包条目。v<版本> 必须匹配 package.json，Release 只包含 DSH 包、校验与报告。未发布版本不冒充可下载附件。

原始文件哈希保留在 SOURCE-PROVENANCE.json；授权改名后的代码绑定独立当前哈希。被移出运行时的旧系统提示词保留在 docs/history/source-prompts/，不加载或打包。素材、palette、alpha、锚点、时序和批准记录不因重命名而修改。
