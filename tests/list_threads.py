import threading

def list_threads():
    threads = threading.enumerate()
    print("Active Threads:")
    for thread in threads:
        print(thread.name)

if __name__ == "__main__":
    list_threads()
