import random

# Encrypts a single byte using a random displacement over a shuffled alphabet
def cifrar_byte(byte_val, abc_base, nuevo_abc):
    # Find the byte's position in the shuffled base alphabet
    pos = abc_base.index(byte_val)

    # Generate a random displacement between 1 and 9
    desplazamiento = random.randint(1, 9)

    # Create a block of encrypted bytes based on the new alphabet
    bloque = bytearray()
    for i in range(desplazamiento):
        # Shift forward from the original position, wrapping around if needed
        idx = (pos + i) % len(nuevo_abc)
        bloque.append(nuevo_abc[idx])

    # Return the encrypted block and the number of bytes used
    return bloque, desplazamiento

# Encrypts a full sequence of bytes using a random substitution cipher
def cifrado_de_azar_binario(data_bytes, correo_destinatario):
    # Generate a base alphabet of all byte values from 0 to 255 and shuffle it
    abc_base = list(range(256))
    random.shuffle(abc_base)

    # Create a new random alphabet of the same length
    nuevo_abc = random.sample(range(256), len(abc_base))

    mensaje_cifrado = bytearray()     # The final encrypted message
    desplazamientos = []              # List to record block lengths per byte

    # Iterate through each byte in the input data
    for byte_val in data_bytes:
        if byte_val in abc_base:
            # Encrypt the byte and get the corresponding block and length
            bloque, desplaz = cifrar_byte(byte_val, abc_base, nuevo_abc)
            mensaje_cifrado.extend(bloque)
            desplazamientos.append(desplaz)
        else:
            # In rare cases (e.g. invalid byte), leave as-is
            mensaje_cifrado.append(byte_val)
            desplazamientos.append(0)

    # Return a dictionary containing all necessary information for decryption
    return {
        "cifrado": bytes(mensaje_cifrado),
        "nuevo_alfabeto": nuevo_abc,
        "desplazamientos": desplazamientos,
        "correo": correo_destinatario,  # Optional, informational field
        "abc_base": abc_base
    }

# Decrypts a message produced by cifrado_de_azar_binario()
def descifrado_de_azar_binario(resultado_cifrado):
    # Extract encrypted content and parameters
    cifrado = resultado_cifrado["cifrado"]
    desplazamientos = resultado_cifrado["desplazamientos"]
    nuevo_abc = resultado_cifrado["nuevo_alfabeto"]
    abc_base = resultado_cifrado["abc_base"]

    mensaje_descifrado = bytearray()  # The reconstructed original message
    idx = 0  # Current position in the encrypted data

    # Process each recorded block length
    for desplaz in desplazamientos:
        if desplaz == 0:
            # If the byte wasn't encrypted, read it directly
            mensaje_descifrado.append(cifrado[idx])
            idx += 1
        else:
            # Extract the block and get the first byte as reference
            bloque = cifrado[idx:idx + desplaz]
            idx += desplaz

            primer_byte = bloque[0]

            # Find its position in the new alphabet and recover the original byte
            if primer_byte in nuevo_abc:
                pos = nuevo_abc.index(primer_byte)
                mensaje_descifrado.append(abc_base[pos])

    return bytes(mensaje_descifrado)