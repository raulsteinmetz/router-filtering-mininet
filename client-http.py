import os

def send_http_request():
    server_ip = '8.8.8.8'
    port = '80'  # Assuming the HTTP server is running on port 80
    url = f'http://{server_ip}:{port}'

    print(f"Sending HTTP request to {url}")
    os.system(f'curl {url}')

if __name__ == "__main__":
    send_http_request()
