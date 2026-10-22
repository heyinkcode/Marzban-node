# 活动统计与策略：历史发布记录

[当前说明](../activity-and-policy.md) · [历史索引](README.md)

本文按功能保留原始发布证据。记录中的「当前」「最新」「未发布」「待验收」仅指原记录形成时的状态，不能替代当前说明或新的验收记录。旧流程和旧接口描述不是现行使用指引；重复正文合并并保留来源。整理日期：2026-10-15。

## 历史片段 1

原位置：[FORK_FEATURES.md](https://github.com/heyinkcode/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/FORK_FEATURES.md)。

---

## 2026-10-02 发布状态

- 状态：镜像已发布，服务器验收待完成；本地 39 项测试、真实 Xray `v26.3.27` 检查和 GitHub Actions 已完成，不能写成稳定发布。
- `master` commit `d6f3bec204a75085939b5b4e25fa6502f5946ae5`，Actions run `36975383911`；`ghcr.io/kissow/marzban-node:latest` index `sha256:f2a9e93ca3168abb3559f3e48baa98d02e6377fb8d4a480407f447a97bbbf774`，amd64 `sha256:81965a75de1bc07f5948bb42ea216d5cd80be36bca152641c41c0bf7820c0bc3`，arm64 `sha256:6d82315f1b73a0cd75b7c5ac2f5c3163d4fab10304a54fe8c250e461a4da63cd`，两个架构 OCI revision 均对应该 commit。
- 配对主面板为 `a6efaa8eafd82c3f68d2ff29074cf9eeb1ec8ae0`；Node 服务器更新前仍需备份证书、Compose、配置和数据目录。

本仓库由 Mr.shaw 基于 [Gozargah/Marzban-node](https://github.com/Gozargah/Marzban-node) 开发，供其他使用者按开源许可证使用。感谢原作者和贡献者；保留原有 Git 历史与 AGPL-3.0 许可证。本说明中的扩展不是上游官方功能。

`kissow/Marzban-node` 的 `master` 是唯一日常安装、升级和镜像发布源；与主面板的配对变更在临时分支完成，合并后删除临时分支；原作者仓库只保留为历史基线、许可证及致谢来源。

## 历史片段 2

原位置：[CHANGELOG.md](https://github.com/heyinkcode/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/CHANGELOG.md)。

---

## 2026-10-02 活动查询与策略接收（镜像已发布，服务器验收待完成）

- 固定 Xray v26.3.27 的 `GetAllOnlineUsers` 经现有 TLS API 查询；policy 启用 `statsUserOnline` 并保留已有字段。只有未实现 RPC 的旧核心回退到观察到的近期流量；失败显示未知。读取始终 reset=false，不清零主面板计费数据。
- 新增认证 REST `/device-activity`、`/device-policies` 和 RPyC 配对方法。共用原子校验，完整快照替换、重复用户拒绝、数量/revision/UTC 时间确认；不发送 HWID、IP 或用户代理凭据。
- 健康资源缓存和活动/策略元数据分别合成，避免缓存掩盖刚完成的同步。核心重启清除活动基线，认证会话更新清除旧策略。
- `device-policy-v1`、`xray-user-stats-v1` 表示合同支持；`policy_enforcement=subscription_request_and_node_credentials`、`direct_connection_enforced=true` 表示当前版本已经把已登记设备凭据加载到 Node 的 Xray 配置中。策略 ACK 本身仍不是实时在线设备数证明；旧版本的“仅订阅请求”描述已由本轮实现取代。
- 本地真实 Xray 验证 VLESS 连接/断开、TLS Stats RPC、非重置流量读取，以及 HTTP/SOCKS 配置；CI 固定核心实测步骤和 GHCR 构建均已成功，服务器尚未更新。
- 接口、旧节点兼容、升级和回退见 [合同](../activity-and-policy.md)。证书、服务端口、API 端口、数据库、数据目录、核心版本与安装脚本保持原样。

本文件仅记录本 Fork 相对 [Gozargah/Marzban-node](https://github.com/Gozargah/Marzban-node) 的改动。原作者、许可证和上游 Git 历史均保留；完整功能边界见 [FORK_FEATURES.md](../../FORK_FEATURES.md)。

## 历史片段 3

原位置：[RELEASE_CHECKLIST.md](https://github.com/heyinkcode/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/RELEASE_CHECKLIST.md)。

---

## MR-20261002-01 镜像发布核对（服务器验收待完成）

- [x] 本地 Python 3.12 完整 39 项测试通过，设置 `XRAY_TEST_BINARY` 后无跳过项。
- [x] 真实固定 Xray 26.3.27 验证 TLS Stats、VLESS 在线用户出现/消失、不清零计费以及 4 种 HTTP/SOCKS 配置。
- [x] 原子策略替换、认证会话、错误输入、即时健康确认和旧核心回退均有测试。
- [x] CI 增加固定核心实测步骤；接口合同和配对主面板文档更新。
- [x] Linux Actions 和发布镜像已完成；服务器验收尚未执行。

发布证据：Node `master` commit `d6f3bec204a75085939b5b4e25fa6502f5946ae5`，Actions `36975383911` 成功，GHCR index `sha256:f2a9e93ca3168abb3559f3e48baa98d02e6377fb8d4a480407f447a97bbbf774`；amd64 `sha256:81965a75de1bc07f5948bb42ea216d5cd80be36bca152641c41c0bf7820c0bc3`，arm64 `sha256:6d82315f1b73a0cd75b7c5ac2f5c3163d4fab10304a54fe8c250e461a4da63cd`。配对主面板 commit `a6efaa8eafd82c3f68d2ff29074cf9eeb1ec8ae0`，正式 Xray `v26.3.27`。

本清单适用于 `kissow/Marzban-node` 的每一次 Node 通道、健康指标、Xray 配置、住宅出口、核心版本、脚本或文档更新。涉及主面板下发协议时，必须和 `kissow/Marzban` 配对记录。

## 历史片段 4

原位置：[docs/node-development-plan.md](https://github.com/heyinkcode/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/docs/node-development-plan.md)。

---

## 2026-10-02 发布状态

镜像已发布，服务器验收待完成。`master` commit `d6f3bec204a75085939b5b4e25fa6502f5946ae5`、Actions `36975383911` 和 GHCR index `sha256:f2a9e93ca3168abb3559f3e48baa98d02e6377fb8d4a480407f447a97bbbf774` 已核对；配对主面板 commit 为 `a6efaa8eafd82c3f68d2ff29074cf9eeb1ec8ae0`。正式 Xray 固定 `v26.3.27`，不能把服务器尚未验收写成稳定发布。

## 历史片段 5

原位置：[docs/node-development-plan.md](https://github.com/heyinkcode/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/docs/node-development-plan.md)。

---

## 2026-10-02 配对增补（未发布）

本地加入核心在线用户查询、旧核心观察流量回退，以及脱敏策略快照接收确认。采用既有 REST/RPyC TLS 控制通道；Xray 仍固定 v26.3.27，原证书、端口、数据及部署命令保持原样。详情和限制以本仓库 [活动与策略合同](../activity-and-policy.md) 为准。

Node 接收策略确认不是单独的直接连接拦截证据；当前配对主面板会为已登记 HWID 生成独立协议凭据，并把仅含这些设备账号的 Xray 配置通过现有 TLS 控制通道下发到 Node。已经导入旧共享凭据的客户端不会被订阅请求主动踢下线；Node 不保存原始 HWID。

状态：开发分支已实现节点健康快照与每节点一条 HTTP/SOCKS 出站，完成本地单元测试和面板到 Node 的配置合同检查；真实 Xray 二进制解析测试需要设置 `XRAY_TEST_BINARY`，尚未在真实 Linux Node 联调或部署生产环境。具体能力与限制见根目录 `FORK_FEATURES.md`。
