#!/usr/bin/env python3
### shigeya.tanabe@datadoghq.com
###
### Usage (CSV): python3 dd-iplist.py
### Usage (JSON): python3 dd-iplist.py -j

import ipaddress
import requests # pip3 install requests
import json
import sys

def get_region(dd_ip, aws_iplist):
    ip = ipaddress.ip_address(dd_ip)
    region = 'n/a'
    for prefix in aws_iplist:
        if ip in ipaddress.ip_network(prefix['ip_prefix']):
            region = prefix['region']
            break
    return region

if __name__ == '__main__':
    out_format = "csv"
    if (len(sys.argv) == 2 and sys.argv[1] == "-j"):
        out_format = "json"

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
    if(out_format == "json"):
        ip_list_json = []
        for ip, region in ip_list:
            ip_list_json.append({'ip_address':"%s/32" % ip, 'region': region})
        json_dd[service]["prefixes_ipv4_region"] = ip_list_json
        print(json.dumps(json_dd, indent = 4))
    else:
        for ip in ip_list:
            print(*ip, sep=',')

