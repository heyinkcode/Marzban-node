# Node 到 Node 中转协议

说明源 Node 的认证控制通道、目标快照和透明 TCP 转发。设置通过[主控连接方式弹窗](https://github.com/kissow/Marzban/blob/master/docs/NODE_RELAY.md)完成，不改变目标出口或原客户端条目名称。

源 Node 接受主控通过原认证 REST/RPyC 下发的固定目标快照，使用已有 Xray v26.3.27 独立进程转发 TCP，不经过源住宅出口。目标 Node 继续使用原认证、设备凭据和出口。无需额外转发软件，监听归属检测使用镜像内的 psutil 5.9.4；不改原证书/控制/API端口、.env、数据目录或核心配置。必须放行源的业务监听 TCP端口。

能力 `managed-node-relay-v1` 在 health capabilities 与状态返回。REST POST `/relays/status` 接收 session_id；POST `/relays` 接收 session_id/profiles，原 TLS 客户端证书与会话认证继续生效，错会话403。RPyC `fetch_relay_status()`、`set_relays(JSON字符串)` 均经原 SSL连接，响应JSON字符串，嵌套列表/字典为普通值而非远程对象。

```json
{"profiles":[{"node_id":2,"listen_port":18443,"target_address":"node2.example.com","target_port":8443}]}
```

REST还需原session_id字段；RPyC只传profiles列表的JSON字符串。每profile只允许四个示例字段；node_id正整数且唯一，listen_port整数1024–65535且不占用，target_port整数1–65535，禁止bool冒充整数、URI/模板/回环目标及快照目标指向其中的中转端口。不接受任意Xray JSON或用户密钥。最多512目的地；主控单目标只配一个来源，不自动串联多跳，并做来源自身/环路校验。

状态返回capability/core_started/running/profiles/error/occupied_ports；写ACK返回capability/running/profiles/error。非空快照要求核心已启动；REST未启动409、输入422、进程应用失败409。RPyC相同情况抛明确异常。空列表清理，核心未启动仍可清理。Node验证JSON与固定Xray配置后替换；绑定失败尝试恢复旧进程。监听就绪只代表本地进程端口归属，不代表目标公网可达/客户端速度。

控制会话接管、断开、显式停止清理旧进程；源进程意外退出由主控周期检查后重下发数据库快照。服务/容器重启没有独立relay数据库，主控重连恢复。写超时可能实际已应用；主控恢复前通过状态核对，不盲目重放或广告新端点。原在线用户查询只统计源自身核心；透明转发用户在目标认证，不等于源Node新增物理设备或重复用户计费。

承担来源的 Node 需要支持 managed-node-relay-v1；已切 Fork 的来源服务器使用 marzban-node update，确认连接和能力后更新主面板。仅作目标的现有配对Node无新来源要求；原安装不能用重装/删卷更新。旧Node无能力时主控明确拒绝新的Node来源设置，主控来源/直连仍可使用。

[主控字段与隔离范围](https://github.com/kissow/Marzban/blob/master/docs/NODE_RELAY_SOURCES.md) · [链路测试](https://github.com/kissow/Marzban/blob/master/docs/NODE_RELAY_TESTING.md) · [历史配对发布证据](releases/node-relay-guide-20261015.md)

保留 Marzban、Marzban-Node 与 Xray 原作者及许可证；node_relay.py 复用本 Fork 主控模块。
