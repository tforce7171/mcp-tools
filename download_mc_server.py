import sys
import os
import json
import subprocess

def download_mc_server(command):
    if command == '-l' or command == 'list':
        _list()
    elif command == '-s' or command == 'server':
        server_name = sys.argv[2]
        # _download(server_name)
        _initialize(server_name)
    elif command == '-i' or command == 'interactive':
        _list()
        server_name = input('choose the desired mc server version')
        _download(server_name)
    return

def _list():
    server_urls = load_server_urls()
    for server_url in server_urls:
        print(server_url)

def _download(server_name):
    server_urls = load_server_urls()
    if server_name in server_urls:
        try:
            os.makedirs(f'{os.environ["HOME"]}/temp/{server_name}')
        except FileExistsError:
            print("folder already exists")
        subprocess.run(f'curl -LSo {os.environ["HOME"]}/temp/{server_name}/{server_name}.jar {server_urls[server_name]}'.split(' '))
    else:
        print('no matching mc server')

def _initialize(server_name):
    subprocess.run(f'java -Xmx1024M -Xms1024M -jar {os.environ["HOME"]}/temp/{server_name}/{server_name}.jar nogui'.split(' '), cwd=f'{os.environ["HOME"]}/temp/{server_name}')
    with open(f'{os.environ["HOME"]}/temp/{server_name}/eula.txt', 'w') as f:
        f.write('eula=true')

def load_server_urls():
    configs_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../configs/'))
    with open(configs_path+'/vanilla_server_urls.json', 'r') as f:
        server_urls = json.load(f)
    return server_urls

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('command not provided')
    else:
        download_mc_server(sys.argv[1])
