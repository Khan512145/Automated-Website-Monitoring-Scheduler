import requests
import time
from queue import Queue
from datetime import datetime

class WebsiteMonitor:
    def __init__(self, log_filename="monitor_log.txt"):
        self.website_queue = Queue()
        self.visited_websites = set()  # Set to track added websites
        self.log_file = log_filename

    def add_website(self, url):
        # Check if the URL has already been added
        if url in self.visited_websites:
            print(f"[INFO] {url} is already in the queue. Skipping.")
        else:
            self.website_queue.put(url)
            self.visited_websites.add(url)  # Mark the URL as added
            print(f"[INFO] Added to queue: {url}")

    def check_status(self, url):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return f"[UP] {url} is online (Status Code: {response.status_code})"
            else:
                return f"[WARNING] {url} responded with code: {response.status_code}"
        except requests.exceptions.RequestException as error:
            return f"[DOWN] {url} is unreachable. Error: {error}"

    def write_log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {message}"
        with open(self.log_file, "a") as file:
            file.write(log_entry + "\n")
        print(log_entry)

    def run_monitoring(self, delay=5):
        print("\n[START] Website Monitoring (FCFS Scheduling)\n")
        if self.website_queue.empty():
            print("No websites to monitor.")
            return

        while not self.website_queue.empty():
            current_site = self.website_queue.get()
            status = self.check_status(current_site)
            self.write_log(status)
            time.sleep(delay)

        print("\n[END] Monitoring complete.\n")

    def get_websites_from_user(self, max_sites=5):
        print(f"Enter websites to monitor (type 'done' when finished, or stop after {max_sites} websites):")
        count = 0
        while count < max_sites:
            url = input("Website URL: ").strip()
            if url.lower() == 'done':
                print("Exiting website entry...")
                break
            elif url.startswith("http://") or url.startswith("https://"):
                self.add_website(url)
                count += 1
            else:
                print("Invalid URL format. Please use http:// or https://")
        
        if count == max_sites:
            print(f"Maximum of {max_sites} websites added. Stopping...")

if __name__ == "__main__":
    monitor = WebsiteMonitor()

    print("\n=== Automated Website Monitoring Scheduler ===")
    print("1. Use predefined websites")
    print("2. Enter websites manually\n")

    choice = input("Select option (1 or 2): ")

    if choice == '1':
        monitor.add_website("https://www.google.com")
        monitor.add_website("https://www.github.com")
        monitor.add_website("https://www.python.org")
        monitor.add_website("https://invalidwebsite1234.com")
    elif choice == '2':
        monitor.get_websites_from_user(max_sites=3)  # You can adjust this to your preference
    else:
        print("Invalid option. Exiting.")
        exit()

    delay_input = input("Enter delay time between checks (in seconds): ")
    try:
        delay = int(delay_input)
    except ValueError:
        print("Invalid input. Using default delay of 5 seconds.")
        delay = 5

    monitor.run_monitoring(delay=delay)