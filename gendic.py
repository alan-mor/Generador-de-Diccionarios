import itertools
import os
import sys
import time
from tqdm import tqdm

def estimate_size(charset, length):
    num_words = len(charset) ** length
    size_in_bytes = num_words * (length + 1)  # +1 for newline character
    return num_words, size_in_bytes

def format_size(size_in_bytes):
    size_units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    unit_index = 0
    while size_in_bytes >= 1024 and unit_index < len(size_units) - 1:
        size_in_bytes /= 1024
        unit_index += 1
    return f"{size_in_bytes:.2f} {size_units[unit_index]}"

def format_time(minutes):
    units = [("año", 525600), ("mes", 43200), ("semana", 10080), ("día", 1440), ("hora", 60), ("minuto", 1)]
    for unit, factor in units:
        amount, _ = divmod(minutes, factor)
        if amount > 0:
            return f"{amount:.0f} {unit}{'s' if amount > 1 else ''}"
    return "0 minutos"

def generate_dictionary(filename, charset, length):
    num_words = len(charset) ** length
    with open(filename, 'w') as f:
        for word in tqdm(itertools.product(charset, repeat=length), total=num_words, desc="Generando"):
            f.write(''.join(word) + '\n')

def main():
    print("Generación de diccionario interactivo\n")
    
    charset = ""
    
    print("Selecciona el tipo de caracteres:")
    print("1) Hexadecimales")
    print("2) Letras")
    print("3) Números")
    print("4) Personalizado")
    
    data_type = input("Elige una opción (1/2/3/4): ").strip()
    
    if data_type == '1':
        hex_case = input("¿Usar hexadecimales en mayúsculas, minúsculas o ambos? (M/m/A): ").strip().lower()
        if hex_case == 'm':
            charset = "0123456789abcdef"
        elif hex_case == 'M':
            charset = "0123456789ABCDEF"
        elif hex_case == 'a':
            charset = "0123456789abcdefABCDEF"
        else:
            print("Opción inválida. Abortando.")
            sys.exit(1)
    elif data_type == '2':
        if input("¿Incluir minúsculas? (S/N): ").strip().lower() == 's':
            charset += "abcdefghijklmnopqrstuvwxyz"
        if input("¿Incluir mayúsculas? (S/N): ").strip().lower() == 's':
            charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    elif data_type == '3':
        charset = "0123456789"
    elif data_type == '4':
        if input("¿El diccionario incluirá minúsculas? (S/N): ").strip().lower() == 's':
            charset += "abcdefghijklmnopqrstuvwxyz"
        if input("¿El diccionario incluirá mayúsculas? (S/N): ").strip().lower() == 's':
            charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if input("¿El diccionario incluirá números? (S/N): ").strip().lower() == 's':
            charset += "0123456789"
        if input("¿El diccionario incluirá caracteres especiales? (S/N): ").strip().lower() == 's':
            charset += "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"
    else:
        print("Opción inválida. Abortando.")
        sys.exit(1)
    
    if not charset:
        print("No se han seleccionado caracteres. Abortando.")
        sys.exit(1)
    
    try:
        length = int(input("Escribe la extensión del diccionario deseado: ").strip())
    except ValueError:
        print("Longitud inválida. Abortando.")
        sys.exit(1)
    
    num_words, size_in_bytes = estimate_size(charset, length)
    estimated_time_minutes = num_words / 1000000  # Assuming 1 million words per minute generation rate
    
    print(f"\nEl diccionario que se generará contendrá aproximadamente {num_words} palabras.")
    print(f"Se estima que tendrá un peso de {format_size(size_in_bytes)} y tardará aproximadamente {format_time(estimated_time_minutes)} en generarse.")
    print(f"Un ataque con este diccionario podría demorar {format_time(estimated_time_minutes * 2)} (asumiendo 500k intentos por minuto).")
    
    if input("¿Deseas continuar? (S/N): ").strip().lower() != 's':
        print("Operación cancelada por el usuario.")
        sys.exit(0)
    
    filename = input("Introduce el nombre del archivo de salida (con extensión .txt): ").strip()
    if not filename.endswith(".txt"):
        filename += ".txt"
    
    print("Generando diccionario...")
    start_time = time.time()
    generate_dictionary(filename, charset, length)
    end_time = time.time()
    
    print(f"Diccionario generado en {end_time - start_time:.2f} segundos.")
    print(f"Archivo guardado como {filename}.")

if __name__ == "__main__":
    main()
