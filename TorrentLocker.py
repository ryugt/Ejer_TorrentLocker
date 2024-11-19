from math import gcd  # Importa la función gcd (Máximo Común Divisor) del módulo math
from functools import reduce  # Importa la función reduce del módulo functools
from collections import Counter  # Importa la clase Counter del módulo collections

def file_to_hex(file_path):
    # Abre el archivo en modo binario y lee su contenido
    with open(file_path, 'rb') as file:
        byte_data = file.read()
    # Convierte los datos binarios a una cadena hexadecimal
    hex_data = byte_data.hex()
    return hex_data  # Devuelve la cadena hexadecimal

def find_repeated_blocks(hex_data, min_size):
    repeated_blocks = {}  # Diccionario para almacenar bloques repetidos y sus posiciones
    # Probar diferentes tamaños de bloque desde 2 hasta min_size
    for block_size in range(2, min_size):
        # Iterar sobre la cadena hexadecimal para encontrar bloques repetidos
        for i in range(len(hex_data) - block_size + 1):
            block = hex_data[i:i + block_size]  # Extraer un bloque de tamaño block_size
            if block in repeated_blocks:
                repeated_blocks[block].append(i)  # Agregar la posición si el bloque ya existe
            else:
                repeated_blocks[block] = [i]  # Crear una nueva entrada para el bloque
    # Filtrar y devolver solo los bloques que se repiten más de dos veces
    return {block: positions for block, positions in repeated_blocks.items() if len(positions) > 2}

def calculate_mcd(positions):
    if len(positions) < 3:
        return None  # No hay suficiente información para calcular el MCD
    # Calcular las distancias entre posiciones consecutivas
    distances = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
    # Calcular y devolver el MCD de las distancias
    return reduce(gcd, distances)

def process_repeated_blocks(hex_data, min_size):
    repeated_blocks = find_repeated_blocks(hex_data, min_size)  # Encontrar bloques repetidos
    mcd_counter = Counter()  # Crear un contador para los MCD
    # Iterar sobre los bloques repetidos y sus posiciones
    for block, positions in repeated_blocks.items():
        mcd = calculate_mcd(positions)  # Calcular el MCD de las posiciones
        if mcd is not None and mcd > 1:  # Ignorar MCD = 1
            mcd_counter[mcd] += 1  # Incrementar el contador para el MCD
    if mcd_counter:
        most_common_mcd, count = mcd_counter.most_common(1)[0]
    return most_common_mcd

def split_into_blocks(hex_data, block_size):
    # Dividir los datos hexadecimales en bloques del tamaño especificado
    return [hex_data[i:i + block_size] for i in range(0, len(hex_data), block_size)]

def find_most_repeated_pattern(blocks):
    pattern_counter = Counter(blocks)  # Contar la frecuencia de cada bloque
    most_common_pattern, count = pattern_counter.most_common(1)[0]  # Obtener el patrón más común y su cuenta
    return most_common_pattern, count  # Devolver el patrón más común y su cuenta

def xor_hex_data(hex_data, key):
    key_bytes = bytes.fromhex(key)  # Convertir la clave de hexadecimal a bytes
    hex_bytes = bytes.fromhex(hex_data)  # Convertir los datos hexadecimales a bytes
    # Realizar la operación XOR entre los datos y la clave
    xor_result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(hex_bytes)])
    return xor_result.hex()  # Devolver el resultado en formato hexadecimal

def save_hex_to_xlsx(hex_data, file_path):
    # Guardar los datos hexadecimales en un archivo .xlsx
    with open(file_path, 'wb') as file:
        file.write(bytes.fromhex(hex_data))

# Obtener los nombres de los archivos del usuario
file_path1 = "video.docx.enc"
file_path2 = "claves.xlsx.enc"
file_path3 = "datos.pptx.enc"

# Leer los datos de los archivos y convertirlos a hexadecimal
hex_data1 = file_to_hex(file_path1)
hex_data2 = file_to_hex(file_path2)
hex_data3 = file_to_hex(file_path3)

# Calcular el tamaño de los archivos en bytes
size1 = len(hex_data1) 
size2 = len(hex_data2) 
size3 = len(hex_data3) 

# Determinar el menor tamaño
min_size = int(abs(min(size1, size2, size3)/512))

# Procesar y mostrar los bloques repetidos y MCD para cada archivo
key_length = int((process_repeated_blocks(hex_data1, min_size) + process_repeated_blocks(hex_data2, min_size) + process_repeated_blocks(hex_data3, min_size))/3)
print(f"\nLa clave de cifrado es el MCD de los MCD más comunes de los bloques repetidos, cuyo valor es.:{key_length}")
blocks = split_into_blocks(hex_data2, key_length)
most_common_pattern, count = find_most_repeated_pattern(blocks)
print(f"\nLa clave de encryptacion mas probable es: {most_common_pattern} con {count} ocurrencias")
# Realizar la operación XOR con hex_data2 y most_common_pattern
xor_result = xor_hex_data(hex_data2, most_common_pattern)
# Guardar el resultado en un archivo .xlsx
output_file_path = "resultado.xlsx"
save_hex_to_xlsx(xor_result, output_file_path)
print(f"\nEl resultado de la operación XOR se ha guardado en: {output_file_path}")