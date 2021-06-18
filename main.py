from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
import requests, json
import time
driver = webdriver.Chrome(executable_path="/home/dario/Desktop/chromedriver_linux64/chromedriver")
driver.get('https://hbogola.com/home')

time.sleep(5)

body = driver.find_element_by_css_selector('body')

# CLICK BOTON COOKIES
driver.find_element_by_id('onetrust-accept-btn-handler').click()

# Scroll hasta el final de la página, para evitar problemas por lazy load.
scrolls = 15
while True:
    scrolls -= 1
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)
    if scrolls < 0:
        break
    else:
        print(scrolls)

time.sleep(5)

#DECLARO ARRAY

urlarr = []

#Recorro todas las requests y extraigo las url

for request in driver.requests:
    if request.response:
        url = request.url
        #Divido la url en 2 solo si contiene el substr que tiene el json de las peliculas/series
        splitted = url.split("f5d80122-51d5-46c6-bcf0-ec3b73b2e45b?p=Home+", 1)
        #Si la url esta dividida en dos es porque es de una pelicula y se agrega la url a un array
        if len(splitted) == 2:
            urlarr.append(url)

#SE HACE UN REQUEST A LA URL Y SE PARSEA EL JSON CON LOS DATOS SOLICITADOS

def parse_content(req):
    response = requests.get(req)
    json_value = response.json()


    try:
        tittle = json_value['Name']
    except:
        tittle = "null"
    try:
        highlight = json_value['HighlightInfo']
    except:
        highlight = "null"
    try:
        duration = json_value['DurationText']
    except:
        duration = "null"
    try:
        description = json_value['Abstract']
    except:
        description = "null"


    subtitulos = []
    global subtitulos_str
    for sub in json_value['Subtitles']:
        try:
            subtitulos.append(sub['Name'])
            subtitulos_str = ",".join(subtitulos)
        except:
            subtitulos = "null"


    idioma = []
    global idioma_str
    for subo in json_value['AudioTracks']:
        try:
            idioma.append(subo['Name'])
            idioma_str = ",".join(idioma)
        except:
            idioma = "null"


    try:
        image = json_value['BackgroundUrl']
    except:
        image = "null"
    try:
        logo = json_value['LocalizedSingleColorLogoUrl']
    except:
        logo = "null"
    try:
        director = json_value['Director']
    except:
        director = "null"
    try:
        año = json_value['ProductionYear']
    except:
        año = "null"
    try:
        genero = json_value['Genre']
    except:
        genero = "null"
    try:
        escritor = json_value['Writer']
    except:
        escritor = "null"
    try:
        agerating = json_value['AgeRating']
    except:
        agerating = "null"
    try:
        cast = json_value['Cast']
    except:
        cast = "null"

    #DEVUELVE TODOS LOS DATOS OBTENIDOS DE LA PELICULA/SERIE EN UN DICCIONARIO
    return {"tittle" : tittle, "highlight" : highlight, "duration" : duration,
    "description" : description, "subtitulos" : subtitulos_str, "idioma" : idioma_str,
    "image" : image, "logo" : logo, "director" : director,
    "añoprod" : año, "genero" : genero, "escritor" : escritor,
    "AgeRating" : agerating, "cast" : cast}



import db

for content in urlarr:
    movie = parse_content(content)
        db.insert_sql(movie)