import json
import requests
URL = "http://localhost:5000"
METODO_MAC_SENSORES = "/mac_sensores"
METODO_OBTER_INFO = "/obter_info_sensor/"
METODO_REGO = "/regar"


class DatosSensor():
	def __init__(self, mac_addr=None, humidade=None, temperatura=None,nombre=None, nivel_ph=None, luz_solar=None, ultima_medicion=None, zona=None):
		self.mac_addr=mac_addr
		self.humidade = humidade
		self.temperatura=temperatura
		self.nombre=nombre
		self.nivel_ph=nivel_ph
		self.luz_solar=luz_solar
		self.ultima_medicion=ultima_medicion
		self.zona=zona

r = requests.get(url = URL+METODO_MAC_SENSORES, params = None) 
 
# Obtemos os datos en formato JSON
datos = r.json()
lInfoZonas = []
lMediaLuz = []
for nome in datos:
	mac_addr = datos[nome]
	info = requests.get(url = URL+METODO_OBTER_INFO+mac_addr, params = None)
	s1 = json.dumps(info.json())
	d = json.loads(s1)
	datosSensor = DatosSensor(d['MAC'],d['HUMIDADE'],d['TEMPERATURA'],d['NOME'],d['NIVEL_PH'],d['LUZ_SOLAR'],d['ULTIMA_MEDICION'],d['ZONA'])
	lMediaLuz.append(datosSensor.luz_solar)		
	tupla = {}
	if len(lInfoZonas) == 0:
		tupla[datosSensor.zona] = [datosSensor.humidade]
		lInfoZonas.append(tupla)
	else:
		enc = 0
		for info in lInfoZonas:
			if datosSensor.zona in info:
				enc = 1
				info[datosSensor.zona].append(datosSensor.humidade)
				break
				
		if enc == 0:
			tupla[datosSensor.zona] = [datosSensor.humidade]
			lInfoZonas.append(tupla)
media = (sum(l) / float(len(l)))
if media >= 150:
	res = requests.post(url = URL+METODO_REGO, json=json.dumps(lInfoZonas))
