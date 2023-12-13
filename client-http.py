import os
import argparse
import time
import matplotlib.pyplot as plt
import numpy as np
import subprocess

def send_http_request(long, mark_time, verbose, number_of_requests, plot):
    server_ip = '8.8.8.8'
    port = '80'
    packet_size = 64  # in bytes

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

    timings = {url: [] for url in urls}
    data_transferred = {url: [] for url in urls}

    for _ in range(number_of_requests):
        for url in urls:
            if verbose:
                print(f"Sending HTTP GET request to {url}")

            start_time = time.time()
            # Adjusting curl command based on verbose flag
            if verbose:
                # Output to console and save file
                result = subprocess.run(f'curl -o ./received_file.html -w "%{{size_download}}" {url}', 
                                        shell=True, capture_output=True, text=True)
            else:
                # Run silently
                result = subprocess.run(f'curl --silent -o /dev/null -w "%{{size_download}}" {url}', 
                                        shell=True, capture_output=True, text=True)
            end_time = time.time()
            elapsed_time = end_time - start_time
            timings[url].append(elapsed_time)
            data_transferred[url].append(int(result.stdout.strip()))

            if mark_time:
                print(f"Request to {url} completed in {elapsed_time:.2f} seconds")


    # Compute and print bytes per second and packets per second
    for url in urls:
        total_bytes = sum(data_transferred[url])
        total_time = sum(timings[url])
        bytes_per_second = total_bytes / total_time
        packets_per_second = bytes_per_second / packet_size

        print(f"{url} - Bytes per second: {bytes_per_second:.2f}, Packets per second: {packets_per_second:.2f}")

    if plot:
        for url, times in timings.items():
            plt.figure()

            # Calculate moving average
            moving_avg = np.convolve(times, np.ones(5)/5, mode='valid')

            plt.plot(times, label='Response Time')
            plt.plot(range(4, len(times)), moving_avg, label='Moving Average (5)', linestyle='--')

            plt.xlabel('Request Number')
            plt.ylabel('Time (seconds)')
            plt.title(f'Timings for {url}')
            plt.legend()
            plt.grid(True)

            if not os.path.exists('./analysis'):
                os.makedirs('./analysis')

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
