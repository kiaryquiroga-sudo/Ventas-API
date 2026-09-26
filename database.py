from sqlalchemy import create_engine
# Trae la función que arma la conexión hacia la base de datos.

#preparar la configuración de la conexión — le dice "cuando alguien te use, 
# vas a hablar con SQLite, y el archivo se va a llamar mi_bd.db". 
# El archivo físico recién se crea después, con Base.metadata.create_all(motor).

from sqlalchemy.orm import declarative_base, sessionmaker 
# Trae declarative_base (para crear la plantilla de la que heredan las tablas)
# y sessionmaker (para preparar la fábrica de sesiones).es decir , es un canal de comunicacion

motor=create_engine("sqlite:///mi_bd.db")
#Define la conexión: usa SQLite, y guarda todo en el archivo "mi_bd.db".
# Todavía no crea el archivo, solo prepara el objeto de conexión.

sessionLocal=sessionmaker(bind=motor)
# Prepara la fábrica de sesiones, atada (bind=) a este motor específico.
# Cada vez que llamemos sessionLocal(), nos va a dar una sesión nueva conectada a "motor"

Base=declarative_base()
# Crea la plantilla vacía. Cualquier clase que herede de Base
