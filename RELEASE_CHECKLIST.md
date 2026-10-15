# Marzban-Node 发布检查清单

每次发布复制此未勾选模板，结果进入对应功能发布页；[历史记录](docs/releases/README.md)不能当成本次通过证明。

- [ ] 配对主控、Node、scripts 范围与最低能力已登记；无运行时变化的仓库已标明。
- [ ] 功能合同、CHANGELOG 摘要、协议索引与功能目录同步；首页不添加发布明细。
- [ ] 原证书、端口、数据、账号和固定 Xray v26.3.27 保留，无敏感字段泄露。
- [ ] REST/RPyC 认证、旧版本、错误输入、完整快照和精确 ACK 已验证。
- [ ] 单元、真实固定核心、限时子进程、并发、失败恢复和清理按范围测试；跳过项如实记录。
- [ ] PR 与正式 Linux 工作流通过；SHA、双架构 OCI 摘要与 revision 已对应核对。
- [ ] 实际升级前备份和回滚方案已核验；已有 Fork 用 update，新机才 install。
- [ ] 实际控制连接、业务入站、出口、DNS/UDP、订阅和中转按范围逐台验收。
- [ ] 区分发布与服务器验收；记录验收日期、范围、剩余风险和恢复步骤。
- [ ] 纯文档提交明确无需重新构建镜像，不把旧运行时 revision 改成文档提交 SHA。

[协议边界](docs/node-development-plan.md) · [主控发布流程](https://github.com/kissow/Marzban/blob/master/docs/REPOSITORY_UPDATE_FLOW.md)
