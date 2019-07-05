#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, and_, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import RPi.GPIO as GPIO
import json
import requests
import time

# GPIO PROPIEDADES E INICIALIZACIÓN
#canle_GPIO desaparecerá, xa que cando aparezca o rego por zona, obteremos este valor mediante a táboa CONFIGURACION_POR_ZONA

# resto de configuracion de GPIO e inicializacion
GPIO.setmode(GPIO.BCM)


app = Flask(__name__)

# CONFIGURACION BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pi:XXXXXXX@localhost/rHorta'
db = SQLAlchemy(app)

# Creamos un obxecto para interactuar coa base de datos
def crear_session(config):
    engine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    session = Session()
    session._model_changes = {}
    return session

# Utilizaremos db_session para interactuar coa base de datos
db_session = crear_session(app.config)

# Obxecto Modelo da táboa propiedades
class Propiedad(db.Model):
	__tablename__ = 'propiedades'
	clave = db.Column(db.String(50), primary_key=True)
	valor = db.Column(db.String(255), unique=False, nullable=True)

	def __repr__(self):
		return '<propiedad %r:%r>' % self.clave
	def as_dict(self):
	       return {self.clave:self.valor}

# Obxecto Modelo da táboa eventos_rego
class EventosRego(db.Model):
    __tablename__ = 'eventos_rego'
    id = db.Column(db.Integer, primary_key=True)
    inicio = db.Column(db.Date, unique=False, nullable=True)
    fin = db.Column(db.Date, unique=False, nullable=True)
    zona = db.Column(db.String, unique=False, nullable=True)	

# Obxecto Modelo da táboa sensores_mi_flora
class SensorMiFlora(db.Model):
	__tablename__ = 'sensores_mi_flora'
	mac_addr = db.Column(db.String, primary_key=True)
	humidade =db.Column(db.Float, unique=False, nullable=True) 
	temperatura=db.Column(db.Float, unique=False, nullable=True) 
	nombre=db.Column(db.String, unique=False, nullable=True)
	nivel_ph=db.Column(db.Float, unique=False, nullable=True)
	luz_solar =db.Column(db.Float, unique=False, nullable=True)
	nivel_bateria =db.Column(db.Float, unique=False, nullable=True)  
	firmware =db.Column(db.String, unique=False, nullable=True)  
	ultima_medicion= db.Column(db.Date, unique=False, nullable=True)
	zona=db.Column(db.String, unique=False, nullable=True)

# Obxecto Modelo da táboa sensores_mi_flora
class SensorMiFloraHist(db.Model):
	__tablename__ = 'sensores_mi_flora_historico'
	mac_addr = db.Column(db.String, primary_key=True)
	humidade =db.Column(db.Float, unique=False, nullable=True) 
	temperatura=db.Column(db.Float, unique=False, nullable=True) 
	nombre=db.Column(db.String, unique=False, nullable=True)
	nivel_ph=db.Column(db.Float, unique=False, nullable=True)
	luz_solar =db.Column(db.Float, unique=False, nullable=True)
	nivel_bateria =db.Column(db.Float, unique=False, nullable=True)  
	firmware =db.Column(db.String, unique=False, nullable=True)  
	fecha= db.Column(db.Date, unique=False, nullable=True)
	zona=db.Column(db.String, unique=False, nullable=True)

class Zona(db.Model):
	__tablename__ = 'zona'
	id_zona =db.Column(db.String, primary_key=True)
	canal_gpio=db.Column(db.Integer, unique=False, nullable=True)
	tope_riegos=db.Column(db.Integer, unique=False, nullable=True)
	min_humidade=db.Column(db.Float, unique=False, nullable=True)
	max_humidade=db.Column(db.Float, unique=False, nullable=True)


# Realiza unha consulta a base de datos, na táboa propiedades, para obter o valor de id_evento
def id_evento():
	return db_session.query(Propiedad).filter(Propiedad.clave == 'id_evento').one().valor;

#Realiza a accion sobre o relé
def accion_rele(canle, sinal):
	GPIO.output(canle, sinal)

# Activa a bomba de auga, mandando un GPIO.HIGH ó relé
def activar_bomba_auga(canle_GPIO):
	GPIO.setup(canle_GPIO,GPIO.OUT)
	accion_rele(canle_GPIO, GPIO.HIGH)

# Activa a bomba de auga, mandando un GPIO.LOW ó relé
def desactivar_bomba_auga(canle_GPIO):
	GPIO.setup(canle_GPIO,GPIO.OUT)
	accion_rele(canle_GPIO, GPIO.LOW)
	
# devolve o estado do rego (ACTIVO ou INACTIVO)
def get_estado_rego():
	propiedad = db_session.query(Propiedad).filter(Propiedad.clave == 'estado_rego').one();
	return propiedad.valor

# devolve a canle que debemos utilizar para regar unha zona
def get_canal_zona(id_zona):
	return db_session.query(Zona).filter(Zona.id_zona == id_zona).one().canal_gpio;

# obtén o numero de regos nunha zona determinada
def num_regos_zona(id_zona):
	hoxe = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
	num_regos = db_session.query(EventosRego).filter(hoxe<=EventosRego.fin, EventosRego.zona == id_zona).count()
	return num_regos

# actualiza na taboa sensores_mi_flora os parametros medidos por os diferentes sensores mi_flora. 
# garda na taboa sensores_mi_flora_historico un novo rexistro cós parametros medidos por os diferentes sensores mi_flora. 
@app.route('/gardar_info_sensores', methods=['POST'])
def gardar_info_sensores():
	try:
		list_of_dicts = json.loads(request.json)
		for d in list_of_dicts:		
			fech = datetime.now()
			db_session.query(SensorMiFlora).filter(SensorMiFlora.mac_addr == d['MAC']).update({'ultima_medicion': datetime.now(),'humidade':d['HUMIDADE'],'temperatura':d['TEMPERATURA'], 'nivel_ph':d['PH'], 'firmware':d['FW'], 'luz_solar':d['LUZ'], 'nivel_bateria':d['BATERIA']})
			db_session.commit()
			historico = SensorMiFloraHist(mac_addr = d['MAC'],humidade =d['HUMIDADE'],temperatura=d['TEMPERATURA'],nombre=d['NOME'],nivel_ph=d['PH'],luz_solar =d['LUZ'],nivel_bateria =d['BATERIA'],firmware =d['FW'],fecha= fech)
			db_session.add(historico)
			db_session.commit()
		return jsonify({'result':'OK'}), 200
	except:
		return jsonify({'result':'KO'}), 403

@app.route("/obter_info_sensor/<mac>")
def obter_info_sensor(mac=None):
	sensor = db_session.query(SensorMiFlora).filter(SensorMiFlora.mac_addr == mac).one();
	d = {}
	d['MAC']=mac
	d['HUMIDADE']=sensor.humidade
	d['TEMPERATURA']=sensor.temperatura
	d['NOME']=sensor.nombre
	d['NIVEL_PH']=sensor.nivel_ph
	d['LUZ_SOLAR']=sensor.luz_solar
	d['ULTIMA_MEDICION']=sensor.ultima_medicion
	d['ZONA']=sensor.zona
	return jsonify(d)

@app.route("/regar", methods=['POST'])
def regar():
	lZonasRegadas = []
	list_of_dicts = json.loads(request.json)
	for tupla in list_of_dicts:
		for id_zona in tupla:
			zona = db_session.query(Zona).filter(Zona.id_zona == id_zona).one();
			l = tupla[id_zona]
			media = (sum(l) / float(len(l)))
			if media <= zona.min_humidade and num_regos_zona(id_zona) < zona.tope_riegos:
				activar(id_zona)
				time.sleep(7)
				desactivar(id_zona)
					
	
	return jsonify(lZonasRegadas)

#Devolve un JSON có nome e MAC dos diferentes sensores rexistrados en sensores_mi_flora
@app.route("/mac_sensores")
def get_mac_sensores():
	result = db_session.query(SensorMiFlora).all();
	json ={}
	for row in result:
		json[row.nombre] = row.mac_addr	
	return jsonify(json)


# Devolve o estado actual do rego (ACTIVO ou INACTIVO)
@app.route("/estado_rego")
def estado_rego():
	propiedad = db_session.query(Propiedad).filter(Propiedad.clave == 'estado_rego').one();
	return jsonify({propiedad.clave:propiedad.valor}), 200

# Activa o rego
# 1. Inicia un novo evento de rego, có id dispoñible en propiedades e a fecha de inicio actual (timestamp).
# 2. Cambia o estado_rego en propiedades a ACTIVO
# 3. Activa o relé que encenderá a bomba de auga.
@app.route("/activar/<id_zona>")
def activar(id_zona=None):
	json = jsonify({"error":"o rego xa está activado"})
	if get_estado_rego() == 'INACTIVO':
		evento = EventosRego(id=id_evento(), inicio=datetime.now(), fin=None, zona=id_zona)
		db_session.add(evento)
		db_session.commit()
		db_session.query(Propiedad).filter(Propiedad.clave == 'estado_rego').update({'valor': 'ACTIVO'})
		db_session.commit()
		activar_bomba_auga(get_canal_zona(id_zona))
		json = estado_rego()
		num_regos_zona(id_zona)
	return json

# Desactiva o rego
# 1. Modifica o evento de rego có id dispoñible en propiedades e a fecha de fin actual (timestamp).
# 2. Cambia o estado_rego en propiedades a INACTIVO
# 4. Incrementa o valor de id_evento, para que sexa utilizado no seguinte rego.
# 3. Desactiva o relé apagando a bomba de auga.
@app.route("/desactivar/<id_zona>")
def desactivar(id_zona=None):
	json = jsonify({"error": "o rego xa está desactivado"})
	if get_estado_rego() == 'ACTIVO':
		idEvento = int(id_evento())
		db_session.query(EventosRego).filter(EventosRego.id == str(idEvento)).update({'fin': datetime.now()})
		db_session.query(Propiedad).filter(Propiedad.clave == 'id_evento').update({'valor': str(idEvento+1)})
		db_session.query(Propiedad).filter(Propiedad.clave == 'estado_rego').update({'valor': 'INACTIVO'})
		db_session.commit()
		desactivar_bomba_auga(get_canal_zona(id_zona))
		json = estado_rego()
	return json
# Desactiva o rego
# 1. Desactiva o relé apagando a bomba de auga.
# 2. desactiva sin mirar estado
# 3. Cambia o estado_rego en propiedades a INACTIVO
# 4. Incrementa o valor de id_evento, para que sexa utilizado no seguinte rego.

@app.route("/forzar_desactivado")
def forzar_desactivado():
	desactivar_bomba_auga()
	idEvento = int(id_evento())
	db_session.query(Propiedad).filter(Propiedad.clave == 'id_evento').update({'valor': str(idEvento+1)})
	db_session.query(Propiedad).filter(Propiedad.clave == 'estado_rego').update({'valor': 'INACTIVO'})
	db_session.commit()	
	return estado_rego()

if __name__ == "__main__":
	app.run()
