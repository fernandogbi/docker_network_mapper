
import docker
import ipaddress
import sys

print(__name__)


client = docker.from_env()

networks = client.networks.list()

higher_subnet = "0.0.0.0"

for network in networks:
    attrs = network.attrs
    config = attrs["IPAM"]["Config"]
    
    if len(config) == 0:
        continue
    
    subnet = config[0]["Subnet"]
    
    if ipaddress.ip_network(subnet) > ipaddress.ip_network(higher_subnet):
        higher_subnet = subnet

print("a rede mais alte e a: " + higher_subnet + " e sera criada agora a rede: " + str(ipaddress.IPv4Network(higher_subnet).broadcast_address + 1) + "/29")