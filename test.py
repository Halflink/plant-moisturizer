import threading
import time


def thread_function(thread_name):
    print('start thread ' + str(thread_name))
    time.sleep(10)
    print('end thread')


if __name__ == "__main__":
    test_thread = threading.Thread(target=thread_function, args=(2,))
    test_thread.start()
    for i in range(20):
        print('count ' + str(i))
        time.sleep(2)
