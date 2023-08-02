from flask import Flask, jsonify, request
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
import os

app = Flask(__name__)

url_path = Path('.') / '.env'
load_dotenv(dotenv_path=url_path)
class Settings:
    SERVER_HOST = os.environ.get('SERVER_HOST')

settings = Settings()

db_config = {
    'host': settings.SERVER_HOST,
    'user': 'root',
    'password': '2024octubre',
    'database': 'chat'
}

def test_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        conn.close()
        return True
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return False

@app.route('/test-db-connection')
def test_connection_endpoint():
    if test_db_connection():
        return jsonify({"message": "La conexión a la base de datos es exitosa.", "path":settings.SERVER_HOST})
    else:
        return jsonify({"message": "Error en la conexión a la base de datos.", "path":settings.SERVER_HOST})

@app.route('/')
def hello_world():
    return '¡Hola, mundo! Este es mi primer endpoint en Flask 2023.'

#CUANDO RECIBAMOS LAS PETICIONES EN ESTA RUTA
@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    #SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        #SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.args.get('hub.verify_token') == "HolaNovato":
            #ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return request.args.get('hub.challenge')
        else:
            #SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
          return "Error de autentificacion."
    #RECIBIMOS TODOS LOS DATOS ENVIADO VIA JSON
    data=request.get_json()
    #EXTRAEMOS EL NUMERO DE TELEFONO Y EL MANSAJE
    telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    #EXTRAEMOS EL TELEFONO DEL CLIENTE
    mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    #EXTRAEMOS EL ID DE WHATSAPP DEL ARRAY
    idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    #EXTRAEMOS EL TIEMPO DE WHATSAPP DEL ARRAY
    timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
    #ESCRIBIMOS EL NUMERO DE TELEFONO Y EL MENSAJE EN EL ARCHIVO TEXTO
    #SI HAY UN MENSAJE
    if mensaje is not None:
      from rivescript import RiveScript
      bot = RiveScript()
      bot.load_file('restaurante.rive')
      bot.sort_replies()

      #Obtener respuesta
      respuesta = bot.reply('localuser', mensaje) # parte importante para 
      respuesta=respuesta.replace("\\n", "\\\n")
      respuesta=respuesta.replace("\\", "")
      
    #CONECTAMOS A LA BASE DE DATOS
      import mysql.connector
      mydb = mysql.connector.connect(
          host = settings.SERVER_HOST,
          user = "root",
          password = "2024octubre",
          database='chat'
      )
      mycursor = mydb.cursor()
      query="SELECT count(id) AS cantidad FROM registro WHERE id_wa='" + idWA + "';"
      mycursor.execute("SELECT count(id) AS cantidad FROM registro WHERE id_wa='" + idWA + "';")

      cantidad, = mycursor.fetchone()
      cantidad=str(cantidad)
      cantidad=int(cantidad)
      if cantidad==0 :
        sql = ("INSERT INTO registro"+ 
        "(mensaje_recibido,mensaje_enviado,id_wa      ,timestamp_wa   ,telefono_wa) VALUES "+
        "('"+mensaje+"'   ,'"+respuesta+"','"+idWA+"' ,'"+timestamp+"','"+telefonoCliente+"');")
        mycursor.execute(sql)
        mydb.commit()
        enviar(telefonoCliente, respuesta)

def enviar(telefonoRecibe,respuesta):
  from heyoo import WhatsApp
  #TOKEN DE ACCESO DE FACEBOOK
  token='EAAO2qVs7HpwBO0s8PcVRrwlLUKPO1Ti6lfT9bbcAtCeYo1d5qx0NymqNNKvZCcqyhpIJL1GGggZA4AJix5XbLV8vfoTFPlUMXjteh96q95GMvcECQTJW6oi9NqsXzEzUUVj1Bz9pyagVJ9hloZBXrbOlUDpsAcuZBcGV49RghhGlfswrPxYGMpnEZCmaqGGDhUFlTMgCWyDSWwlFfdiATlG4c4asZD'
  #IDENTIFICADOR DE NÚMERO DE TELÉFONO
  idNumeroTeléfono='113200398528965'
  #INICIALIZAMOS ENVIO DE MENSAJES
  mensajeWa=WhatsApp(token,idNumeroTeléfono)
  telefonoRecibe=telefonoRecibe.replace("521","52")
  #ENVIAMOS UN MENSAJE DE TEXTO
  mensajeWa.send_message(respuesta,telefonoRecibe)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=93)
