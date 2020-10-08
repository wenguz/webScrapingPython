##buscar y descargar noticias de internet con python
##pip3 install feedparser
##pip3 install newspaper3k: https://newspaper.readthedocs.io/en/latest/
##https://newspaper.readthedocs.io/en/latest/
##ejemplo utilizado:https://towardsdatascience.com/the-easy-way-to-web-scrape-articles-online-d28947fc5979
import json
import feedparser as fp
import newspaper
from newspaper import Article
import pandas as pd

##limite de descargas
limite = 4
datos = pd.DataFrame()

# Llamar al archivo JSON
with open('paginas.json') as archivos_datos:
    paginas = json.load(archivos_datos)

# Iterar por cada pagina de noticias

contador = 1

for pagina, valor in paginas.items():
    #verificar si hay un enlace rss para dar prioridad
    if 'rss' in valor:
        v = fp.parse(valor['rss'])
        print("Descargando articulos de: ", pagina) # Se crea un diccionario con la palabra reservada newspaper jalando los datos de nuestro json
        ##diccionario para elelmentos de articulo
        newsPaper = {
            "pagina": pagina,
            "link": valor['link'],
            "articulos": [] # Se crea un elemento en blanco, donde se guardaran las noticias
        }
        for entrada in v.entries:

            if contador > limite:
                break
            article = pd.DataFrame()
            article['link'] = entrada.link
            try:
                contenido = Article(entrada.link)
                contenido.download()
                contenido.parse()
            except Exception as e:
                # Para evitar errores en caso de problemas de conexion
                # En caso de error el programa seguira el ciclo e imprimira continuar
                print(e)
                print("continuando...")
                continue
            article = pd.DataFrame(columns=['Titulo','Autor','Texto','Resumen','fecha_publicacion','URL'])
            article['Titulo'] = contenido.title
            article['Autor'] = contenido.authors
            article['Texto']=contenido.text
            article['Resumen']=contenido.summary
            article['fecha_publicacion']=contenido.publish_date
            article['URL'] = contenido.source_url

            newsPaper['articulos'].append(article)
            print(contador, "Articulo descargado de", pagina, ", url: ", entrada.link)
            contador = contador + 1

    else:
        # El Else es para las paginas que no cuentan con un rss
        # Se usa la libreria de newspaper para extraer articulos

        print("Descargando articulos de: :  ", pagina)
        hoja = newspaper.build(valor['link'], memoize_articles=False)
        newsPaper = []
        contador = 0
        for contenido in hoja.articles:
            print("descargando")

            contenido.download()
            print("descargando")
            contenido.parse()
            if contador > limite:
                break
            print("armando article")
            article = pd.DataFrame(columns=['Titulo','Autor','Texto','Resumen','fecha_publicacion','URL'])
            article['Titulo'] = contenido.title
            article['Autor'] = contenido.authors
            article['Texto']=contenido.text
            article['Resumen']=contenido.summary
            article['fecha_publicacion']=contenido.publish_date
            article['URL'] = contenido.source_url
                
            newsPaper.append(article)
            print(contador, "Articulo descargado de", pagina, " url: ", contenido.url)
            contador = contador + 1
    datos = datos.append(newsPaper,ignore_index = True)


# Por ultimo todo se guarda en un archivo json
try:
  datos.to_excel('datos_noticias.xlsx')
  print("guarda")
except Exception as e: print(e)