# 早期开发与发布流程：历史发布记录

[当前说明](../node-development-plan.md) · [历史索引](README.md)

本文按功能保留原始发布证据。记录中的「当前」「最新」「未发布」「待验收」仅指原记录形成时的状态，不能替代当前说明或新的验收记录。旧流程和旧接口描述不是现行使用指引；重复正文合并并保留来源。整理日期：2026-10-15。

## 历史片段 1

原位置：[FORK_FEATURES.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/FORK_FEATURES.md)。

---

# Marzban-Node 开源扩展功能

## 历史片段 2

原位置：[FORK_FEATURES.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/FORK_FEATURES.md)。

---

## 当前扩展

- 已有认证的 REST `/health` 和 RPyC 通道向 Marzban 主面板返回节点运行指标；新增 `device-policy-v1`、`xray-user-stats-v1` 能力标识，不新增公网监控端口。优先查询核心在线用户，旧核心尽力回退到近期流量；来源与 scope 单独标注。见 [活动与策略合同](../activity-and-policy.md)。
- REST `/device-activity` / `/device-policies` 与 RPyC 配对方法提供活动采样及原子策略快照接收，返回数量、revision、同步时间和执行范围。策略不含用户代理凭据、HWID 或 IP；配对主面板通过既有 Xray 控制通道另行同步每个 HWID 的设备账号，Node 重启后从生成配置加载这些账号，支持新连接凭据拒绝。
- 从主面板配置中读取可选的 `marzban_node_extensions` 扩展，每个 Node 最多接受一条住宅 IP 出站，并转换为 Xray HTTP/SOCKS 出站。普通官方配置没有扩展时行为不变。
- 路由保留管理员已有的具体规则优先；默认住宅出口位于兜底规则之前。HTTP 默认出口只匹配 TCP，避免把 UDP 送入不支持的协议。
- 核心重启前运行 Xray 配置预检；预检失败不会先停掉当前核心。配置错误不在日志中输出代理密码。

当前尚未实现住宅代理连通性健康检查、故障摘除或自动故障回滚，以及实时在线设备数统计。`reject_new` 的设备账号加载链已在本地开发版实现：Node 接受主面板为已登记 HWID 下发的独立 Xray 凭据，同时保留主面板要求的共享兼容账号，不自行保存原始 HWID。没有 `X-HWID` 的客户端由主面板返回共享订阅；因此无法获得 HWID 限额保证。已有旧配置不会被 Node 主动踢下线。仍须配对镜像与真实 Linux 节点验收，不能把本地测试写成已部署。

## 历史片段 3

原位置：[FORK_FEATURES.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/FORK_FEATURES.md)。

---

## 本地验证

运行 `python -B -m unittest discover -s tests -v`。若安装了 Xray 二进制，设置 `XRAY_TEST_BINARY` 为其绝对路径后重跑测试，会额外验证 HTTP/SOCKS 有认证和无认证的 4 种最终 Xray 配置。

## 历史片段 4

原位置：[FORK_FEATURES.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/FORK_FEATURES.md)。

---

## 跨仓库登记

当前可依赖的 REST/RPyC 通道、健康快照和 `marzban_node_extensions` 配置合同，
以 [`../09-接口登记索引.md`](https://github.com/kissow/Marzban/blob/master/MR_SHAW_API_AND_RELEASE.md) 为唯一索引；不要仅凭本文件
新增接口。变更时同时更新主面板的接口说明、scripts 的命令合同、CHANGELOG、
测试证据和 [`../08-跨仓库更新登记模板.md`](https://github.com/kissow/Marzban/blob/master/docs/REPOSITORY_UPDATE_FLOW.md)。
安装命令、证书、服务端口、数据目录或镜像来源发生变化时，必须增加升级、回退和
服务器验收记录；若没有变化，也要明确写出“无变化”。

## 历史片段 5

原位置：[CHANGELOG.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/CHANGELOG.md)。

---

# Mr.shaw Marzban-Node Fork 更新记录

## 历史片段 6

原位置：[CHANGELOG.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/CHANGELOG.md)。

---

## 2026-10-15 文档导航整理

README仅保留产品介绍、安装及文档导航；历史发布与检测记录迁入[历史归档](../README_RELEASE_HISTORY.md)，现行使用、协议及发布证据从[文档中心](../README.md)进入。更新维护规则，后续不再把维护日志放到首页。原安装命令、上游署名及许可证保留；仅文档，无运行时、API或镜像变化。配对文档导航/证据保留检查118项通过。

## 历史片段 7

原位置：[CHANGELOG.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/CHANGELOG.md)。

---

## 开发中（尚未发布）

- 通过既有认证 REST/RPyC 通道向主面板提供节点 CPU、内存、磁盘和运行时间，不新增监控端口。
- 支持主面板下发的单条 HTTP 或 SOCKS5 住宅代理出口；每个 Node 最多一条。
- 具体路由规则优先于默认住宅出口；HTTP 出口只承接 TCP，UDP 保持原路由。
- Xray 重启前先验证新配置；验证失败时不先停止正在运行的核心。日志不输出住宅代理密码。
- （历史阶段记录）直接连接设备数量限制尚未实现；当时本地开发版只有用户策略元数据接收，订阅 HWID 限制由配对主面板执行。该阶段已被上方“设备账号加载链”取代，不代表当前实现。

发布时须记录与 `kissow/Marzban` 的配对版本，并完成真实 Linux 节点联调。

## 历史片段 8

原位置：[CHANGELOG.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/CHANGELOG.md)。

---

## 文档与接口登记规则

- 所有 REST/RPyC 方法、健康快照字段、`managed-outbounds-v1` 能力、
  `marzban_node_extensions` 配置字段和 Xray 预检行为，必须同步登记到
  [`../09-接口登记索引.md`](https://github.com/kissow/Marzban/blob/master/MR_SHAW_API_AND_RELEASE.md)。
- 同一提交必须更新本文件、[`FORK_FEATURES.md`](../../FORK_FEATURES.md)、
  [`RELEASE_CHECKLIST.md`](../../RELEASE_CHECKLIST.md)、Node 开发计划和配对的
  Marzban/Marzban-scripts 文档；仅 UI 或文档变更也要写明运行时接口无变化。
- 发布记录必须包含三仓库 commit、Actions run、GHCR 镜像 digest、Xray 版本、
  备份位置、配对最低版本和服务器验收结果。未完成的接口只能标记为开发中。

## 历史片段 9

原位置：[RELEASE_CHECKLIST.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/RELEASE_CHECKLIST.md)。

---

# Marzban-Node 发布清单

## 历史片段 10

原位置：[RELEASE_CHECKLIST.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/RELEASE_CHECKLIST.md)。

---

## 变更登记

- [x] 已记录 Node commit、配对主面板 commit、脚本 commit、分支和发布状态。
- [x] 已标记是否修改认证 REST/RPyC 通道、能力标识、配置字段、Xray 核心、证书、服务端口或 API 端口。
- [x] 已明确旧版 Node 的兼容行为；不新增公网监控端口，不覆盖证书和现有数据卷。
- [ ] 没有提交 `_patch-node.tmp`、日志、证书私钥、Token、代理密码或生产配置。

## 历史片段 11

原位置：[RELEASE_CHECKLIST.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/RELEASE_CHECKLIST.md)。

---

## 协议和配置

- [x] 新增或修改的 Node 方法、请求、响应、错误和能力标识已同步到主面板接口文档及 CHANGELOG。
- [ ] Xray 配置有 JSON 预检；失败时不会先停止当前核心，失败日志不泄露密码。
- [ ] HTTP/SOCKS 出站的 TCP/UDP 路由、认证、DNS、恢复直连和删除出站行为有测试。
- [ ] 如果只改 Node 文档或脚本，明确写出主面板通道和运行时无变化。

## 历史片段 12

原位置：[RELEASE_CHECKLIST.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/RELEASE_CHECKLIST.md)。

---

## 测试

- [ ] `python -B -m unittest discover -s tests -v`
- [ ] 已用配套 Xray 二进制验证核心版本和最终 JSON；正式基线当前为 `v26.3.27`。
- [ ] 已测试健康快照、过期/离线、重连、配置失败回滚和多 Node 隔离。
- [ ] 已测试 Node 证书、服务端口、API 端口、订阅和原有入站功能不受影响。
- [ ] 已在隔离 Linux Node 与主面板完成真实认证联调，再决定是否进入正式镜像。

## 历史片段 13

原位置：[RELEASE_CHECKLIST.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/RELEASE_CHECKLIST.md)。

---

## CI、镜像和发布

- [x] GitHub Actions 成功，记录 run ID、源 commit、架构和失败重试结果。
- [x] `ghcr.io/kissow/marzban-node` 的 tag/index digest 和 OCI revision 与预期 Node commit 匹配。
- [x] 主面板需要同步发布时，两个仓库的配对 SHA、协议兼容范围和升级顺序已记录。
- [x] `CHANGELOG.md`、`FORK_FEATURES.md`、README、开发计划和项目验收清单状态一致。

## 历史片段 14

原位置：[RELEASE_CHECKLIST.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/RELEASE_CHECKLIST.md)。

---

## 服务器验收与回滚

- [ ] 每台 Node 更新前备份证书、Compose、配置和数据目录，记录位置和校验。
- [ ] 官方旧安装只执行 `adopt`；已切 Fork 的 Node 只执行 `update`；新 Node 才执行 `install`。
- [ ] 更新后验证 `marzban-node status`、日志、Xray 实际版本、主面板连接、节点订阅和出站公网 IP。
- [ ] 明确回滚镜像/tag 和配置恢复方式；不删除 `/var/lib/marzban-node`，不重建证书。

## 历史片段 15

原位置：[RELEASE_CHECKLIST.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/RELEASE_CHECKLIST.md)。

---

## 发布记录最小字段

```text
Node commit：
配对主面板 commit：
脚本 commit：
Actions run：
GHCR index/架构 digest：
OCI revision：
能力标识与协议版本：
Xray 版本：
真实 Node 验收：
已知限制与回滚方式：
```

## 历史片段 16

原位置：[docs/node-development-plan.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/docs/node-development-plan.md)。

---

# Marzban-Node 开源扩展开发边界

文档分工：README及各语言README保持产品介绍、安装/使用和简洁导航；不堆叠发布编号、测试过程、SHA、Actions、镜像摘要或验收日志。功能变更更新对应docs专页，摘要写CHANGELOG，接口写接口文档，发布证据写发布页；README仅在产品介绍/使用入口变化时调整。保留上游署名与许可；旧记录迁移保留历史并修正相对链接。

[文档中心](../README.md) · [历史首页记录](../README_RELEASE_HISTORY.md)

## 历史片段 17

原位置：[docs/node-development-plan.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/docs/node-development-plan.md)。

---

## 基线与协作

本仓库是 Mr.shaw 维护的 `Gozargah/Marzban-node` Fork，历史基线为 `607cb4d2c94019219ab91a8df5eeed1ff49b1ecf`。对应面板仓库为 `kissow/Marzban`，历史基线为 `7f396db3e703d71a28060bc9ce4a532ec64cb1f4`。保留原项目历史和 AGPL-3.0 许可证；`kissow/Marzban-node/master` 是正式发布分支，临时配对分支合并后删除。

## 历史片段 18

原位置：[docs/node-development-plan.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/docs/node-development-plan.md)。

---

## 三项功能的节点侧调查

1. **逐节点状态**：先核对现有节点与面板的通信、认证、心跳和状态数据，再定义最小健康快照及时间戳。优先复用现有安全通道，不默认开放新端口；旧节点须保持兼容。
2. **设备限制**：确认节点实际能观测到哪些连接标识及其生命周期，评估共享 IP、NAT、重装客户端和漫游导致的误判。先审计、告警，再考虑可回退的阻断。
3. **住宅 IP 出站**：核对 Xray 能力、面板下发配置与节点应用路径；代理凭据不得写入日志或仓库，灰度失败必须能回到原出站。

## 历史片段 19

原位置：[docs/node-development-plan.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/docs/node-development-plan.md)。

---

## 联调门槛

面板 API 与节点协议分别验证。记录面板 SHA、节点 SHA、协议兼容范围和回滚方式；测试节点验收后再讨论生产部署。原作者仓库仅作历史参考；如需参考外部代码，必须人工审阅后合入隔离分支，禁止自动“同步分支”或强推覆盖 Mr.shaw 的正式发布分支。第三方项目如需使用指标，应独立调用 Marzban 的受保护 API，不属于本仓库开发范围。

## 历史片段 20

原位置：[docs/node-development-plan.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/docs/node-development-plan.md)。

---

## 接口与发布登记

节点开发涉及的 REST/RPyC 方法、健康快照、能力标识、住宅出口配置合同和失败
行为，统一登记在 [`../../09-接口登记索引.md`](https://github.com/kissow/Marzban/blob/master/MR_SHAW_API_AND_RELEASE.md)。每次
改动还要同步填写 [`../../08-跨仓库更新登记模板.md`](https://github.com/kissow/Marzban/blob/master/docs/REPOSITORY_UPDATE_FLOW.md)，
并在主面板、Node、scripts 的 CHANGELOG 和发布清单中记录配对 commit、最低兼容
版本、Actions/GHCR 证据、Xray 版本、备份和服务器验收。仅 Node 内部重构也要
说明主面板 API、Node 通道、证书、端口、数据库和脚本命令是否无变化。

标准顺序是：先登记影响矩阵，再改代码和合同；本地测试与 `git diff --check`；
CI 构建并记录镜像 digest；隔离服务器执行 `install`/`adopt`/`update` 对应场景；
最后才把“开发中”改为“已发布”。
