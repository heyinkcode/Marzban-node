# Xray 核心基线：历史发布记录

[当前说明](../node-development-plan.md) · [历史索引](README.md)

本文按功能保留原始发布证据。记录中的「当前」「最新」「未发布」「待验收」仅指原记录形成时的状态，不能替代当前说明或新的验收记录。旧流程和旧接口描述不是现行使用指引；重复正文合并并保留来源。整理日期：2026-10-15。

## 历史片段 1

原位置：[FORK_FEATURES.md](https://github.com/heyinkcode/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/FORK_FEATURES.md)。

---

## Xray 核心版本与功能边界

仓库正式构建基线统一为 `v26.3.27`（稳定版）。Node 的 Dockerfile 和 GitHub Actions 通过 `XRAY_CORE_VERSION` 固定该版本，并与主面板配对发布；Node 不再在构建时随 `latest` 自动漂移。`v26.9.9` 当前是预发布版本，不能直接作为生产 `latest`。

Xray 核心新增协议或传输层不会自动变成 Node 的可配置功能。只有主面板能生成对应 Xray JSON、Node 能安全接收并预检/重启、订阅转换覆盖客户端格式，且完成端到端测试后，才会新增面板开关。当前 Node 扩展只处理节点健康回报和每个 Node 独立的 HTTP/SOCKS 住宅代理出站；Hysteria 2、Finalmask、XHTTP/3、ECH、WireGuard 等暂不宣称已通过本扩展开放。

如果测试 `v26.9.9`，必须使用独立测试镜像标签，不覆盖 `latest`，并检查配置预检、TCP/UDP、DNS、证书、重启恢复和回滚。服务器上的 `core-update` 可能写入外部 Xray 二进制，导致容器内外出现不同版本；正式部署以仓库镜像中的固定版本为准。

## 历史片段 2

原位置：[CHANGELOG.md](https://github.com/heyinkcode/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/CHANGELOG.md)。

---

## 正式版核心一致性闸门（2026-09-30，未发布）

- 构建完成后立即读取 Xray 二进制版本，并强制核对为 `v26.3.27`；下载脚本返回错误版本时镜像构建失败。
- GitHub Actions 增加正式版本锁定检查，避免主面板和 Node 的 `latest` 镜像意外混入其他核心。

## 历史片段 3

原位置：[CHANGELOG.md](https://github.com/heyinkcode/Marzban-node/blob/7d103e66972e1eeecc3002edc83ba926460ee6c4/CHANGELOG.md)。

---

## Xray 核心正式基线收口（2026-09-30，未发布）

- Node Dockerfile、GitHub Actions 和安装脚本统一锁定 `XRAY_CORE_VERSION=v26.3.27`，不再从动态 `latest` 地址取核心。
- Node 的 `core-update` 采用相同固定版本，并同步修正下载完成提示；删除无效的旧核心菜单变量，避免出现多个版本来源。
- 保留显式版本参数作为隔离测试入口；正式镜像和生产 Node 不使用 `v26.9.9` 等测试候选版本。
- 本次没有删除或迁移证书、端口、节点数据、Docker 数据卷或现有配置；镜像尚未由本地变更直接宣称发布。
