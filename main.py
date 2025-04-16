from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

es = Elasticsearch("http://localhost:9200")
index_name = "libros"

# Verificar conexión
try:
    info = es.info()
    print("✅ Conectado a Elasticsearch:", info["version"]["number"])
except Exception as e:
    print("❌ Error al conectar:", e)
    exit(1)

# Crear índice si no existe
try:
    es.indices.get(index=index_name)
    print("📂 Índice 'libros' ya existe")
except NotFoundError:
    print("📁 Índice 'libros' no existe, creando...")
    es.indices.create(index=index_name)

# Indexar documentos
libros = [
    {"id": 1, "titulo": "El mundo y sus demonios", "autor": "Carl Sagan"},
    {"id": 2, "titulo": "El hombre que calculaba", "autor": "Malba Tahan"},
    {"id": 3, "titulo": "El microscopio de Nicolas", "autor": "Alberto Pez"}
]

for libro in libros:
    es.index(index=index_name, id=libro["id"], document=libro)

print("✅ Libros indexados correctamente")
