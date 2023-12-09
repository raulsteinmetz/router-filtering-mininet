import os

def send_http_request():
    server_ip = '8.8.8.8'
    port = '80'
    url = f'http://{server_ip}:{port}/index.html'  # Requesting the index.html file

    print(f"Sending HTTP GET request to {url}")
    os.system(f'curl {url}')

if __name__ == "__main__":
    send_http_request()
