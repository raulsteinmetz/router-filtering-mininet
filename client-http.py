import os

def send_http_request():
    server_ip = '8.8.8.8'
    port = '80'

    url = f'http://{server_ip}:{port}/no-bw.html'  # Requesting the index.html file
    print(f"Sending HTTP GET request to {url}")
    os.system(f'curl {url}')

    url = f'http://{server_ip}:{port}/bw.html'  # Requesting the index.html file
    print(f"Sending HTTP GET request to {url}")
    os.system(f'curl {url}')

    url = f'http://{server_ip}:{port}/contains-lots-of-text.html'
    print(f"Sending HTTP GET request to {url}")
    os.system(f'curl {url}')

    url = f'http://{server_ip}:{port}/contains-lots-of-text-bw.html'
    print(f"Sending HTTP GET request to {url}")
    os.system(f'curl {url}')

if __name__ == "__main__":
    send_http_request()
