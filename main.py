from datetime import date, time
from fastapi import FastAPI, HTTPException
# FastAPI: para crear la aplicación.
# HTTPException: para devolver errores controlados (como 404), sin romper el programa.

from database import Base, motor, sessionLocal 
# Base (para crear las tablas), motor (la conexión), sessionLocal (la fábrica de sesiones).

from models import Producto, Venta
# Traemos las clases-tabla, para poder crear y consultar registros de cada una.
#---
from fastapi.responses import FileResponse
import pandas as pd
from borb.pdf import Document, Page, SingleColumnLayout, Paragraph, PDF, FixedColumnWidthTable as Table
#---
Base.metadata.create_all(motor)#crea las tablas de verdad
# Acá se crea DE VERDAD el archivo mi_bd.db (si no existía),
# con las tablas "productos" y "Ventas" adentro, según la forma definida en models.py.


app=FastAPI()##apilcacion instanciada
# Instancia la aplicación. De acá en adelante, cada endpoint se "cuelga" de este objeto.

#endpoints
@app.get("/productos")# el / define la direccion del endpoint
#el GET es solo consulta, no modifica nada
#dentro del parentesis va el valr/variable que vamos a usar
def listaProductos():
    db=sessionLocal()#abrimos el canal hacia la base de datos

    productos =db.query(Producto).all()#el querry nos dice que quiere consultar y dentro de()
    # va en que tabla hace la consulta
    #all nos dice que quiere traer todos los registros

    db.close()#cierra el canal porque ya conseguimos lo que queriamos
    return productos#nos devuelve la lista

@app.get("/productos/{id_producto}")#con el id lo que podemos hacer son consultas sobre 1 producto en especial
def productoParticular(id_producto: int):#le asignamos un nombre a la funcion
    #y le decimos que va a hacer su tarea en base a esa variable que tiene que ser ese tipo de dato
    db=sessionLocal()#abrimos el canal
    producto=db.query(Producto).filter(Producto.id_producto==id_producto).first()
    #filter es una condicion de filtrado. entre( ) va la condicion en cuestion
    #first() como ya lo dice la primera ves que se cumpla la condicion es la que va a mostrarse
    db.close()
    if producto==None:
        raise HTTPException(status_code=404,detail="producto no encontrado")
        #hacemos una exception para declarar el error y que no se rompa el programa

    return producto

@app.post("/productos",status_code=201)#post crea un nuevo producto/recurso
#status_code=201 es para cuando todo se ejecuto correctamente
#201:nuevo recurso creado
def crearProducto(nombre:str, precios:float):
    db=sessionLocal()#abrimos canal
    nuevo=Producto(nombreProducto=nombre,precio=precios)#creamos el recurso
    #primero va en nombre del atributo y despues el nombre de la variable
    db.add(nuevo)#agregar el recurso en cuestion
    db.commit()#confirmamos el guardado permanente
    db.refresh(nuevo)#vuelve a leer un objeto específico 
    #desde la base de datos, actualizando sus valores en memoria
    db.close()
    return nuevo

@app.put("/productos/{id_producto}",status_code=201)#put nos actualiza todos los valores de los atributos de una clase
def actualizarRecurso(id_producto:int, nombreProductos:str,precios:float):#el id es importante para saber que recurso vamos a actualizar
    db=sessionLocal()
    recursoActualizado=db.query(Producto).filter(Producto.id_producto==id_producto).first()
    #primero encontramos el producto
    if recursoActualizado ==None :
        db.close()
        raise HTTPException(status_code=404, detail="producto no encontrado")
        #en caso de no encontrar dicho producto cortamos
    recursoActualizado.nombreProducto=nombreProductos #pisammos los datos
    recursoActualizado.precio=precios #pisamos datos

    db.commit()#confirmamos los cambios
    db.refresh(recursoActualizado)#refrescamos para que se efectue el cambio
    db.close
    return recursoActualizado

@app.delete("/productos/{id_producto}",status_code=200)#borrar recursos
#200:OK
def borrarRecurso(id_p:int):
    db=sessionLocal()
    borrar=db.query(Producto).filter(Producto.id_producto==id_p).first()
    if borrar==None:
        db.close()
        raise HTTPException(status_code=404, detail="producto no encontrado")
    db.delete(borrar)
    db.commit()#confirmamos el cambio en los registros
    db.close()

# ==========================================
#                VENTAS
# ==========================================
@app.post("/ventas")
def nuevaVenta (f:date,h:time,id_fk:int, cantidads:int):
    db=sessionLocal()
    venta=db.query(Producto).filter(Producto.id_producto==id_fk).first()
    #dentro del query va producto porque el id que buscamos esta dentro de los registros de esa tabbla
    if venta==None:
        db.close()
        raise HTTPException(status_code=404, detail="producto no encontrado")

    precioT=venta.precio*cantidads
    nuevaV= Venta(fecha=f,hora=h,id_ProductoFK=id_fk,cantidad=cantidads,precioTotal=precioT)
    db.add(nuevaV)
    db.commit()
    db.refresh(nuevaV)#refrescamos ese nuevo recurso
    db.close()
    return nuevaV

@app.get("/ventas")
def listaVentas():#no especificamos que datos necesita ya que necesita todos
    db=sessionLocal()
    lista=db.query(Venta).all()
    db.close()
    return lista

@app.get("/ventas/{id_ventas}")
def venta(id_v:int):
    db=sessionLocal()
    recurso=db.query(Venta).filter(Venta.id_ventas==id_v).first()
    db.close()
    if recurso==None:
        raise HTTPException(status_code=404, detail="producto no encontrado")
    return recurso

@app.put("/ventas/{id_ventas}",status_code=201)
def actualizarVenta(id_V:int, id_ProFk:int,f:date,h:time,cantidads:int):
    db=sessionLocal()
    actualizarV=db.query(Venta).filter(Venta.id_ventas==id_V).first()
    if actualizarV==None:
        db.close()
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    actualizarP=db.query(Producto).filter(Producto.id_producto==id_ProFk).first()
    if actualizarP==None:
        db.close()
        raise HTTPException(status_code=404, detail="producto no encontrado")
    actualizarV.fecha=f
    actualizarV.hora=h
    actualizarV.id_ProductoFK=id_ProFk
    actualizarV.cantidad=cantidads
    actualizarV.precioTotal=actualizarV.cantidad*actualizarP.precio

    db.commit()
    db.refresh(actualizarV)
    db.close()
    return actualizarV

@app.delete("/ventas/{id_ventas}",status_code=200)
def borrarVenta(id_v:int):
    db=sessionLocal()
    borrar=db.query(Venta).filter(Venta.id_ventas==id_v).first()
    if borrar==None:
        db.close()
        raise HTTPException(status_code=404, detail="venta no encontrada")
    db.delete(borrar)
    db.commit()
    db.close()

@app.get("/reportes/ventas")
#genera un PDF con el listado de todas las ventas registradas
def reporteVentas():
    db=sessionLocal()
    ventas=db.query(Venta).all()#traemos todas las ventas de la base
    db.close()

    #armamos los datos en una tabla de pandas, mas facil de ordenar
    datos=[]
    for v in ventas:
        datos.append({
            "id":v.id_ventas,
            "fecha":str(v.fecha),
            "hora":str(v.hora),
            "producto_id":v.id_ProductoFK,
            "cantidad":v.cantidad,
            "total":v.precioTotal
        })
    df=pd.DataFrame(datos)

    #armamos el documento PDF con borb
    doc=Document()
    page=Page()
    doc.append_page(page)
    layout=SingleColumnLayout(page)
    layout.append_layout_element(Paragraph("Reporte de Ventas"))

    tabla=Table(number_of_rows=len(df)+1, number_of_columns=6)
    encabezados=["ID","Fecha","Hora","Producto","Cantidad","Total"]
    for e in encabezados:
        tabla.append_layout_element(Paragraph(e))
    for _, fila in df.iterrows():
        tabla.append_layout_element(Paragraph(str(fila["id"])))
        tabla.append_layout_element(Paragraph(fila["fecha"]))
        tabla.append_layout_element(Paragraph(fila["hora"]))
        tabla.append_layout_element(Paragraph(str(fila["producto_id"])))
        tabla.append_layout_element(Paragraph(str(fila["cantidad"])))
        tabla.append_layout_element(Paragraph(str(fila["total"])))
    layout.append_layout_element(tabla)

    PDF.write(what=doc, where_to="reporte_ventas.pdf")

    return FileResponse("reporte_ventas.pdf", media_type="application/pdf", filename="reporte_ventas.pdf")