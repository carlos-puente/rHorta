# rHorta

rHorta é un proxecto de ocio e aprendizaxe, ideado có obxectivo de deseñar unha horta domótica e sustentable partindo dun nivel nulo de electrónica, utilizando Raspberry Pi e sensores de baixo coste. En canto a nocións informáticas, partiremos dun nivel alto de programación, aínda que sen experiencia en desenvolvemento para placas e sensores.

# Guía de instalación da API
Ollo, esto está en construcción.

## Instalando python3

A libraría que utilizaremos para comunicarnos cós sensores MiFlora, precisa python3, así que debemos asegurarnos que o noso sistema o teña correctamente instalado. Para iso executamos os seguintes comandos:

```
$ sudo apt-get install python3-dev libffi-dev libssl-dev -y
$ wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz
$ tar xJf Python-3.6.3.tar.xz
$ cd Python-3.6.3
$ ./configure
$ make
$ sudo make install
$ sudo pip3 install --upgrade pip
$ sudo apt install git python3 python3-pip bluetooth bluez python-dev python-rpi.gpio picap
$ picap-setup
```

Despois de executar os comandos anteriores, cós sensores MiFlora encendidos, recomendo facer un:

```
$ sudo hcitool lescan
```

E así comprobar que estanse a listar correctamente.

## Instalando postgreSQL

Os datos que obteñamos, así como eventos de rego e demáis, estarán gardados nunha base de datos, escollendo PostgreSQL como xestor. A instalación é moi sinxela.

```
$ sudo apt install postgresql libpq-dev postgresql-client pgadmin3 postgresql-client-common -y
$ sudo su postgres
$ createuser pi -P --interactive
```

Ao executar "createuser pi -P --interactive" o sistema irá pedíndonos o contrasinal para o usuario pi, así como se queremos que sexa administrador (algo que sí queremos).

## Instalando os aplicativos de rHorta

### Descargando o proxecto

```
$ cd ~
$ git clone https://github.com/carlos-puente/rHorta.git
```

Despois de executar estes dous comandos, o noso sistema estará en ~/rHorta.

### Posta en marcha da base de datos

Debemos crear unha base de datos seguindo o seguinte diagrama:

![Alt text](http://carlosjai.me/wp-content/uploads/2019/07/db.png)


* **zona**: información sobre a zona de rego. Está pensada para que poida haber varias zonas con rego individualizado, xa sexan zonas diferentes na horta, ou por exemplo, duas macetas con necesidades diferentes.
* **sensores_mi_flora**: información da última medición dos parámetros dun sensor determinado.
* **sensores_mi_flora_historico**: histórico de todas as medicións de tódolos sensores do sistema.
* **propiedades**: sistema clave valor para almacenar propiedades.
* **eventos_rego**: auditoría dos regos por zona.

Podemos importala mediante o script dispoñible en resources/schema.sql. Utilizando, por exemplo, o pgAdmin3 (Programacion > pgAdmin), instalado no paso anterior para tal efecto.

### Instalación dos requerimentos para os aplicativos.

Debemos instalar unha serie de paquetes vía pip3, para que o noso aplicativo funcione correctamente.

```
$ sudo pip3 install psycopg2
$ sudo pip3 install btlewrap
$ sudo pip3 install miflora
$ sudo pip3 install bluepy
$ sudo pip3 install pexpect
$ sudo pip3 install requests
$ sudo pip3 install flask
$ sudo pip3 install flask_sqlalchemy
$ sudo pip3 install RPi.GPIO
```

### Automatizando a execución

Despois do paso anterior, o sistema estaría instalado, e poderíamos lanzar cada un dos aplicativos (aloxados en ~/rHorta/api, ~/rHorta/sistema_rego e ~/rHorta/medicions_parametros). Pero é preferible automatizalo no cron.

```
$ sudo crontab -e
```

Onde engadiremos:

```
@reboot sh /home/pi/rHorta/api/launcher.sh >/home/pi/rHorta/logs/cronlog 2>&1
@hourly sh /home/pi/rHorta/medicions_parametros/launcher.sh >/home/pi/rHorta/logs/cronlog 2>&1
0 0,6,8,10,12,16,18,20 * * * /home/pi/rHorta/sistema_rego/launcher.sh >/home/pi/rHorta/logs/cronlog 2>&1
```
Ollo, utilizamos /home/pi/ como path onde estará rHorta.

* A API onde teremos os microservizos, executarase ao inicio, mediante: @reboot sh /home/pi/rHorta/api/launcher.sh
* Realizaremos a medición dos parámetros dos sensores cada hora, mediante: @hourly sh /home/pi/rHorta/medicions_parametros/launcher.sh
* Comprobaremos se fai falta regar (e regarase se é necesario) cada 2 horas, mediante: 0 0,6,8,10,12,16,18,20 * * * /home/pi/rHorta/sistema_rego/launcher.sh

Todos estes métodos crearán logs en ~/rHorta/logs/cronlog
