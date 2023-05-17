# OpenWrt images for the NanoPi R4S

## Features
- Created from official builds using OpenWrt's imagebuilder.
- Full Docker compatability using 'firewall', 'iptables-legacy' and 'ip6tables-legacy'.
- Safely expands "/" partition on boot to fill microSD or eMMC.
- Includes LuCI interface w/ HTTPS support.
- No extra packages or bloatware.

## Usage

1. Write image to microSD card

```shell
dd if=openwrt-*-sysupgrade.img of=/dev/diskX
```
