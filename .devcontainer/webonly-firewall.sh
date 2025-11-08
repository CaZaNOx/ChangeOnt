#!/usr/bin/env bash
set -euo pipefail

# If iptables isn't callable (no CAP_NET_ADMIN / policy), skip but succeed.
if ! /usr/sbin/iptables -L >/dev/null 2>&1; then
  echo "[webonly-firewall] No iptables access (no CAP_NET_ADMIN/NFT policy). Skipping."
  exit 0
fi

# Flush and allow loopback + established
/usr/sbin/iptables -F OUTPUT || true
/usr/sbin/iptables -P OUTPUT ACCEPT
/usr/sbin/iptables -A OUTPUT -o lo -j ACCEPT
/usr/sbin/iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Block LAN/host ranges; keep internet open
for NET in 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16 169.254.0.0/16 172.17.0.0/16 100.64.0.0/10; do
  /usr/sbin/iptables -A OUTPUT -d "$NET" -j REJECT || true
done
/usr/sbin/iptables -A OUTPUT -d 172.17.0.1 -j REJECT || true

echo "[webonly-firewall] Applied: LAN/host blocked; internet allowed."
