import os

def send_http_request():
    server_ip = '8.8.8.8'
    port = '80'
    url = f'http://{server_ip}:{port}/does-not-conatin-bad-words.html'  # Requesting the index.html file

    print(f"Sending HTTP GET request to {url}")
    os.system(f'curl {url}')

    url = f'http://{server_ip}:{port}/contains-bad-words.html'  # Requesting the index.html file

    print(f"Sending HTTP GET request to {url}")
    os.system(f'curl {url}')

if __name__ == "__main__":
    send_http_request()
