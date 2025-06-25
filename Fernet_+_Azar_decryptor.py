import os
import json
import gzip
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet
from Azar_encryptor import descifrado_de_azar_binario

# === Utility Functions ===

# Returns the target folders to scan for encrypted files
def obtener_rutas_objetivo():
    home = Path.home()
    return [home / "Desktop", home / "Documents"]

# Generates a unique filename identifier using MD5 hash of the file path
# Ensures consistency with the names used during encryption
def generar_nombre_unico(path: Path):
    hash_ruta = hashlib.md5(str(path).encode()).hexdigest()[:6]
    return f"{path.stem}_{hash_ruta}"

# Loads the .json.gz metadata file from the "Claves" folder (Desktop)
def cargar_json_desde_claves(nombre_unico):
    # Path to the folder where all received .json.gz metadata files must be stored.
    # IMPORTANT: You must manually create a folder named "Claves" on your Desktop
    # and save there all the .json.gz files sent to your storage email.
    claves_dir = Path.home() / "Desktop" / "Claves"
    json_path = claves_dir / f"{nombre_unico}_meta.json.gz"
    if json_path.exists():
        with gzip.open(json_path, "rt", encoding="utf-8") as f:
            return json.load(f)
    return None

# === Main function to decrypt a single file ===

def descifrar_archivo(archivo_path: Path):
    try:
        nombre_unico = generar_nombre_unico(archivo_path)

        # Expected file paths for key and metadata
        clave_path = archivo_path.with_name(nombre_unico + "_clave.key")
        json_path = Path.home() / "Desktop" / "Claves" / f"{nombre_unico}_meta.json.gz"

        # Check if required decryption files exist
        if not clave_path.exists():
            print(f"[!] Missing key: {clave_path.name}")
            return

        if not json_path.exists():
            print(f"[!] Missing JSON metadata in 'Claves' folder for: {archivo_path.name}")
            return

        # Load metadata from the gzip file
        with gzip.open(json_path, "rt", encoding="utf-8") as f:
            meta = json.load(f)

        # Load the encrypted data
        with open(archivo_path, "rb") as f:
            datos_cifrados = f.read()

        # Load the Fernet key
        with open(clave_path, "rb") as f:
            clave = f.read()

        # Build the data structure expected by the custom decryption function
        resultado = {
            "cifrado": datos_cifrados,
            "nuevo_alfabeto": meta["nuevo_alfabeto"],
            "desplazamientos": meta["desplazamientos"],
            "abc_base": meta["abc_base"],
            "correo": "not_needed"
        }

        # First, apply the custom random decryption
        datos_fernet = descifrado_de_azar_binario(resultado)

        # Then, decrypt the Fernet-encrypted content
        fernet = Fernet(clave)
        datos_originales = fernet.decrypt(datos_fernet)

        # Save the decrypted file with "_descifrado" suffix
        salida = archivo_path.with_name(archivo_path.stem + "_descifrado" + archivo_path.suffix)
        with open(salida, "wb") as f:
            f.write(datos_originales)

        print(f"[✔] Decrypted: {archivo_path.name} → {salida.name}")

        # Optional cleanup: remove encrypted file, key and metadata
        archivo_path.unlink(missing_ok=True)  # Delete encrypted file
        clave_path.unlink(missing_ok=True)    # Delete key file
        json_path.unlink(missing_ok=True)     # Delete metadata file

        print(f"[🧹] Cleaned up: {archivo_path.name}, {clave_path.name}, {json_path.name}")

    except Exception as e:
        print(f"[✘] Error decrypting {archivo_path.name}: {e}")

# Scans the target directories and attempts to decrypt all files found
def descifrar_todos():
    for ruta in obtener_rutas_objetivo():
        if ruta.exists():
            for archivo in ruta.rglob("*"):
                if archivo.is_file() and not archivo.name.endswith("_clave.key"):
                    descifrar_archivo(archivo)

# Entry point of the script
if __name__ == "__main__":
    descifrar_todos()