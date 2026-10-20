import sqlite3
import os

# ==========================================
# MÓDULO 1. CREACIÓN DE LA BASE DE DATOS
# ==========================================

def crear_bd():
    os.makedirs("database", exist_ok=True)

    conexion = sqlite3.connect("database/empresa_acme.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleado (
            curp TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            calle TEXT,
            colonia TEXT,
            telefono TEXT,
            edad INTEGER,
            sueldo_mensual REAL
        )
    """)

    conexion.commit()
    conexion.close()

    print("Base de datos de la empresa ACME creada correctamente.")


# ==========================================
# MÓDULO 2. ALTAS DE EMPLEADOS
# ==========================================

def alta_empleado():
    conexion = sqlite3.connect("database/empresa_acme.db")
    cursor = conexion.cursor()

    print("\n===== ALTA DE EMPLEADO (EMPRESA ACME) =====")

    curp = input("CURP: ").strip()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    calle = input("Calle: ").strip()
    colonia = input("Colonia: ").strip()
    telefono = input("Teléfono: ").strip()
    
    try:
        edad = int(input("Edad: ").strip())
    except ValueError:
        edad = 0

    try:
        sueldo_mensual = float(input("Sueldo mensual: ").strip())
    except ValueError:
        sueldo_mensual = 0.0

    if not curp or not nombre or not apellido:
        print("Error: CURP, nombre y apellido son obligatorios.")
        conexion.close()
        return

    try:
        cursor.execute("""
            INSERT INTO empleado (
                curp,
                nombre,
                apellido,
                calle,
                colonia,
                telefono,
                edad,
                sueldo_mensual
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            curp,
            nombre,
            apellido,
            calle,
            colonia,
            telefono,
            edad,
            sueldo_mensual
        ))

        conexion.commit()
        print("Empleado registrado correctamente.")

    except sqlite3.IntegrityError:
        print("Error: el CURP ya existe.")

    except sqlite3.Error as error:
        print(f"Error al registrar al empleado: {error}")

    finally:
        conexion.close()

# ==========================================
# ======= MÓDULO DE MODIFICACIONES  =========
# ==========================================

def modificar_empleado():
    conexion = sqlite3.connect("database/empresa_acme.db")
    cursor = conexion.cursor()

    print("\n====== MODIFICACIÓN DE EMPLEADO (EMPRESA ACME) ======")

    curp = input("Ingrese el CURP del empleado: ").strip()

    # Buscar al empleado
    cursor.execute("""
        SELECT nombre, apellido, calle, colonia,
               telefono, edad, sueldo_mensual
        FROM empleado
        WHERE curp = ?
    """, (curp,))

    empleado = cursor.fetchone()

    if empleado is None:
        print("Error: no se encontró un empleado con ese CURP.")
        conexion.close()
        return

    print("\nDatos actuales del empleado:")
    print("Nombre:", empleado[0])
    print("Apellido:", empleado[1])
    print("Calle:", empleado[2])
    print("Colonia:", empleado[3])
    print("Teléfono:", empleado[4])
    print("Edad:", empleado[5])
    print("Sueldo mensual:", empleado[6])

    print("\nIngrese los nuevos datos.")
    print("Presione ENTER para conservar el dato actual.")

    nombre = input(f"Nombre [{empleado[0]}]: ").strip()
    apellido = input(f"Apellido [{empleado[1]}]: ").strip()
    calle = input(f"Calle [{empleado[2]}]: ").strip()
    colonia = input(f"Colonia [{empleado[3]}]: ").strip()
    telefono = input(f"Teléfono [{empleado[4]}]: ").strip()
    
    nueva_edad = input(f"Edad [{empleado[5]}]: ").strip()
    nuevo_sueldo = input(f"Sueldo mensual [{empleado[6]}]: ").strip()

    # Conservar los datos si no se ingresaron cambios
    nombre = nombre if nombre else empleado[0]
    apellido = apellido if apellido else empleado[1]
    calle = calle if calle else empleado[2]
    colonia = colonia if colonia else empleado[3]
    telefono = telefono if telefono else empleado[4]
    
    try:
        edad = int(nueva_edad) if nueva_edad else empleado[5]
    except ValueError:
        edad = empleado[5]

    try:
        sueldo_mensual = float(nuevo_sueldo) if nuevo_sueldo else empleado[6]
    except ValueError:
        sueldo_mensual = empleado[6]

    try:
        cursor.execute("""
            UPDATE empleado
            SET nombre = ?,
                apellido = ?,
                calle = ?,
                colonia = ?,
                telefono = ?,
                edad = ?,
                sueldo_mensual = ?
            WHERE curp = ?
        """, (
            nombre,
            apellido,
            calle,
            colonia,
            telefono,
            edad,
            sueldo_mensual,
            curp
        ))

        conexion.commit()
        print("\nEmpleado modificado correctamente.")

    except sqlite3.Error as error:
        conexion.rollback()
        print("Error al modificar el empleado:", error)

    finally:
        conexion.close()

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    crear_bd()
    alta_empleado()
    modificar_empleado()