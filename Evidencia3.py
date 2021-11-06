from collections import namedtuple
from typing import List

ciclo = True
datos_productos = {}
Venta = namedtuple("Venta", ("descripcion","cantidad","precio","fecha_de_venta"))
monto_total = 0
n = 0
import datetime
datos_venta = {}
import csv
import os
import sys 
import sqlite3
from sqlite3 import Error


while ciclo:
    print("\n---REGISTRAR UNA VENTA---")
    print("1.Registrar")
    print("2.Consulta de datos")
    print("3.Reporte de ventas")
    print("4.Conexion y tabla en Sqlite")
    print("5..Salir")
    print("-"*30)
    op_menu = int(input())

    if op_menu == 1:
        carrito = []
        ciclo2 = True
        folio = int(input("Numero de folio: "))
        fecha_de_venta = input("Fecha de venta: ")
        while ciclo2:
            print("\n***Registrar***")
            descripcion = input("Descripcion del articulo: ")
            cantidad = int(input("Cantidad de piezas vendidas: "))
            precio = int(input("Precio de ventas: "))
            venta_registrada = Venta(descripcion,cantidad,precio,fecha_de_venta)
            carrito.append(venta_registrada)
            op_agregar = input("¿Otro mas? S/N: ").upper()
            if op_agregar == "N":
                ciclo2 = False
        else:
            monto = (cantidad * precio)
            monto_total = monto_total + monto
            iva = (monto_total * 0.16)
            monto_iva = monto_total + iva
            print(f"El monto total a pagar por parte del cliente es: {monto_iva}")
            print(f"El IVA aplicable a la venta es: {iva}")
            datos_venta[folio] = [carrito,iva,monto_iva,fecha_de_venta]

    elif op_menu == 2:
        consulta = int(input("Ingrese el folio: ")
        )
        if consulta in datos_venta.keys():
            print(f"El folio es: {consulta} ")
            print(f"Su fecha de venta es: {datos_venta[consulta][3]} ")
            print("-" * 50)
            for consulta_venta in datos_venta[consulta][0]:
                print(f"El producto cuenta con una cantidad de: {consulta_venta.cantidad} ")
                print(f"La descripcion del producto es: {consulta_venta.descripcion} ")
                print(f"El precio unitario del producto es: {consulta_venta.precio} ")
                print("-" * 50)
            
            print(f"Monto total del  producto es: {datos_venta[consulta][2]} ")
            print(f"IVA del  producto es: {datos_venta[consulta][1]} ")
            
        else:
            print("No esta registrada")

    elif op_menu == 3:
        List = [descripcion , iva , monto_iva,  fecha_de_venta]
        print (str(List[0]) + "\t" + str(List[1]) + "\t" + str(List[2]))
        with open('Registro.csv', 'w', newline='') as VentadeLlantas:
            Registro = csv.writer(VentadeLlantas)
            Registro.writerow(("descripcion" , "iva" , "monto_iva"))
            Registro.writerows([(descripcion, iva , monto_iva) for fecha in datos_venta.items()])
            print(f"---Grabado exitoso en-----> {os.getcwd()}")

    elif op_menu == 4:
        try:
            with sqlite3.connect("RegistrosSQLite.db") as conn: #Establecer conexion
                mi_cursor = conn.cursor() 
                mi_cursor.execute("CREATE TABLE IF NOT EXISTS RegistrosSQLite (DESCRIPCION TEXT NOT NULL, TOTAL REAL NOT NULL, TOTAL_IVA REAL NOT NULL)")
                mi_cursor.execute(f"INSERT INTO RegistrosSQLite VALUES(?,?,?)",(descripcion,iva, monto_iva))
                print("Creada exitosamente")
        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()

    elif op_menu == 5:
        ciclo = False