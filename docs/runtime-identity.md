# DSH 运行时身份与迁移

从源码 2.5.1-preview.7 起，包、Host、Client 模块、Cordis 条目统一使用 dsh-furry-partner；客户端插件为 dsh-furry-partner/client。配置面板键为 plugins.bundle.config:dsh-furry-partner，提示词章节为 dsh-furry-partner:persona，缓存前缀为 dsh-motion-。

## 升级步骤

1. 保存工作，备份旧插件的 config.json、Cordis 配置和插件包；不要把两个包同时启用。
2. 停用旧组合包或旧独立包条目。旧 Cordis id 可能为 furry-partner，旧 Host／Client 身份为 pi-furry-partner；这些仅用于识别待移除的旧配置。
3. 安装新构建包，将旧条目替换为下面这一份；不是追加重复条目。
4. 如安装位置变化，将备份中的实际偏好迁移到新配置，保留一份原始备份。
5. 重新启动／重新加载 DSH Host 和 Client，确认只有一个桌宠和一个设置面板。

```yaml
- insert:
    - id: dsh-furry-partner
      name: dsh-furry-partner
```

## 路由与存储

以下相对路径均在 `/api/dsh-furry-partner/` 下：sheet、gesture、branding/title、config、hires/manifest、hires/frame、animated/catalog、animated/asset。客户端与 Host 同时切换；不开放旧路由别名。

同一浏览器来源下继续使用 dsh-furry-partner:ui:v2 和 dsh-furry-partner:settings:v2，不清空已有偏好。config.json 的默认文件位置仍相对插件包根目录。改名不改变动作、工具状态、时钟、素材或用户输入；未知配置字段也不擅自删除。

本次只修改代码与文档，没有代用户迁移本机配置、安装插件或发布新 Release。来源清单与历史提示词中的旧名称保留为证据，不参与模块注册或浏览器运行时。
