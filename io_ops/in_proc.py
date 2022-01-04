import time
import multiprocessing
import requests


def task():
    r = requests.get('https://api.covidtracking.com/v1/us/current.json')
    return len(r.text)

def main():
    PROCESSES_COUNT = 10
    with multiprocessing.Pool(PROCESSES_COUNT) as pool:
        results = list()
        for _ in range(PROCESSES_COUNT):
            results.append(pool.apply_async(task))
        
        for r in results:
            p = r.get()


if __name__ == "__main__":
    begin = time.time()
    main()
    print(f"duration: {time.time() - begin}")