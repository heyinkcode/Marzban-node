# Marzban-node

A companion service for distributing Marzban across servers. This community fork is based on [Gozargah/Marzban-node](https://github.com/Gozargah/Marzban-node) and adds managed egress, health reporting and Node relay support. Configure it through the paired [Marzban panel](https://github.com/kissow/Marzban).

## Quick install
Install Marzban-node on your server using this command
```bash
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/kissow/Marzban-scripts/master/marzban-node.sh)" @ install
```
Install Marzban-node on your server using this command with custom name:
```bash
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/kissow/Marzban-scripts/master/marzban-node.sh)" @ install --name marzban-node2
```
Or you can only install this script (marzban-node command) on your server by using this command
```bash
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/kissow/Marzban-scripts/master/marzban-node.sh)" @ install-script
```

Use `help` to view all commands:
```marzban-node help```


## Manual install
Read the setup guide here: https://gozargah.github.io/marzban/docs/marzban-node

## Residential outbound setup

The Node does not require a separate residential-proxy program. Install Docker,
run the normal one-click Node installer, and keep the existing certificate,
service port and Xray API port. Configure the residential HTTP/SOCKS5 endpoint
in the paired Marzban panel; the panel sends the Node-specific setting through
the existing authenticated channel. The Node validates the generated Xray
configuration before restart. If no endpoint is configured, the Node behaves
like the upstream release.

For an existing official installation, switch it without deleting the current
certificate, ports or data:

```bash
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/kissow/Marzban-scripts/master/marzban-node.sh)" @ adopt
```

## Documentation

- [Feature and setup guides / 功能与使用文档](docs/README.md)
- [Changelog / 更新记录](CHANGELOG.md)
- [Protocol and maintenance guide / 协议与维护规范](docs/node-development-plan.md)
