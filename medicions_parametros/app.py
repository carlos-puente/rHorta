#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend
from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY

# api-endpoint 
URL = "http://localhost:5000/mac_sensores"

procesado = 0  

# sending get request and saving the response as response object 
r = requests.get(url = URL, params = None) 
  
# extracting data in json format 
data = r.json() 
lInfoSensor = []
for nome in data:
	mac_addr = data[nome]
	procesado = 0
	while procesado == 0:
		try:
			poller = MiFloraPoller(mac_addr, BluepyBackend)
			print("\nObtendo datos de "+nome+" ("+mac_addr+")")
			d={}
			d['MAC'] = mac_addr
			d['FW'] = poller.firmware_version()
			d['NOME'] = poller.name()
			d['TEMPERATURA'] = poller.parameter_value(MI_TEMPERATURE)
			d['HUMIDADE'] = poller.parameter_value(MI_MOISTURE)
			d['LUZ'] = poller.parameter_value(MI_LIGHT)
			d['PH'] = poller.parameter_value(MI_CONDUCTIVITY)
			d['BATERIA'] = poller.parameter_value(MI_BATTERY)
			procesado = 1
			lInfoSensor.append(d)			
		except:
			procesado = 0

res = requests.post('http://localhost:5000/gardar_info_sensores', json=json.dumps(lInfoSensor))

