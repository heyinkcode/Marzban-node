# Marzban-Node 更新摘要

每项更新的合同、测试与发布证据放到对应功能文档；旧全文见[功能历史](docs/releases/README.md)。

## 2026-10-16

- 分开现行使用说明与历史开发/发布证据，修正中转订阅、能力及保存流程的旧阶段表述；仅文档，不改功能或镜像。[文档中心](docs/README.md)

## 2026-10-15

- 按功能整理文档、精简目录及协议入口；修正文档中设备独立账号与共享兼容账号的范围表述，不改运行时。
- 增加目标 Node 的出口连接检测、确认应用和失败恢复处理。[合同与发布证据](docs/egress-probe.md)

## 2026-10-08

- Node 可作为另一目标 Node 的中转来源，使用完整快照与精确 ACK。[合同](docs/node-relay.md)、[发布证据](docs/node-relay-release.md)

## 2026-10-03

- HTTP/SOCKS5 出口新增 DNS/UDP 模式。[合同](docs/egress-udp.md)、[发布证据](docs/egress-udp-release.md)
- 主控保留无 HWID 共享订阅兼容路径，Node 运行时无对应变化。[兼容边界](docs/activity-and-policy.md)

## 2026-10-02 及更早

- 增加活动查询、策略接收和设备独立凭据支持。[现行合同](docs/activity-and-policy.md)
- 固定核心基线与早期开发记录。[历史导航](docs/releases/README.md)

镜像发布与生产服务器验收分别记录，不据此宣称所有客户端/供应商已验证。
