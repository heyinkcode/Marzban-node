# README 历史发布记录归档

2026-10-15 从产品首页迁入；保留历史发布、检测、镜像证据与维护流程，调整相对链接。下方未发布/current/latest为各日期原始快照，不代表当前版本。现行功能、发布与验收以[文档中心](README.md)、[更新记录](../CHANGELOG.md)和对应功能专页为准。

# Marzban-node

## MR-20261015-EGRESS-PROBE（配对镜像已发布，服务器验收待完成）

发布前验证：主控完整190/190两轮，应用专项8/8再三轮；Node完整80/80两轮，出口/真实核心恢复专项21/21再三轮（含真实子进程、TCP/UDP报文及固定Xray进程，无跳过）；前端60/60、TypeScript/Vite生产构建、pip check和固定入口diff检查通过。原组件HTML已展示，浏览器截图与两台生产服务器验收未执行。真实恢复测试额外发现旧核心进程/日志管道未回收，已修复并复跑；Windows夹具单独补SystemRoot，不修改Linux生产环境。

原出口弹窗新增目标 Node 连接检测，解析/TCP/HTTP或SOCKS5认证/HTTPS出口/DNS与UDP分阶段报告，5/10秒阶段上限、1/3轮、单Node一次、30秒总上限。四语言、原主题/宽度/账号密码/UDP模式保留。只测当前草稿，不保存或重启业务核心；停止等待不取消Node已启动的限时任务。不是客户端或中转整链验收，也不是测速/业务Xray探测。

主控新增sudo POST /api/node/{node_id}/egress/test；既有PUT/DELETE出口接口改为Node重启/API确认后才提交，失败保留保存值，Node启动失败尝试恢复旧配置，ACK丢失明确未确认且不盲目重发。Node新增认证REST /egress/probe、RPyC probe_egress与managed-egress-probe-v1能力。修复密码首尾空格被Node裁剪的问题。两仓库需配对更新；scripts无运行时变化，Xray v26.3.27、数据库迁移/证书/端口/用户/.env/数据卷无变化。

[合同、错误码、摘要证据与升级验收](egress-probe.md)。先更新使用出口检测的目标Node，再更新主控；scripts无运行时变化。

2026-10-15 发布证据：主控源789130c30a69a85708255154d0d4f6a24c573495，经PR #21合入258218c07c9f2e265e790764bd727e528dcb761d；Node源ce3bed0decccef70c70765f9f59936a8b6a78dc6，经PR #5合入168a9e63d7c5219dffafd5839876db30b57e3cd5。主控分支Actions38670782109、正式38671882097，Node PR38660291647/分支38660285441、正式38671875814均成功；两latest的index/双架构manifest/config摘要与OCI revision已核对。用户要求的额外一轮主控190/190、Node80/80、前端60/60、类型/生产构建/pip check也通过。仅文档[skip ci]回写不改变镜像运行时revision；服务器未更新/验收，不能据此宣称实际供应商或客户端已恢复。


## MR-20261008-NODE-RELAY-SOURCES（镜像已发布，服务器/视觉验收待完成）

连接方式采用原React/Chakra独立管理弹窗和原信息图标。可选择Marzban主服务器或另一台源Node中转到目标Node；保留原订阅别名、顺序、数量，只替换精确匹配的端点，不新增Relay。目标认证、设备凭据和出口不变。自转发/环路/占用/能力/精确ACK/失败回滚、来源隔离与恢复有回归测试。

管理API增加source/source_node_id/来源列表，additive迁移9012ab34cd56；Node新增managed-node-relay-v1、原认证REST/RPyC完整快照与独立转发进程。固定Xray26.3.27，原证书、控制/API端口、用户、.env与数据卷保留。首版VLESS TCP/RAW REALITY、IPv4/DNS-only入口、单跳选择，不是所有协议或任意UDP转发；每源512个配置不是吞吐承诺。

本地最终代码和独立发布副本再次复测：主控164/164、Node60/60（准备固定Xray，无跳过）、前端47/47、类型/生产构建、依赖/diff通过。干净Linux CI与两镜像双架构发布核对完成；真实跨服务器mTLS、公网吞吐、多引擎数据库、实际原组件UI截图仍待验收，不标稳定版。UI截图因浏览器策略blocked，未绕过。

主控revision 93bfbb5b17dd8ee731449976df1a4af4e0f57ca5，Actions37657985804；Node revision 7b45fc0dc3b4451045a06123b52ccdaaa5911b8d，Actions37657976968。scripts合并ed274ba82410f9e6f580cbec59b2a15a89ab81ea，Actions37657994843成功，脚本运行时不变。先在承担来源的Node运行marzban-node update，再在主控运行marzban update；仅作目标的既有配对Node不强制更新。新Node沿用仓库install，现在拉取新latest；旧机不重装、不删卷、不重复adopt。源业务入口TCP需放行，客户端刷新订阅。

[精确配对SHA、index/架构/config摘要、接口与SSH验收证据](https://github.com/heyinkcode/Marzban/blob/master/docs/NODE_RELAY_SOURCES_RELEASE.md)。下方旧记录只描述各自日期的阶段，不代替本轮最新状态；文档[skip ci]提交不改变已核对的运行时镜像revision。


> **Current release (2026-10-03, MR-20261003-EGRESS-UDP):** Paired panel/Node code and multiarchitecture latest images are published and OCI revisions verified. [Source SHAs, successful Actions and exact image digests](egress-udp-release.md). Server/provider/mobile/UI screenshot acceptance remains pending; this is not a stable-release claim. Update Node first, then panel. Scripts runtime, certificates, ports, volumes and pinned Xray v26.3.27 are unchanged. Legacy remains default. TCP-only DNS is not arbitrary UDP-to-TCP conversion. [Wire contract and acceptance](egress-udp.md).

> **Historical release (2026-10-03, HWID compatibility):** Source commit `c135743d1ad26d45538e4c6c7a65a9c6693856a8`, Actions `37090612247`, image index `sha256:21340918298f0b8647fb7eb360294334891fc219e280a75af5d133c66ee9fbc1`. Its runtime-unchanged note does not apply to the current UDP feature, which requires Node update. This historical digest is not current latest.

> **Mr.shaw community fork:** This repository preserves the upstream Marzban-Node project and adds node health reporting plus one managed HTTP/SOCKS outbound per Node. Read [Fork features](../FORK_FEATURES.md), the [Changelog](../CHANGELOG.md), and [`RELEASE_CHECKLIST.md`](../RELEASE_CHECKLIST.md). The current image includes online-user queries and device-policy acknowledgement/credential loading; [the contract and limitations](activity-and-policy.md) distinguish subscription registration from direct connection enforcement. The image is published and awaiting server acceptance.

Every Node code, protocol, Xray-core, configuration, UI-facing contract, or documentation change must be registered with the paired `kissow/Marzban` and `kissow/Marzban-scripts` records. The Node is not considered released until the protocol notes, paired commit, tests, Actions result, GHCR digest, and server acceptance status are recorded. If a change does not affect the Node channel, explicitly record that the channel, certificates, ports, and data are unchanged.

## Interface and release record

The canonical cross-repository interface list is [`../09-接口登记索引.md`](https://github.com/heyinkcode/Marzban/blob/master/MR_SHAW_API_AND_RELEASE.md).
Before changing a REST/RPyC method, health snapshot field, `marzban_node_extensions`
field, Xray preflight rule, certificate/port behavior, or installation command, update
that index, this README, `CHANGELOG.md`, and the paired Marzban and Marzban-scripts
records in the same change. The required change card and evidence fields are defined in
[`../08-跨仓库更新登记模板.md`](https://github.com/heyinkcode/Marzban/blob/master/docs/REPOSITORY_UPDATE_FLOW.md).

For every release, record the Node commit, paired panel commit, scripts commit, image
tag and GHCR digest, GitHub Actions run, fixed Xray version, protocol compatibility,
backup path, and server acceptance result. A UI-only or documentation-only change must
explicitly state that the Node channel, certificates, ports, data directories, and API
behavior are unchanged. Do not mark a release as published until the cross-repository
gate in the interface index is complete.
