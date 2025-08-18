import threading
import time
def thread_func(self):
    urls = [
        f"https://www.newsmth.net/nForum/mainpage?ajax"
    ]

    threads = []  # 存放列表

    for url in urls:
        threads.append(threading.Thread(target =self.craw ,args= (url,))) # 创建子进程，并指定相关函数
        time.sleep(0.1)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()