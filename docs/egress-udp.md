# Managed outbound DNS and UDP contract

Per-Node HTTP/SOCKS5 egress modes use an isolated configuration copy. They do not change the main-server business egress or another Node. Pinned Xray remains v26.3.27. See [diagnostics and acknowledged apply](egress-probe.md) for the current panel lifecycle.

## Wire format

Use the existing authenticated REST/RPyC Xray configuration channel; no new listener, certificate, database or public API:

```json
{
  "marzban_node_extensions": {
    "outbounds": [{
      "tag": "managed-residential-egress",
      "protocol": "socks",
      "server": "proxy.example.invalid",
      "port": 1080,
      "udp_mode": "tcp_only"
    }],
    "default_outbound_tag": "managed-residential-egress"
  }
}
```

At most one profile per Node; optional username/password must be supplied together. Do not log passwords/config payloads. Preserve encrypted panel storage and the existing Xray HTTP/SOCKS credential mapping. Node health adds `managed-outbounds-udp-v1`; retain `managed-outbounds-v1`.

| Mode | Semantics |
| --- | --- |
| absent / `legacy` | Old behavior. Panel omits the field for backward compatibility; SOCKS fallback uses TCP/UDP, HTTP fallback uses TCP. |
| `proxy` | SOCKS fallback TCP/UDP via the provider; no DNS rewrite. HTTP is invalid. This is not a capability probe of the provider. |
| `tcp_only` | Fallback UDP53 → DNS outbound with TCP through the residential proxy; other fallback UDP → blackhole; fallback TCP → residential proxy. |

All existing explicit API/security/domain/IP/inbound rules before the generic fallback retain priority, including explicit direct routes. Do not claim full-flow leak protection. No new direct fallback is added. Non-DNS UDP is not converted to TCP; application fallback is not guaranteed.

For `tcp_only`, the Node-local DNS server list is replaced with `tcp://1.1.1.1` and `tcp://8.8.8.8`; hosts/queryStrategy and other DNS settings are preserved. The resolver's private inbound tag routes through the provider. A/AAAA use the internal resolver; other DNS requests use the DNS outbound TCP tunnel. Providers must permit TCP53, and custom DNS server/domain rules are replaced. Reserved tags `managed-residential-dns`, `managed-residential-dns-query`, `managed-residential-udp-block` cannot collide with existing inbound/outbound/DNS tags.

The extension is validated and applied on a deep copy, committed only on success. Invalid mode/type, HTTP+proxy, duplicate/reserved tags or invalid structure raise `OutboundConfigError`. Core preflight must succeed before replacing the running core. A syntactically valid config does not prove the provider is reachable.

## Compatibility and rollback

Panel GET/PUT egress expose `udp_mode`, default legacy. Nonlegacy requires both capability flags and is checked before saving and again on connect/restart. Missing capability/old/offline Node returns panel 409; invalid input 422. The legacy wire field remains parse-compatible with old managed-outbound Nodes; the current panel save/delete workflow additionally requires `managed-egress-probe-v1`, acknowledged apply and API readiness. See [diagnostics and safe apply](egress-probe.md). A downgraded Node cannot silently ignore saved nonlegacy settings.

Update a target Node with the required outbound and safe-apply capabilities first, check connection, then update the panel and enable a mode on a test Node. Back up Compose, certificates/config and data directories. Existing switched Fork installations use update without repeated adopt. Keep existing service/API ports, volumes and credentials; do not reinstall or delete volumes. Restore legacy before downgrading either side. Panel migration only adds `node_egress.udp_mode`; Node has no migration.

## Verification and attribution

Use an isolated test account to verify the provider exit IP, TCP53, selected UDP mode and real client behavior. Do not change a busy production Node to isolate one phone. Parser or local DNS success does not prove all applications or a provider's full UDP support.

Retain Gozargah/Marzban-Node and XTLS/Xray-core licenses and credits. Reference behavior: [fixed-version DNS outbound](https://github.com/XTLS/Xray-core/blob/v26.3.27/proxy/dns/dns.go) and [DNS config parser](https://github.com/XTLS/Xray-core/blob/v26.3.27/infra/conf/dns_proxy.go).

[Panel configuration guide](https://github.com/kissow/Marzban/blob/master/docs/NODE_EGRESS_UDP.md) · [Historical tests and release evidence](releases/egress-udp-guide-20261015.md)
