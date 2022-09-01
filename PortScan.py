#!/usr/bin/env python
# coding: utf-8




import socket


target = 'telkom.co.za'   # we enter the host/url
targetIP = socket.gethostbyname(target) # gets ip address of host
print(targetIP)
ports = []  #  list of open ports


def port_scan(port_num):
    ourSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ourSocket.settimeout(0.1)
    if ourSocket.connect_ex((target, port_num)) == 0:
        ports.append(port_num)
    ourSocket.close()


for x in range(79,444):
    port_scan(x)
    
print("Target IP: {} | Target IP: {}".format(target, targetIP))

for port in ports:
    print("Port {}: OPEN".format(port))








# In[ ]:

