import os
import argparse
import time
import matplotlib.pyplot as plt

def send_http_request(long, mark_time, verbose, number_of_requests, plot):
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

    # Initialize a dictionary to store timings for each URL
    timings = {url: [] for url in urls}

    for _ in range(number_of_requests):
        for url in urls:
            if verbose:
                print(f"Sending HTTP GET request to {url}")

            start_time = time.time()
            os.system(f'curl --silent -o /dev/null {"-s" if not verbose else ""} {url}')
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Log the elapsed time for this URL
            timings[url].append(elapsed_time)

            if mark_time:
                print(f"Request to {url} completed in {elapsed_time:.2f} seconds")

    if plot:
        for url, times in timings.items():
            plt.figure()
            plt.plot(times, label='Response Time')
            plt.xlabel('Request Number')
            plt.ylabel('Time (seconds)')
            plt.title(f'Timings for {url}')
            plt.legend()
            plt.grid(True)

            # Ensure the analysis directory exists
            if not os.path.exists('./analysis'):
                os.makedirs('./analysis')

            # Save the plot
            plt.savefig(f'./analysis/timing_{url.split("/")[-1]}.png')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--long', action='store_true', help='Request URLs with lots of text')
    parser.add_argument('--mark_time', action='store_true', help='Print the time elapsed during requests')
    parser.add_argument('--verbose', action='store_true', help='Print curl command output')
    parser.add_argument('--number_of_requests', type=int, default=1, help='Number of times to send requests')
    parser.add_argument('--plot', action='store_true', help='Plot the timings and save the plots')
    args = parser.parse_args()

    send_http_request(args.long, args.mark_time, args.verbose, args.number_of_requests, args.plot)
