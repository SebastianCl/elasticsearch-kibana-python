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

# Documentos de ejemplo
libros = [
    {"id": 1, "titulo": "El mundo y sus demonios", "autor": "Carl Sagan"},
    {"id": 2, "titulo": "El hombre que calculaba", "autor": "Malba Tahan"},
    {"id": 3, "titulo": "El microscopio de Nicolas", "autor": "Alberto Pez"},
    {"id": 4, "titulo": "La fisica nuclear", "autor": "G.H. Guihernre"},
]

def indexar_libros():
    for libro in libros:
        es.index(index=index_name, id=libro["id"], document=libro)
    print("✅ Libros indexados correctamente")


def buscar_por_campo(campo, texto):
    print(f"\n🔍 Buscando libros por {campo}: '{texto}'")
    respuesta = es.search(
        index=index_name,
        query={"match": {campo: texto}}
    )

    mostrar_resultados(respuesta)


def buscar_por_titulo_y_autor(titulo, autor):
    print(f"\n🔍 Buscando libros por título: '{titulo}' y autor: '{autor}'")
    respuesta = es.search(
        index=index_name,
        query={
            "bool": {
                "must": [
                    {"match": {"titulo": titulo}},
                    {"match": {"autor": autor}},
                ]
            }
        }
    )

    mostrar_resultados(respuesta)


def mostrar_resultados(respuesta):
    hits = respuesta["hits"]["hits"]
    if not hits:
        print("❌ No se encontraron resultados.")
        return

    for hit in hits:
        fuente = hit["_source"]
        print(f"📘 {fuente['titulo']} — {fuente['autor']}")


# 🧭 Menú CLI
def menu():
    while True:
        print("\n📚 MENÚ DE BÚSQUEDA")
        print("1. Buscar por título")
        print("2. Buscar por autor")
        print("3. Buscar por título y autor")
        print("4. Indexar libros")
        print("0. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            texto = input("🔤 Ingrese título a buscar: ").strip()
            buscar_por_campo("titulo", texto)

        elif opcion == "2":
            texto = input("🧑‍💼 Ingrese autor a buscar: ").strip()
            buscar_por_campo("autor", texto)

        elif opcion == "3":
            titulo = input("🔤 Ingrese título: ").strip()
            autor = input("🧑‍💼 Ingrese autor: ").strip()
            buscar_por_titulo_y_autor(titulo, autor)

        elif opcion == "4":
            indexar_libros()

        elif opcion == "0":
            print("👋 Saliendo del programa.")
            break

        else:
            print("❌ Opción inválida. Intenta de nuevo.")


# ▶️ Iniciar menú
if __name__ == "__main__":
    menu()
