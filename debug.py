from threading import Thread, current_thread
from time import sleep

def main():
    threads = []
    try:
        element_count = 6
        for element in range(0, element_count):
            thread = Thread(target = do_something, args=(element, element_count))
            thread.start()
    except KeyboardInterrupt as e:
        for thread in threads:
            thread.alive = False
            thread.join()
        exit(e)

def do_something(element: int, element_count: int):
    thread = current_thread()
    thread.alive = True
    while thread.is_alive():
        try:
            thread.join(0.5)
        print(f"[Thread: {element}/{element_count}] started doing something")
        sleep(2)
        print(f"[Thread: {element}/{element_count}] stopped doing something")

if __name__ == "__main__":
	main()