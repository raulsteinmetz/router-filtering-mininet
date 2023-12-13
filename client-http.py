import os
import argparse
import time

def send_http_request(long, mark_time):
    server_ip = '8.8.8.8'
    port = '80'

    if long:
        urls = [
            f'http://{server_ip}:{port}/contains-lots-of-text.html',
            f'http://{server_ip}:{port}/contains-lots-of-text-bw.html'
        ]
    else:
        urls = [
            f'http://{server_ip}:{port}/no-bw.html',
            f'http://{server_ip}:{port}/bw.html'
        ]

    for url in urls:
        if not mark_time:
            print(f"Sending HTTP GET request to {url}")
        start_time = time.time()
        os.system(f'curl {url} {"-s" if mark_time else ""}')
        end_time = time.time()

        if mark_time:
            print(f"Request to {url} completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--long', action='store_true', help='Request URLs with lots of text')
    parser.add_argument('--mark_time', action='store_true', help='Print the time elapsed during requests')
    args = parser.parse_args()

    send_http_request(args.long, args.mark_time)
