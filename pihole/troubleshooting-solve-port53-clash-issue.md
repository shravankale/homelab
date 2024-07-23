## PiHole port 53 conflict issue resolution

Source: https://github.com/pi-hole/docker-pi-hole?tab=readme-ov-file#installing-on-ubuntu-or-fedora and ChatGPT

### Steps to Modify systemd-resolved Configuration

1. **Edit `resolved.conf` to disable the DNS stub listener**:
    ```sh
    sudo sed -r -i.orig 's/#?DNSStubListener=yes/DNSStubListener=no/g' /etc/systemd/resolved.conf
    ```

2. **Update the `/etc/resolv.conf` symlink**:
    ```sh
    sudo rm /etc/resolv.conf
    sudo ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf
    ```

3. **Restart `systemd-resolved`**:
    ```sh
    sudo systemctl restart systemd-resolved
    ```

### Steps to Configure Netplan

If you need to explicitly set your Docker host's nameservers, update the netplan configuration:

1. **Edit netplan configuration** (assuming the configuration file is `/etc/netplan/01-netcfg.yaml`):
    ```sh
    sudo vim /etc/netplan/01-netcfg.yaml #Replace 01-netcfg.yaml with 01-xxx.yaml
    ```

2. **Update the configuration**:
    ```yaml
    network:
        version: 2
        renderer: NetworkManager
        ethernets:
            enp2s0: #Replace enp2s0 with your adapter id (check ip addr)
                dhcp4: yes
                dhcp4-overrides:
                    use-dns: no
                nameservers:
                    addresses:
                        - 1.1.1.1
                        - 1.0.0.1
    # Uncomment and configure this if needed in the future
    # wifis:
    #   wlp30:
    #     optional: true
    #     dhcp4: yes
    #     dhcp4-overrides:
    #       use-dns: no
    #     nameservers:
    #       addresses:
    #         - 1.1.1.1
    #         - 1.0.0.1

    ```
    The server itself does not use PiHole as a DNS service. But one of the addresses can be replaced with the PiHole DNS.
    **IMPORTANT**: Keep atleast one non-PiHole DNS nameserver as fallback just in case the PiHole container is unavaiable 

3. **Apply the netplan configuration**:
    ```sh
    sudo netplan apply
    ```
4. **Check dns settings in use (using NetworkManager):
    ```sh
    nmcli device show | grep IP4.DNS
    ```

Deploy Pihole with Updated Docker Compose File