#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend
from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY

# HOW - TO: Incluiremos no CRON (crontab -e) a seguinte liña para que a medición sexa executada cada hora.

# Mediante chamadas a API, obterá as MAC de cada sensor, para poder utilizar as ferramentas da libraría miflora.
# Obtendo, mediante BLE (utilizando BluepyBackend) os datos, comúnicase coa API para actualizar na base de datos.

# api-endpoint 
URL = "http://localhost:5000"
METODO_MAC_SENSORES = "/mac_sensores"
METODO_GARDAR_INFO = "/gardar_info_sensores"
MAX_PETICIONS = 20
# obtemos os datos de cada sensor mi_flora {nome:MAC} da API
r = requests.get(url = URL+METODO_MAC_SENSORES, params = None) 
 
# Obtemos os datos en formato JSON
datos = r.json() 
# creamos unha lista baleira, onde iremos gardando cada conxunto de medicións correspondente a cada sensor mi_flora.
lInfoSensor = []

# engadiremos aquí os sensores mi flora que non puideron ser analizados, tras MAX_PETICIONS
lSensoresNonAnalizados = []
#Recorremos cada tupla
for nome in datos:
	mac_addr = datos[nome]
	num_peticions = 0
	while num_peticions<=MAX_PETICIONS:
		# executaremos este bucle mentres non fagamos unha medición correcta
		try:
			num_peticions++
			# obtemos as medicións do sensor mi flora
			poller = MiFloraPoller(mac_addr, BluepyBackend)
			print("\nObtendo datos de "+nome+" ("+mac_addr+")")
			d={}
			# engadimos ao diccionario o par {'MAC':mac_addr}
			d['MAC'] = mac_addr
			# engadimos ao diccionario o par {'FW':version_firmware} 
			d['FW'] = poller.firmware_version()
			# engadimos ao diccionario o par {'NOME':nome}
			d['NOME'] = poller.name()
			# engadimos ao diccionario o par {'TEMPERATURA':temperatura}
			d['TEMPERATURA'] = poller.parameter_value(MI_TEMPERATURE)
			# engadimos ao diccionario o par {'HUMIDADE':humidade}
			d['HUMIDADE'] = poller.parameter_value(MI_MOISTURE)
			# engadimos ao diccionario o par {'LUZ':luz}
			d['LUZ'] = poller.parameter_value(MI_LIGHT)
			# engadimos ao diccionario o par {'PH':pH}
			d['PH'] = poller.parameter_value(MI_CONDUCTIVITY)
			# engadimos ao diccionario o par {'BATERIA':bateria}
			d['BATERIA'] = poller.parameter_value(MI_BATTERY)
			# Cando recuperamos todo, mostramos a información e engadimos á lista
			print("Info obtida tras "+num_peticions+" peticions: "+str(d))
			lInfoSensor.append(d)
			# Como o proceso foi OK, rompemos o bucle, e así analizar os outros sensores mi_flora
			break
		except:
			print("Error obtendo datos (peticion "+str(num_peticions)+"), intentamos de novo")
			if num_peticions == MAX_PETICIONS:				
				lSensoresNonAnalizados.append(mac_addr)
				
# enviamos a API un json con cada unha das medicións
if len(lInfoSensor)>0:
	res = requests.post(url = URL+METODO_GARDAR_INFO, json=json.dumps(lInfoSensor))
	if len(lSensoresNonAnalizados) > 0:
		printf("Non foi posible obter os parámetros de: "+str(lSensoresNonAnalizados))
		#TO-DO: sistema para ter en conta os sensores non analizados.
else:
	print("ERRO: non foi posible obter datos para ningun sensor")
