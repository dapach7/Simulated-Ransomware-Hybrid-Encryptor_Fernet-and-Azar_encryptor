# 🛡️ Fernet_+_Azar_encryptor – Educational Ransomware Project
# 🛡️ Fernet_+_Azar_cifrado – Proyecto de Ramsonware educativo

### ⚠️ For Educational Purposes Only
### ⚠️ Solo para uso EDUCATIVO

---

## 📌 Description (English)

**Fernet_+_Azar_encryptor** is an educational project that demonstrates a double-layer encryption system:

- **Layer 1:** Standard encryption using [Fernet](https://cryptography.io/en/latest/fernet/) (symmetric encryption).
- **Layer 2:** A custom random substitution cipher (`Azar_encryptor.py`) that randomly obfuscates byte data.

The system is capable of encrypting files in any user-specified directory. In this demonstration, the **Desktop** and **Documents** folders were used as examples, but this path can be easily modified to target other directories. The script sends encryption metadata to a **designated email** for secure storage and optionally creates a ransom note.

---

## 📌 Descripción (Español)

**Fernet_+_Azar_encryptor** es un proyecto educativo que demuestra un sistema de cifrado en dos capas:

- **Capa 1:** Cifrado estándar con [Fernet](https://cryptography.io/en/latest/fernet/) (cifrado simétrico).
- **Capa 2:** Un cifrado personalizado de sustitución aleatoria (`Azar_encryptor.py`) que ofusca los datos byte por byte.

El sistema puede cifrar archivos en cualquier directorio que el usuario especifique. En esta demostración se usaron las carpetas **Escritorio** y **Documentos** como ejemplo, pero el código puede modificarse fácilmente para apuntar a cualquier otra ubicación. El script envía los metadatos de cifrado a un **correo electrónico designado** y opcionalmente crea una nota de rescate.

---

## 📁 Files / Archivos

| File Name                    | Description (EN)                            | Descripción (ES)                                              |
| ---------------------------- | ------------------------------------------- | ------------------------------------------------------------- |
| `Azar_encryptor.py`          | Custom random byte substitution cipher      | Cifrado personalizado por sustitución aleatoria               |
| `Fernet_+_Azar_encryptor.py` | Encrypts files using Fernet + custom cipher | Cifra archivos con Fernet + cifrado personalizado             |
| `Fernet_+_Azar_decryptor.py` | Decrypts files using key + metadata         | Descifra archivos con clave y metadatos previamente guardados |

---

## 🔐 Encryption Workflow / Flujo de Cifrado

### English:

1. Scans Desktop and Documents for files (or any user-defined path).
2. Each file is encrypted:
   - First using **Fernet (AES)**.
   - Then with a **custom randomized byte cipher**.
3. The resulting encryption metadata is stored in a `.json.gz` file.
4. The metadata is sent via email to a **designated storage account**.
5. A `.key` file containing the Fernet key is saved locally.
6. An optional ransom note (`LEEME.txt`) is created.

### Español:

1. Escanea las carpetas Escritorio y Documentos (o cualquier ruta definida por el usuario).
2. Cada archivo es cifrado:
   - Primero usando **Fernet (AES)**.
   - Luego con un **cifrado personalizado aleatorio de bytes**.
3. Los metadatos resultantes se almacenan en un archivo `.json.gz`.
4. Los metadatos se envían por correo a una **cuenta de almacenamiento designada**.
5. Un archivo `.key` con la clave Fernet se guarda localmente.
6. Se crea una nota de rescate opcional (`LEEME.txt`).

## 🔓 Decryption Workflow / Flujo de Descifrado

### English:

1. Place all received `.json.gz` metadata files into a folder named **Claves** on your Desktop.
2. Run `Fernet_+_Azar_decryptor.py`.
3. The script will:
   - Locate the original file.
   - Use the `.key` file and `.json.gz` metadata.
   - Reverse the custom cipher.
   - Decrypt with Fernet.
4. The decrypted file is saved with `_descifrado` appended to its name.

### Español:

1. Coloca todos los archivos `.json.gz` recibidos en una carpeta llamada **Claves** en tu Escritorio.
2. Ejecuta `Fernet_+_Azar_decryptor.py`.
3. El script hará lo siguiente:
   - Ubicará el archivo original.
   - Utilizará el archivo `.key` y los metadatos `.json.gz`.
   - Invertirá el cifrado personalizado.
   - Descifrará usando Fernet.
4. El archivo descifrado se guardará con `_descifrado` añadido a su nombre.

---

## ⚠️ Legal & Ethical Notice / Aviso Legal y Ético

> This project is for **educational and research purposes only**.\
> Do **not** use this software to encrypt devices or data without **explicit consent** from the owner.

> Este proyecto es solo con fines **educativos y de investigación**.\
> **No uses** este software para cifrar datos o equipos sin el **consentimiento explícito** de su propietario.

---

## ✅ Requirements / Requisitos

- Python 3.8+
- Required libraries:

```bash
pip install cryptography
```

Also uses built-in modules:

- `os`
- `json`
- `gzip`
- `hashlib`
- `tempfile`
- `pathlib`
- `smtplib`
- `ssl`
- `email`
- `random`

---
**🛠️ VARIABLES QUE DEBES MODIFICAR EN EL CÓDIGO / VARIABLES YOU MUST EDIT IN THE CODE**

## ✉️ Email Configuration / Configuración del Correo

> **NOTE / NOTA:** You can use the same email for both `CORREO_REMITENTE` and `CORREO_DESTINATARIO` if you want to store the `.json.gz` files in the same Gmail account that sends them. 
> Puedes usar el mismo correo para `CORREO_REMITENTE` y `CORREO_DESTINATARIO` si deseas almacenar los archivos `.json.gz` en la misma cuenta de Gmail que los envía.

### English:

In `Fernet_+_Azar_encryptor.py`, set the following variables:

```python
CORREO_REMITENTE = "your_sender_email@gmail.com"
CLAVE_APP = "your_gmail_app_password"
CORREO_DESTINATARIO = "your_storage_email@gmail.com"
```

- `CORREO_REMITENTE`: the Gmail address used to send the encryption metadata.
- `CLAVE_APP`: the [App Password](https://support.google.com/accounts/answer/185833?hl=en) Generated from the Gmail account that will send the .json.gzip files.
- `CORREO_DESTINATARIO`: the destination email where the `.json.gz` metadata will be sent and stored.

Make sure `CORREO_REMITENTE` has **2-Step Verification enabled** and use an **App Password**, not your normal login password.


### Español:

En el archivo `Fernet_+_Azar_encryptor.py`, configura las siguientes variables:

- `CORREO_REMITENTE`: la dirección Gmail usada para enviar los metadatos del cifrado.
- `CLAVE_APP`: la [contraseña de aplicación](https://support.google.com/accounts/answer/185833?hl=es) generada desde la cuenta Gmail que enviara los archivos .json.gzip.
- `CORREO_DESTINATARIO`: el correo destino donde se enviarán y almacenarán los metadatos en formato `.json.gz`.

Asegúrate de que `CORREO_REMITENTE` tenga activada la **verificación en dos pasos** y utiliza una **contraseña de aplicación**, no tu contraseña habitual.

🚀 Deployment / Despliegue ( https://www.youtube.com/watch?v=huXS9gZfoX8&t=45s&ab_channel=DazzaLuis )

English:

To demonstrate the functionality of the encryption script, PyInstaller was used to convert it into a standalone .exe file. This allows the file to be executed on systems without Python installed.

**Only the encryption script was compiled as an executable for demonstration purposes.**

Other tools for turning Python scripts into executables include:

- cx_Freeze

- auto-py-to-exe (a GUI for PyInstaller)

- Nuitka (compiles to C for performance)

Español:

Para demostrar el funcionamiento del script de cifrado, se utilizó PyInstaller para convertirlo en un archivo .exe independiente. Esto permite ejecutar el archivo en sistemas sin necesidad de tener Python instalado.

**Solo se compiló el script de cifrado como ejecutable con fines demostrativos.**

Otras herramientas para convertir scripts de Python en ejecutables son:

- cx_Freeze

- auto-py-to-exe (una interfaz gráfica para PyInstaller)

- Nuitka (compila a C para mejorar el rendimiento)
---

