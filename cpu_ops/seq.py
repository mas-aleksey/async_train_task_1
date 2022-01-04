import time


def countdown():
    i = 0
    while i < 5_000_000:
        i += 1


def main():
    for _ in range(10):
        countdown()



if __name__ == "__main__":
    begin = time.time()
    main()
    print(f"duration: {time.time() - begin}")
