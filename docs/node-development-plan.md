# Node 协议与开发边界

分发所有者迁为 heyinkcode，API/认证/端口合同无变化；[升级边界](GITHUB_NAMESPACE_MIGRATION.md)。

这是现行协议入口，不是发布日志。各次测试、SHA、Actions 和镜像证据见[功能发布历史](releases/README.md)及对应功能专页。

## 控制通道和业务流量

Node 沿用既有认证 REST 或 RPyC TLS 控制连接。主控用它下发配置、读取指标和接收确认，不使用 REST 搬运用户流量。Xray 固定 v26.3.27，保留证书、服务端口、Xray API 端口和数据目录，不新增公开监控端口。

## 扩展合同

| REST POST / RPyC 方法 | 合同和限制 |
| --- | --- |
| `/health` / `fetch_health()` | [健康、活动来源与采样时间](activity-and-policy.md) |
| `/device-activity`、`/device-policies` / `fetch_device_activity()`、`set_device_policies()` | [活动与完整策略快照](activity-and-policy.md) |
| `/egress/probe` / `probe_egress()` | [认证、限时检测、进程回收与脱敏](egress-probe.md) |
| `/relays/status`、`/relays` / `fetch_relay_status()`、`set_relays()` | [来源能力、完整快照、监听与精确 ACK](node-relay.md) |

HTTP/SOCKS5 出口由主控生成每 Node 的配置扩展，见[出口与 UDP](egress-udp.md)。新检测/安全应用需 managed-egress-probe-v1；Node 中转来源需 managed-node-relay-v1。旧节点的兼容或拒绝行为按各合同执行，不凭版本字符串猜测能力。

Node 只加载主控最终下发的账号配置；无 HWID 共享兼容账号仍保留。不能把策略 ACK、在线用户、IP、连接或设备登记数互相替代，也不能声称全部客户端受设备限额强制约束。

## 开发和发布

只修改隔离分支，保留用户数据与上游历史。新增协议须测试认证、旧版本、错误输入、超时、并发、ACK 丢失和恢复；真实固定核心测试与模拟测试分开记录。Node 作为来源的中转进程与业务核心隔离，但同一来源更新快照可能短暂影响其其他中转会话。

主控、Node、scripts 分别登记是否有运行时变化，按能力要求配对发布。普通单测、Linux 构建、双架构镜像核对和真实服务器验收是不同阶段。已有 Fork 使用 update，新机才 install，不重复 adopt 或删除数据卷。

[主控 API 索引](https://github.com/heyinkcode/Marzban/blob/master/MR_SHAW_API_AND_RELEASE.md) · [跨仓库流程](https://github.com/heyinkcode/Marzban/blob/master/docs/REPOSITORY_UPDATE_FLOW.md) · [本仓库发布检查](../RELEASE_CHECKLIST.md)

模式字段解析兼容与当前主控安全应用能力是两项检查；旧 Node 可继续已有业务，不表示支持新的检测/保存/删除流程。见[出口检测合同](egress-probe.md)。文档整理不改变 REST/RPyC、认证或运行时。
