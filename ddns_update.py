# -*- coding:utf-8 -*-
import time
import requests
import paramiko

# init info
ddns_domain = 'test.domain.com'
ddns_username = 'ddns_username'
ddns_password = 'ddns_password'
router_gateway = '192.168.1.1'
router_username = 'username'
router_password = 'password'
router_wan_name = 'pppoe-wan'
router_interval = 600
proxies = {"http":"http://192.168.1.10:8080"}
ddnsurl = {"dynu.com":"http://api.dynu.com/nic/update?hostname={}&myip={}&username={}&password={}"}

# get router wan ip address
def main(router_gateway, router_username, router_password, router_wan_name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(router_gateway, 22, router_username, router_password)

    wan_ip_addr = '0.0.0.0'

    while True:
        stdin, stdout, stderr = ssh.exec_command("ifconfig "+router_wan_name)
        ip_info = stdout.readlines()
        ip_info = str(ip_info).split('P-t-P')
        ip_addr = ip_info[0].split(':')[-1]

        if ip_addr != wan_ip_addr:
            update_ddns(ip_addr)
            wan_ip_addr = ip_addr

        time.sleep(router_interval)

# ddns update
def update_ddns(ip_addr, username=ddns_username, password=ddns_password, domain=ddns_domain, proxies=proxies):
    requests_url = ddnsurl["dynu.com"].format(domain,ip_addr,username,password)
    try:
        requests.get(requests_url, proxies=proxies)
        print("ip address had update! now it's {}".format(ip_addr))
    except:
        print("can't connect ddns api, please check you network!")

if __name__ == "__main__":
    main(router_gateway,router_username,router_password, router_wan_name)
