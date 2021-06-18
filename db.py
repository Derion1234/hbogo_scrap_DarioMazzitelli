import mysql.connector
from config import *


#CONECT A BASE DE DATOS
fulltien_dario = mysql.connector.connect(
	host = db_connection_data['host'],
	user = db_connection_data['user'],
	password = db_connection_data['password'],
	database = db_connection_data['database']
	)
	
mycursor = fulltien_dario.cursor()



#FUNCION SQL INSERT
def insert_sql(movie):
	sql_insert = "INSERT INTO hboscrap (tittle, highlight, duration, description, subtitulos, idioma, image, logo, director, año, genero, escritor, agerating, cast) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	param = (movie["tittle"], movie["highlight"], movie["duration"], movie["description"],
	movie["subtitulos"], movie["idioma"], movie["image"], movie["logo"], movie["director"],
	movie["añoprod"], movie["genero"], movie["escritor"], movie["AgeRating"], movie["cast"])		
	mycursor.execute(sql_insert, param)
	try:
		fulltien_dario.commit()
		print(mycursor.rowcount, 'pelicula insertada.')
	except:
		print('no se inserto')
