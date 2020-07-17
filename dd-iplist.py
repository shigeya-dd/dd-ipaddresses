#!/usr/bin/env python3
##### shigeya.tanabe@datadoghq.com

import ipaddress
import requests # pip3 install requests
import json

def get_region(dd_ip, aws_iplist):
    ip = ipaddress.ip_address(dd_ip)
    region = 'n/a'
    for prefix in aws_iplist:
        if ip in ipaddress.ip_network(prefix['ip_prefix']):
            region = prefix['region']
            break
    return region

if __name__ == '__main__':
    service = "synthetics"
    # service = "webhooks"
    url_dd = "https://ip-ranges.datadoghq.com/%s.json" % service
    url_aws = "https://ip-ranges.amazonaws.com/ip-ranges.json"

    response = requests.get(url_dd)
    json_dd = response.json()
    
    response = requests.get(url_aws)
    json_aws = response.json()

    ip_list = []
    for dd_ip in json_dd[service]["prefixes_ipv4"]:
        dd_ip = dd_ip.split('/')[0]
        ip_list.append([dd_ip, get_region(dd_ip, json_aws['prefixes'])])

    ip_list.sort(key=lambda x: x[1])
    for ip in ip_list:
        print(*ip, sep=',')

