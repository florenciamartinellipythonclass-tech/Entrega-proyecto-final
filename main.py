from utils.helpers import *
from utils import db_manager
import sys

def mostrar_tabla(productos):
    if not productos:
        print("no se encontraron productos.")
        return
    
    print(f"{'ID':<5} {'NOMBRE':<20} {'CATEGORIA':<15} {'PRECIO':<10} {'CANTIDAD':<10} {'DESCRIPCION':<15}")
    print("-" * 65)
    for prod in productos:
         print(f"{prod[0]:<5} {prod[1][:18]:<20} {prod[5][:13]:<15} ${prod[4]:<9.2f} {prod[3]:<10} {prod[2]:<15}")
    print("-" * 65)

# Creación del menu para registro
def menu_registrar():
    imprimir_titulo("Registrar nuevo producto")
    nombre = validar_input_string("Ingrese el nombre del producto: ")
    descripcion = validar_input_string("Ingrese la descripcion del producto (opcional): ")
    cantidad = validar_input_int("Ingrese cantidad inicial: ")
    precio = validar_input_float("Ingrese el precio (sin centavos): ")
    categoria = validar_input_string("Ingrese la categoría del producto: ")

    if db_manager.crear_producto(nombre,descripcion,cantidad,precio,categoria):
        imprimir_exito("Producto registrado correctamente.")
    
def menu_mostrar():
    imprimir_titulo("Listado de productos")
    productos = db_manager.obtener_producto()
    mostrar_tabla(productos)
    
def menu_actualizar():
    imprimir_titulo("Actualizar producto")
    
    id_prod = validar_input_int("Ingrese el Id del producto a modificar: ")
    
    producto_actual = db_manager.buscar_producto_id(id_prod)
    if not producto_actual:
        imprimir_error("Producto no encontrado.")
        return
    
    print(f"Editando: {producto_actual[1]}")
    print("Deje vacio el campo a no modificar")
    
    nuevo_nombre = input(f"Nombre [{producto_actual[1]}]: ").strip() or producto_actual[1] 
    nueva_descripcion = input(f"Descripcion [{producto_actual[2]}]: ").strip() or producto_actual[2]
    cant_str = input(f"Cantidad [{producto_actual[3]}]: ").strip()
    nueva_cantidad = int(cant_str) if cant_str.isdigit() else producto_actual[3]
    precio_str = input(f"Precio [{producto_actual[4]}]: ").strip()
    nuevo_precio= float(precio_str) if precio_str else producto_actual[4]
    nueva_categoria = input(f"Categoria [{producto_actual[5]}]: ").strip() or producto_actual[5]
    
    if db_manager.actualizar_producto(id_prod,nuevo_nombre,nueva_descripcion,nueva_cantidad,nuevo_precio,nueva_categoria):
        imprimir_exito("Producto actualizado exitosamente.")

    else:
        imprimir_error("No puedo actualizarse.")

def menu_eliminar():
    imprimir_titulo("Eliminar producto")
    menu_mostrar() #mostramos para que se sepa el ID a eliminar
    
    id_prod = validar_input_int("ID de producto a eliminar")
    
    #confirmación
    confirm = input(f"¿Seguro que desea eliminar el ID {id_prod}? (s/n): ").lower()
    if confirm == "si":
        if db_manager.eliminar_producto(id_prod):
            imprimir_exito("Producto eliminado.")
    else:
        imprimir_error("No se encontró el ID seleccionado")

def menu_buscar():
    imprimir_titulo("Buscar producto")
    print("1. Buscar por ID")
    print("2. Buscar por nombre o categoria")
    opcion = input("Opción: ")
    
    if opcion == "1":
        id_prod = validar_input_int("ID")
        res = db_manager.buscar_producto_id(id_prod)
        if res:
            mostrar_tabla(res)
        else:
            imprimir_error("Producto no encontrado.")
    elif opcion == "2":
        termino = validar_input_string("Termino de busqueda")
        res = db_manager.buscar_producto_texto(termino)
        mostrar_tabla(res)
    else:
        imprimir_error("No es una opcion valida")
        

def menu_reporte():
    imprimir_titulo("Reporte de baja de stock")
    limite = validar_input_int("Ingrese cantidad limite para alerta")
    res = db_manager.informe_baja_stock(limite)
    if res:
        imprimir_exito(f"Se encontraron {len(res)} productos con stock <= {limite}")
        mostrar_tabla(res)
    else:
        imprimir_exito("Los productos están dentro de los limites establecidos")
        

def main():
    # Asegurar que la DB existe
    db_manager.inicializar_db()
    
    while True:
        # Limpiar pantalla() # Desconectar si quiere que se limpie en cada ciclo
        print("\n" + "="*30)
        print( "    GESTION DE INVENTARIO")
        print("="*30)
        print("1. Agregar producto")
        print("2. Visualizar productos")
        print("3. Actualizar Producto")
        print("4. Buscar producto por nombre")
        print("5. Eliminar producto por número")
        print("6. Reporte Baja Producto")
        print("7. Salir")
        
        opcion = input("\nSeleccionar opción: ")
        
        if opcion == '1':
            menu_registrar()
        elif opcion == '2':
            menu_mostrar()
        elif opcion == '3':
            menu_actualizar()
        elif opcion == '4':
            menu_buscar()
        elif opcion == '5':
            menu_eliminar()
        elif opcion == '6':
            menu_reporte()
        elif opcion == '7':
            print("Saliendo del programa. ¡Hasta luego!")
            sys.exit()
        else:
            imprimir_error("Opción inválida. Intente nuevamente.")
            
if __name__ == "__main__":
    main()

    
