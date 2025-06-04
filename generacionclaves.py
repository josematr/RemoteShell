from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open("clave.key", "wb") as archivo_clave:
    archivo_clave.write(key)

print(" Clave generada y guardada en clave.key")
