import subprocess as sp
import readline
import os

HISTFILE = os.path.expanduser("~/.mysh_history")

if os.path.exists(HISTFILE):
    readline.read_history_file(HISTFILE)

if os.name == "nt":  # Windows
    ls_cmd, clear_cmd = "dir", "cls"
    home, user = "USERPROFILE", "USERNAME"
else:
    ls_cmd, clear_cmd = "ls", "clear"
    home, user = "HOME", "USER"


while True:
    try:
        # Prompt shows current directory name
        prompt = os.path.basename(os.getcwd())
        command = input(f"[{prompt}] mysh> ")
        commands = command.split()
        
        if not commands:
            continue
        if ">" in commands:
            new_command, filename = command.split(" > ") 
            with open(filename, "w") as file:
                sp.Popen(new_command, stdout=file, shell=True).communicate()
            continue
        if commands[0] == "exit":
            break
        elif commands[0] == "ls":
            if len(commands) == 1:
                sp.run(ls_cmd, shell=True)
            else:
                sp.run(f"{ls_cmd} {commands[1]}", shell=True)
        elif commands[0] == "pwd":
            print(os.getcwd())
        elif commands[0] == "cd":
            try:
                os.chdir(commands[1])
            except IndexError:
                print("cd: missing argument")
            except FileNotFoundError:
                print(f"cd: no such file or directory: {commands[1]}")
        elif commands[0] == "echo":
            if commands[1] == "$HOME":
                print(os.environ.get(home))
            elif commands[1] == "$USER":
                print(os.environ.get(user))
            elif commands[1][0] == "$":
                print(os.environ.get(commands[1][1:]))
            else:
                print(commands[1])
        elif commands[0] == "export":
            try:
                key, value = commands[1].split("=")
                os.environ[key] = value
            except:
                print("Invalid key or command. Sample: [export KEY=VALUE]")
        elif commands[0] == "clear":
            os.system(clear_cmd)
        else:
            sp.run(commands, shell=True)
    except KeyboardInterrupt:
        print("\nUse 'exit' to quit.")
    except Exception as e:
        print(f"Error: {e}")

readline.write_history_file(HISTFILE)

