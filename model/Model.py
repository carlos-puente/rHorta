
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, and_, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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
