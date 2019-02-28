
import docker
import ipaddress
import sys

def findNextNetwork():
    client = docker.from_env()

    networks = client.networks.list()

    higher_subnet = u"0.0.0.0"

    for network in networks:
        attrs = network.attrs
        config = attrs["IPAM"]["Config"]
        
        if len(config) == 0:
            continue
        
        subnet = config[0]["Subnet"]
        
        if ipaddress.ip_network(subnet) > ipaddress.ip_network(higher_subnet):
            higher_subnet = subnet

    new_network = str(ipaddress.IPv4Network(higher_subnet).broadcast_address + 1)

    if ipaddress.IPv4Network(unicode(new_network)).is_private:
        print(new_network+"/29")
    else:
        print(False)

if __name__ == '__main__':
    findNextNetwork()