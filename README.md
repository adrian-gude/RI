# RI
Repositorio para la práctica de RI de la asignatura RIWS. (Q1 MUEI año 23-24).

    Lista de comandos:
    - Para extraer los datos usando el scrapy configurado:
        - Acceder a la carpeta "crawler"
        - Ejecutar el siguiente comando:
            scrapy crawl hotels -O hotels.json
        NOTA: si deseas obtener información más detallada durante la ejecución de errores es necesario poner la variable "MOSTRAR_WARNINGS" del archivo     "hotels_spyder.py" a TRUE.
        - La salida se habrá guardado en un archivo con nombre "hotels.json"

    - Para construír un archivo válido para incluír en el índice:
        - Abrir el archivo hotels.json y eliminar la primera y última línea, que son "[" y "]"
        - Eliminar las comas que hay al final de cada línea y que están separando cada hotel
        - Añadir "{create: {}}" una vez por cada hotel
        - Añadir/comprobar que haya una línea en blanco al final del archivo

        Así, al final pasamos de algo como esto:
            [
            {"comunidad": "Pais Vasco", "nombre": "nombre1", "precio": "84", "localizacion": "Calle X", "n_opiniones": "109", "puntuacion": "4.5", "categoria": "2", "idiomas": ["Español", "Inglés"], "servicios": ["Habitaciones de no fumadores"], "url":"ejemplo1", "imageUrl": "urlImagen2"},
            {"comunidad": "Pais Vasco", "nombre": "nombre2, "precio": "84", "localizacion": "Calle Y", "n_opiniones": "109", "puntuacion": "4.5", "categoria": "2", "idiomas": ["Español", "Inglés"], "servicios": ["Hotel de no fumadores"], "url":"ejemplo2", "imageUrl": "urlImagen2"}
            ]

        A algo como esto:
            {"create": {}}
            {"comunidad": "Pais Vasco", "nombre": "nombre1", "precio": "84", "localizacion": "Calle X", "n_opiniones": "109", "puntuacion": "4.5", "categoria": "2", "idiomas": ["Español", "Inglés"], "servicios": ["Habitaciones de no fumadores"], "url":"ejemplo1", "imageUrl": "urlImagen2"}
            {create: {}}
            {"comunidad": "Pais Vasco", "nombre": "nombre2, "precio": "84", "localizacion": "Calle Y", "n_opiniones": "109", "puntuacion": "4.5", "categoria": "2", "idiomas": ["Español", "Inglés"], "servicios": ["Hotel de no fumadores"], "url":"ejemplo2", "imageUrl": "urlImagen2"}

    - Para crear el índice:
        NOTA: es necesario tener elasticsearch ejecutandose.
        (Se adjunta un archivo para importar a Postman todas las operaciones necesarias en la carpeta DATA)
        - Creación (Create Hotels): PUT a la dirección http://localhost:9200/hotels
        - Configuración (Map columns - NGram): PUT a la dirección http://localhost:9200/hotels/_mapping
        - Inserción de datos (Bulk Add Hotels):
            - PUT a la dirección http://localhost:9200/hotels/_bulk

    - Para lanzar la aplicación:
        NOTA: es necesario tener elasticsearch ejecutandose.
        - Se accede a la carpeta "BuscaTuHotel" del repositorio
        - Se abre un terminal en esta carpeta y se ejecutan los siguientes comandos:
            - npm install
            - npm start
            NOTA: "npm install" solo será necesario la primera vez
        - Para visualizar la aplicación solo habrá que esperar a que se habrá una pestaña automaticamente, o por defecto acceder con un navegador web a "http://localhost:3000/"
        - Si se experimentan problemas de seguridad, será necesario añadir las siguientes lineas al archivo elasticsearch.yml, (se adjunta el archivo elasticsearch.yml en la carpeta DATA):
            -http.cors.enabled: true
            -http.cors.allow-origin: "*"
            -http.cors.allow-headers: "*"
            -http.cors.allow-credentials: true
            -# Enable security features
            -xpack.security.enabled: false

