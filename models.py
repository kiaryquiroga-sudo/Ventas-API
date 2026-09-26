from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey
# Trae Column (para definir columnas) y los tipos de dato que vamos a usar.

from database import Base
# Trae la plantilla Base que ya armamos en database.py,
# para que Producto y Venta puedan heredar de ella.

class Producto(Base):
    __tablename__="productos"
    id_producto= Column(Integer,primary_key=True,autoincrement=True,nullable=False )
    nombreProducto= Column(String,nullable=False)
    precio=Column (Float, nullable=False)

class Venta(Base):
    __tablename__="Ventas"
    id_ventas=Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    fecha=Column(Date,nullable=False)
    hora=Column(Time,nullable=False)
    id_ProductoFK=Column(Integer,ForeignKey("productos.id_producto"),nullable=False)
    #es productos y no Producto. porque es el nombre real que le  asignamos dentro de la BD
    cantidad=Column(Integer,nullable=False)
    precioTotal=Column(Float,nullable=False)
