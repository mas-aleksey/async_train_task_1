import time
import requests


def main():
    for _ in range(10):
        r = requests.get('https://api.covidtracking.com/v1/us/current.json')
        print(len(r.text))


if __name__ == "__main__":
    begin = time.time()
    main()
    print(f"duration: {time.time() - begin}")
