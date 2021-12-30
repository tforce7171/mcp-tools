import os
import subprocess

def server_init():
    commands = get_commands()
    for command in commands:
        subprocess.run(command.split(' '))

def get_commands():
    commands_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './commands'))
    with open(commands_path+'/init_server.txt', 'r') as f:
        commands = f.read().split('\n')
        commands.remove('')
        for command in commands:
            if command[0] == '#':
                commands.remove(command)
    return commands

if __name__ == '__main__':
    server_init()
