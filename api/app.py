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

# GPIO PROPIEDADES E INICIALIZACIÓN
canle_GPIO = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(canle_GPIO,GPIO.OUT)

app = Flask(__name__)

# CONFIGURACION BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pi:XXXXXX@localhost/rHorta'
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


# Realiza unha consulta a base de datos, na táboa propiedades, para obter o valor de id_evento
def id_evento():
	return db_session.query(Propiedad).filter(Propiedad.clave == 'id_evento').one().valor;

#Realiza a accion sobre o relé
def accion_rele(canle, sinal):
	GPIO.output(canle, sinal)

# Activa a bomba de auga, mandando un GPIO.HIGH ó relé
def activar_bomba_auga():
	accion_rele(canle_GPIO, GPIO.HIGH)

# Activa a bomba de auga, mandando un GPIO.LOW ó relé
def desactivar_bomba_auga():
	accion_rele(canle_GPIO, GPIO.LOW)

def get_estado_rego():
	propiedad = db_session.query(Propiedad).filter(Propiedad.clave == 'estado_rego').one();
	return propiedad.valor


@app.route('/gardar_info_sensores', methods=['POST'])
def gardar_info_sensores():
	try:
		list_of_dicts = json.loads(request.json)
		for d in list_of_dicts:		
			db_session.query(SensorMiFlora).filter(SensorMiFlora.mac_addr == d['MAC']).update({'ultima_medicion': datetime.now(),'humidade':d['HUMIDADE'],'temperatura':d['TEMPERATURA'], 'nivel_ph':d['PH'], 'firmware':d['FW'], 'luz_solar':d['LUZ'], 'nivel_bateria':d['BATERIA']})
			db_session.commit()
		return jsonify({'result':'OK'}), 200
	except:
		return jsonify({'result':'KO'}), 403


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
@app.route("/activar")
def activar():
	json = jsonify({"error":"o rego xa está activado"})
	if get_estado_rego() == 'INACTIVO':
		evento = EventosRego(id=id_evento(), inicio=datetime.now(), fin=None, zona=None)
		db_session.add(evento)
		db_session.commit()
		db_session.query(Propiedad).filter(Propiedad.clave == 'estado_rego').update({'valor': 'ACTIVO'})
		db_session.commit()
		activar_bomba_auga()
		json = estado_rego()
	return json

# Desactiva o rego
# 1. Modifica o evento de rego có id dispoñible en propiedades e a fecha de fin actual (timestamp).
# 2. Cambia o estado_rego en propiedades a INACTIVO
# 4. Incrementa o valor de id_evento, para que sexa utilizado no seguinte rego.
# 3. Desactiva o relé apagando a bomba de auga.
@app.route("/desactivar")
def desactivar():
	json = jsonify({"error": "o rego xa está desactivado"})
	if get_estado_rego() == 'ACTIVO':
		idEvento = int(id_evento())
		db_session.query(EventosRego).filter(EventosRego.id == str(idEvento)).update({'fin': datetime.now()})
		db_session.query(Propiedad).filter(Propiedad.clave == 'id_evento').update({'valor': str(idEvento+1)})
		db_session.query(Propiedad).filter(Propiedad.clave == 'estado_rego').update({'valor': 'INACTIVO'})
		db_session.commit()
		desactivar_bomba_auga()
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
