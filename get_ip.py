import dns.resolver

def get_ip_address(url):
    try:
        answers = dns.resolver.resolve(url, 'A')  # 'A' record for IPv4 addresses
        return [answer.to_text() for answer in answers]
    except Exception as e:
        return str(e)

# Example usage
url = "www.ufsm-map.onrender.com"
ip_addresses = get_ip_address(url)
print(f"The IP addresses of {url} are: {ip_addresses}")
