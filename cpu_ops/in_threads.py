import time
from threading import Thread


def countdown():
    i = 0
    while i < 5_000_000:
        i += 1


def main():
    threads = [Thread(target=countdown) for _ in range(10)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()



if __name__ == "__main__":
    begin = time.time()
    main()
    print(f"duration: {time.time() - begin}")