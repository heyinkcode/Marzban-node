# Marzban-Node 开源扩展功能

基于上游 Marzban-Node，保留历史、作者署名和许可证。安装见 [README](README.md)，设置由配对 Marzban 主控管理。

| 能力 | 范围 | 文档 |
| --- | --- | --- |
| 健康与活动 | 资源、活动来源、采样时间和策略 ACK；不是物理设备计数 | [活动与策略](docs/activity-and-policy.md) |
| 独立出口 | HTTP/SOCKS5 与 legacy/proxy/tcp_only UDP 模式 | [出口合同](docs/egress-udp.md) |
| 出口检测 | 目标 Node 的代理认证、HTTPS 和 DNS/UDP 检测；限时独立进程，不改业务配置 | [检测与安全应用](docs/egress-probe.md) |
| 中转来源 | 作为源 Node 透明转发到目标 Node，独立于源业务出口 | [中转合同](docs/node-relay.md) |
| 设备凭据 | 接收主控配置中的共享兼容账号和设备独立账号；不保存原始 HWID | [兼容边界](docs/activity-and-policy.md) |

Xray 固定 v26.3.27。扩展沿用原认证 REST/RPyC 与端口；新能力要按合同核对配对版本。透明中转当前为单跳 VLESS TCP/RAW REALITY 范围，不是任意协议或独立 UDP 中转。策略确认、监听成功或容器运行都不代表业务整链已验收。

[协议与开发边界](docs/node-development-plan.md) · [更新摘要](CHANGELOG.md) · [功能发布历史](docs/releases/README.md) · [发布检查](RELEASE_CHECKLIST.md)

使用与协议说明见[文档中心](docs/README.md)，旧阶段测试和发布证据见[对应历史索引](docs/releases/README.md)；文档整理不改变运行时。
