
import docker
import ipaddress as ipaddr
import sys

def findNextNetwork():
    client = docker.from_env()

    networks = client.networks.list()
    subnets = []

    for network in networks:
        attrs = network.attrs
        config = attrs["IPAM"]["Config"]
        
        if len(config) == 0:
            continue
        
        subnets.append(ipaddr.ip_network(config[0]["Subnet"]))

    for index in range(0,len(subnets)):
        new_network = str(subnets[index].broadcast_address + 1)+"/29"
        if checkOverlaps(subnets, new_network):
            print(new_network+" is available")
            sys.exit(0)
            
    print("not subnets available in private range IP")

def checkOverlaps(subnets, new_network):
    for subnet in subnets:
        if subnet.overlaps(ipaddr.IPv4Network(unicode(new_network))) == True:
            return False
        elif ipaddr.IPv4Network(unicode(new_network)).is_private == False:
            return False

    return True

if __name__ == '__main__':
    findNextNetwork()