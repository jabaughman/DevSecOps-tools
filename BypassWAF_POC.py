import socket 
import requests
import sys

banner = r'''
 _______  _____         _______  ______ _______        _______  ______ _______ _______
 |______ |     | |      |_____| |_____/ |______ |      |_____| |_____/ |______ |______
 ______| |_____| |_____ |     | |    \_ |       |_____ |     | |    \_ |______ ______|
                                                                   Wake up, Samurai...                     
'''
VERSION = '1.0'

class text_color:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        yellow = '\033[33m'
        blue = '\033[34m'
        magenta = '\033[35m'
        cyan = '\033[36m'
        white = '\033[37m'

def display_info():
    print(f'{text_color.red}{banner}{text_color.red}\n')
    print(f'{text_color.yellow}Version = {text_color.white}{VERSION}')

def cloudflare_ips(domain):
    try:
        ip_address   = socket.gethostbyname(domain)
        sock_addr    = (ip_address, 443)
        sock_info    = socket.getnameinfo(sock_addr, socket.NI_NUMERICSERV)
        return ip_address, sock_info
    except socket.gaierror:
        return None, None

def enum_sub_domains(domain):
    if not cloudflare_detect(domain):
        print("{domain} is not using cloudflare so I'll parse subdomains for you instead")
        return

def cloudflare_detect(domain):
    try:
        response = requests.head(f"https://{domain}", timeout=5)
        headers = response.headers
        if "server" in headers and "cloudflare" in headers ["server"].lower():
            return True
        if "cf-ray" in headers:
            return True
        if "cloudflare" in headers:
            return True
        if "cf-team" in headers:
            return True
        if "cf-cache-status" in headers:
            return True
    except (requests.exceptions.RequestException, requests.exceptions.ConnectTimeout):
        pass

    return False

def detect_wildcard_bypass_option(domain):
    try:
        response = requests.head(f"https://bypass.{domain}", timeout=5)
        # If the status code is OK, get socket info and return
        if response.status_code == requests.codes.ok:
            ip_address = socket.gethostbyname(f"bypass.{domain}")
            sock_addr = (ip_address, 443)
            sock_info = socket.getnameinfo(sock_addr, socket.NI_NUMERICSERV)
            return sock_info
        

    except (requests.exceptions.RequestException, requests.exceptions.ConnectTimeout, socket.gaierror) as e:
        # Log exception or handle it
        print(f"Error occured: {e}")
    
    # Return None or a specific error indicator if an exception occurs
    return None

    # Optionally, you can return a different value here if none of the above conditions are met


if __name__ == "__main__":
    display_info()
    # Check if a command-line argument is provided
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        # Prompt the user for a domain or set a default
        domain = input("Please enter a domain: ") # Or set a default like domain = "example.com"
    

    ip, sock_info = cloudflare_ips(domain)
    wildcard_detect = detect_wildcard_bypass_option(domain)

    if cloudflare_detect(domain):
        print(f"Target: {domain}")
    if ip is not None and sock_info is not None:
        print(f"IP Address: {ip}, Socket Info: {sock_info}")
    else:
        print("Target is not Proxied by Cloudflare")
    
    if wildcard_detect is not None:
        print(f"Socket Info for Bypass: {wildcard_detect}")