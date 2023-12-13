import os
import argparse
import time

def send_http_request(long, mark_time, verbose, number_of_requests):
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

    # Initialize a dictionary to store cumulative time for each URL
    cumulative_time = {url: 0 for url in urls}

    for _ in range(number_of_requests):
        for url in urls:
            if verbose:
                print(f"Sending HTTP GET request to {url}")

            start_time = time.time()
            os.system(f'curl --silent -o /dev/null {"-s" if not verbose else ""} {url}')
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Add elapsed time to the cumulative time for this URL
            cumulative_time[url] += elapsed_time

            if mark_time:
                print(f"Request to {url} completed in {elapsed_time:.2f} seconds")

    # Calculate and print the average time for each URL
    if mark_time:
        for url in urls:
            average_time = cumulative_time[url] / number_of_requests
            print(f"Average time for {url}: {average_time:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--long', action='store_true', help='Request URLs with lots of text')
    parser.add_argument('--mark_time', action='store_true', help='Print the time elapsed during requests')
    parser.add_argument('--verbose', action='store_true', help='Print curl command output')
    parser.add_argument('--number_of_requests', type=int, default=1, help='Number of times to send requests')
    args = parser.parse_args()

    send_http_request(args.long, args.mark_time, args.verbose, args.number_of_requests)
