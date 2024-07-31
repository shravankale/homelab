# Homelab over Tailscale

### TODO:
1. Test if "--accept-dns=false" is required

## Instructions:

### Install Tailscale on server
```bash
# Source: https://tailscale.com/download/linux
curl -fsSL https://tailscale.com/install.sh | sh
```

### Initiate tailscale

Handle the initial login flow using identity provider such as google

```bash
# tailscale up: start tailscale
# --accept-dns=false : This makes sure that the dns of the tailscale network (tailnet) isn't set as itself 
# --advertise-routes=xxx.yy.0.0/mm : where xxx.yy.0.0 is the docker bridge network and mm is the subnetmask in CIDR format
sudo tailscale up --accept-dns=false --advertise-routes=xxx.yy.0.0/mm
```

### Enabling the subnet and IP forwarding (and optimization)

#### 1. Enable the subnet
Enable the subnet for the machine(server) on tailscale admin web console

#### 2. Enable IP forwarding 
IP forwarding: forwading packets across network interfaces on the server

```bash
#Check current status of IP forwarding, If it returns 0, IP forwarding is disabled, and if 1 then it's enabled.
sysctl net.ipv4.ip_forward

#Temporarily enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1

#Enable forwarding permanently in sudo vim /etc/sysctl.conf
sudo nano /etc/sysctl.conf
#Uncomment the line #net.ipv4.ip_forward=1 by removing the '#' and save

#Reload settings
sudo sysctl -p
```

#### 3. Add server as a nameserver on tailscale
On the tailscale admin web console, add the tailscale IP of the server as a nameserver under DNS settings

#### 4. Potential system optimizations --> **Doesn't work yet**
Refer: https://tailscale.com/kb/1320/performance-best-practices#ethtool-configuration

```bash
NETDEV=$(ip route show 8.8.8.8 | cut -f5 -d' ')
sudo ethtool -K $NETDEV rx-udp-gro-forwarding on rx-gro-list off

#Enable on each boot
printf '#!/bin/sh\n\nethtool -K %s rx-udp-gro-forwarding on rx-gro-list off \n' "$(ip route show 0/0 | cut -f5 -d" ")" | sudo tee /etc/networkd-dispatcher/routable.d/50-tailscale
sudo chmod 755 /etc/networkd-dispatcher/routable.d/50-tailscale

#Test the created script to ensure it runs successfully on your machine:
sudo /etc/networkd-dispatcher/routable.d/50-tailscale
test $? -eq 0 || echo 'An error occurred.'
```