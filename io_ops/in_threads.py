import time
from threading import Thread
import requests


def task():
    r = requests.get('https://api.covidtracking.com/v1/us/current.json')

def main():
    threads = [Thread(target=task) for _ in range(10)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    begin = time.time()
    main()
    print(f"duration: {time.time() - begin}")