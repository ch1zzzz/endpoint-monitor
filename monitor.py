import requests
import yaml
import time
import threading
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

availability_stats = {}


# load YAML
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


# check availability
def check_endpoint(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)

    try:
        start_time = time.time()
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=5)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=body, timeout=5)
        else:
            response = requests.request(method, url, headers=headers, data=body, timeout=5)

        latency = (time.time() - start_time) * 1000
        status_code = response.status_code

        if 200 <= status_code < 300 and latency < 500:
            # logging.info(f"UP - {endpoint['name']} [{url}] (status: {status_code}, latency: {latency:.2f} ms)")
            return True
        else:
            # logging.warning(f"DOWN - {endpoint['name']} [{url}] (status: {status_code}, latency: {latency:.2f} ms)")
            return False
    except requests.exceptions.RequestException as e:
        # logging.error(f"DOWN - {endpoint['name']} [{url}] (error: {e})")
        return False


# update data
def update_availability_stats(url, is_up):
    domain = urlparse(url).netloc
    if domain not in availability_stats:
        availability_stats[domain] = {'up_checks': 0, 'total_checks': 0}

    availability_stats[domain]['total_checks'] += 1
    if is_up:
        availability_stats[domain]['up_checks'] += 1


# print percent
def log_availability():
    for domain, stats in availability_stats.items():
        total_checks = stats['total_checks']
        up_checks = stats['up_checks']
        availability_percentage = int((up_checks / total_checks) * 100) if total_checks > 0 else 0
        logging.info(f"{domain} has {availability_percentage}% availability percentage")


# check points every 15s
def monitor_endpoints(endpoints, stop_event):
    while not stop_event.is_set():
        for endpoint in endpoints:
            is_up = check_endpoint(endpoint)
            update_availability_stats(endpoint['url'], is_up)
        log_availability()
        stop_event.wait(15)


# read YAML, start monitor
def main(file_path):
    try:
        endpoints = load_yaml(file_path)
        stop_event = threading.Event()
        monitor_thread = threading.Thread(target=monitor_endpoints, args=(endpoints, stop_event))
        monitor_thread.start()

        while monitor_thread.is_alive():
            monitor_thread.join(timeout=1)

    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Stopping...")
        stop_event.set()
        monitor_thread.join()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <path_to_yaml_file>")
        sys.exit(1)

    yaml_file = sys.argv[1]
    main(yaml_file)
