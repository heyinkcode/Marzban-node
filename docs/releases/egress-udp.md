# 出口 UDP 与 DNS：历史发布记录

[当前说明](../egress-udp.md) · [历史索引](README.md)

本文按功能保留原始发布证据。记录中的「当前」「最新」「未发布」「待验收」仅指原记录形成时的状态，不能替代当前说明或新的验收记录。旧流程和旧接口描述不是现行使用指引；重复正文合并并保留来源。整理日期：2026-10-15。

## 历史片段 1

原位置：[FORK_FEATURES.md](https://github.com/heyinkcode/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/FORK_FEATURES.md)。

---

## MR-20261003-EGRESS-UDP（镜像已发布，服务器验收待完成）

新增能力 `managed-outbounds-udp-v1` 和 per-Node `udp_mode`：legacy 保持原样，proxy 使用 SOCKS TCP/UDP，tcp_only 将默认 UDP DNS 经住宅代理改走 TCP、阻断其他默认 UDP。保留已有显式路由优先级，不添加直连降级；不能保证全部应用回退 TCP。主面板与 Node 均有运行时代码变化，需要发布后配对更新，scripts/核心/证书/端口/数据卷无变化。48 项本地测试通过，实际手机与供应商、Linux 配对验收待完成。详见 [线协议和限制](../egress-udp.md)。下方历史 Node 无变化说明不适用于本功能。

发布证据（配对源 SHA、Actions、两镜像 index/架构 digest/OCI revision、scripts 文档提交）见 [egress-udp-release.md](../egress-udp-release.md)。服务器未验收，不是稳定版。

## 历史片段 2

原位置：[CHANGELOG.md](https://github.com/heyinkcode/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/CHANGELOG.md)。

---

## MR-20261003-EGRESS-UDP：住宅代理 UDP 兼容（镜像已发布，服务器验收待完成）

- 通过原认证配置通道接受 per-Node `udp_mode`，新增 `managed-outbounds-udp-v1`；默认 legacy 不改变旧行为。
- `proxy` 保留 SOCKS TCP/UDP；`tcp_only` 将默认 UDP53 DNS 交给 TCP 住宅隧道、阻断其他默认 UDP，保留原显式路由优先级。不会将所有 UDP 转 TCP，不新增直连回退。
- 配置在深拷贝中验证后原子提交，错误模式/标签冲突不写入半套配置。TCP-only 替换该 Node 的 DNS 上游列表，供应商需允许 TCP53。
- 48 项完整本地测试通过：8 组真实固定核心配置解析、4 项 DNS TCP 运行测试；Linux/实际供应商/手机应用验收待完成。两个仓库已推送，Actions 和配对 latest 发布核对通过；真实服务器验收待完成。
- 需要配对主面板更新；scripts、证书、端口、数据卷、固定核心 v26.3.27 无变化。完整线协议见 [egress-udp.md](../egress-udp.md)。下方历史“Node 不需更新”仅适用于 HWID 兼容修复，不适用于本功能。

发布证据（配对源 SHA、Actions、两镜像 index/架构 digest/OCI revision、scripts 文档提交）见 [egress-udp-release.md](../egress-udp-release.md)。服务器未验收，不是稳定版。

## 历史片段 3

原位置：[RELEASE_CHECKLIST.md](https://github.com/heyinkcode/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/RELEASE_CHECKLIST.md)。

---

## MR-20261003-EGRESS-UDP（镜像已发布，服务器验收待完成）

- [x] 能力 `managed-outbounds-udp-v1`、legacy/proxy/tcp_only 线协议、显式路由优先级与 DNS 上游替换边界已登记。
- [x] 原子配置应用、非法模式/HTTP+proxy/标签冲突、旧配置兼容有回归测试。
- [x] 48 项完整测试通过无跳过；固定 Xray v26.3.27，8 组配置解析、4 项 A/TXT 经模拟 HTTP/SOCKS TCP 供应商运行测试。
- [x] README/FORK_FEATURES/CHANGELOG/[协议](../egress-udp.md) 和配对主面板、05/08/09 已更新；scripts 运行时无变化，配对文档已更新并通过 Actions 检查。
- [ ] 隔离 Linux 认证通道与实际供应商 TCP53、v2rayNG/Clash Meta、其他 UDP 应用和 legacy 回退验收。
- [x] 配对推送、Actions 成功、镜像 index/架构 digest/OCI revision 已登记。服务器验收仍待完成。

本功能有 Node 运行时代码变化，需要发布后更新 Node；下方“Node 不需更新”仅属于旧 HWID 兼容补丁。未改证书、端口、数据卷或核心版本；不要重装或删除数据。其他 UDP 的阻断为路由单元覆盖，非真实应用全量保证。

发布证据（配对源 SHA、Actions、两镜像 index/架构 digest/OCI revision、scripts 文档提交）见 [egress-udp-release.md](../egress-udp-release.md)。服务器未验收，不是稳定版。
