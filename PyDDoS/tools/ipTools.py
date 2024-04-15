import sys
import socket
import ipaddress
import requests
from urllib.parse import urlparse
from time import sleep
from colorama import Fore

""" Check if site is under CloudFlare protection """

def __isCloudFlare(link):
    parsed_uri = urlparse(link)
    domain = "{uri.netloc}".format(uri=parsed_uri)
    try:
        origin = socket.gethostbyname(domain)
        iprange = requests.get("https://www.cloudflare.com/ips-v4").text
        ipv4 = [row.rstrip() for row in iprange.splitlines()]
        for i in range(len(ipv4)):
            if ipaddress.ip_address(origin) in ipaddress.ip_network(ipv4[i]):
                print(
                    f"{Fore.RED}[!] {Fore.YELLOW}The site is protected by CloudFlare, attacks may not produce results.{Fore.RESET}"
                )
                sleep(1)
    except socket.gaierror:
        return False

def __GetAddressInfo(target):
    try:
        ip = target.split(":")[0]
        port = int(target.split(":")[1])
    except IndexError:
        print(f"{Fore.RED}[!] {Fore.MAGENTA}You must enter ip and port{Fore.RESET}")
        sys.exit(1)
    else:
        return ip, port

def __GetURLInfo(target):
    if not target.startswith("http"):
        target = f"http://{target}"
    return target

def GetTargetAddress(target, method):
    if method in (
        "IPATTACK",
    ) and target.startswith("http"):
        parsed_uri = urlparse(target)
        domain = "{uri.netloc}".format(uri=parsed_uri)
        origin = socket.gethostbyname(domain)
        __isCloudFlare(domain)
        return origin, 80
    elif method in ("IPATTACK"):
        return __GetAddressInfo(target)
    elif method == "URLATTACK":
        url = __GetURLInfo(target)
        __isCloudFlare(url)
        return url
    else:
        return target

def InternetConnectionCheck():
    try:
        requests.get("https://google.com", timeout=4)
    except:
        print(
            f"{Fore.RED}[!] {Fore.MAGENTA}Your device is not connected to the Internet{Fore.RESET}"
        )
        sys.exit(1)
