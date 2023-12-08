import os

def send_http_request():
    server_ip = '8.8.8.8'
    port = '80'
    url = f'http://{server_ip}:{port}'
    data = "sample_data=HelloWorld"

    print(f"Sending HTTP POST request to {url}")
    os.system(f'curl -X POST -d "{data}" {url}')

if __name__ == "__main__":
    send_http_request()
