import os
import argparse

def send_http_request(long):
    server_ip = '8.8.8.8'
    port = '80'

    if long:
        # Request only the pages with lots of text
        urls = [
            f'http://{server_ip}:{port}/contains-lots-of-text.html',
            f'http://{server_ip}:{port}/contains-lots-of-text-bw.html'
        ]
    else:
        # Request the other pages
        urls = [
            f'http://{server_ip}:{port}/no-bw.html',
            f'http://{server_ip}:{port}/bw.html'
        ]

    for url in urls:
        print(f"Sending HTTP GET request to {url}")
        os.system(f'curl {url}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--long', action='store_true', help='Request URLs with lots of text')
    args = parser.parse_args()

    send_http_request(args.long)
