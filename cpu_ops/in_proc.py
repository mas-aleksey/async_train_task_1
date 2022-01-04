import time
import multiprocessing


def countdown():
    i = 0
    while i < 5_000_000:
        i += 1


def main():
    PROCESSES_COUNT = 10
    with multiprocessing.Pool(PROCESSES_COUNT) as pool:
        results = list()
        for _ in range(PROCESSES_COUNT):
            results.append(pool.apply_async(countdown))
        
        for r in results:
            p = r.get()


if __name__ == "__main__":
    begin = time.time()
    main()
    print(f"duration: {time.time() - begin}")