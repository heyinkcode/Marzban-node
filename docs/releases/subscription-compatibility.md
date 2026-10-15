# 普通订阅与 HWID 兼容：历史发布记录

[当前说明](../activity-and-policy.md) · [历史索引](README.md)

本文按功能保留原始发布证据。记录中的「当前」「最新」「未发布」「待验收」仅指原记录形成时的状态，不能替代当前说明或新的验收记录。旧流程和旧接口描述不是现行使用指引；重复正文合并并保留来源。整理日期：2026-10-15。

## 历史片段 1

原位置：[FORK_FEATURES.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/FORK_FEATURES.md)。

---

## 2026-10-03 主面板订阅兼容配对（Node 运行时无变化）

主面板在 `reject_new` 下对不带 `X-HWID` 的普通客户端恢复原共享订阅；Node 仍从原有认证控制通道加载主面板配置中的共享账号和已登记 HWID 独立账号。Node 不接收原始 HWID、不独立登记设备、不新增端口/数据库/证书/核心版本，本次不需更新 Node。带 HWID 的超额拒绝由主面板执行；无 HWID/共享配置可绕过 HWID 限额，因此不是物理设备或实时在线设备限制。真实 Node 验收需随主面板重新执行。

配对镜像已发布：主面板源 `37bab0b113c44ccb2a9db6230ac982b7d2a889a1` / Actions `37090609233` / GHCR `sha256:c4bbe88b5b547bbdca3d6b8a4bf1e7c92aeb29ae50b36cd758b7c6eccae2edfc`；Node 源 `c135743d1ad26d45538e4c6c7a65a9c6693856a8` / Actions `37090612247` / GHCR `sha256:21340918298f0b8647fb7eb360294334891fc219e280a75af5d133c66ee9fbc1`。服务器验收待完成。

## 历史片段 2

原位置：[CHANGELOG.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/CHANGELOG.md)。

---

## 2026-10-03 主面板订阅兼容修复配对说明（镜像已发布，服务器验收待完成；Node 运行时无变化）

- 主面板修复 `reject_new` 对无 `X-HWID` 客户端返回 `428` 的回归，并恢复共享账号；Node 继续通过原有认证 Xray 控制通道接收共享账号和已登记 HWID 的独立账号。
- Node 不保存原始 HWID、不自行判断订阅是否带 HWID，也不新增端口、数据库、证书或 Xray 核心版本；本次不需要更新 Node 镜像。
- 带 HWID 的新设备超额拒绝由主面板订阅登记执行，Node 只加载主面板下发的最终账号配置。无 HWID 客户端使用共享凭据，不能获得 HWID 限额保证；策略 ACK 不是所有客户端被拦截的证明。
- 主面板本轮服务器验收需重新完成；本条不能把此前 Node 镜像发布证据当作本轮验收通过。
- 配对发布证据：主面板源 commit `37bab0b113c44ccb2a9db6230ac982b7d2a889a1` / Actions `37090609233` / GHCR `latest` index `sha256:c4bbe88b5b547bbdca3d6b8a4bf1e7c92aeb29ae50b36cd758b7c6eccae2edfc`；Node 源 commit `c135743d1ad26d45538e4c6c7a65a9c6693856a8` / Actions `37090612247` / GHCR `latest` index `sha256:21340918298f0b8647fb7eb360294334891fc219e280a75af5d133c66ee9fbc1`。Node 本轮无需更新服务器。

## 历史片段 3

原位置：[RELEASE_CHECKLIST.md](https://github.com/kissow/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/RELEASE_CHECKLIST.md)。

---

## MR-20261003-HWID-COMPAT 配对发布（镜像已发布，服务器验收待完成）

- [x] 配对主面板修复无 HWID 普通客户端在 `reject_new` 下返回 `428` 的回归；Node 运行时无需修改，继续接收共享账号与已登记 HWID 独立账号。
- [x] Node 源 commit `c135743d1ad26d45538e4c6c7a65a9c6693856a8` 已推送；Actions `37090612247` 成功；GHCR `latest` index `sha256:21340918298f0b8647fb7eb360294334891fc219e280a75af5d133c66ee9fbc1` 已发布。
- [x] 配对主面板源 commit `37bab0b113c44ccb2a9db6230ac982b7d2a889a1`、Actions `37090609233` 和 GHCR `latest` index `sha256:c4bbe88b5b547bbdca3d6b8a4bf1e7c92aeb29ae50b36cd758b7c6eccae2edfc` 已记录；正式 Xray 仍为 `v26.3.27`。
- [ ] 服务器尚未更新；待主面板服务器完成普通订阅、HWID 登记/重复/超额和真实 Node 连接验收。
