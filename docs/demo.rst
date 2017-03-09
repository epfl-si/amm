Config :
--------

source ./demo.config

Créer la clé :
--------------

http POST http://127.0.0.1:8888/v1/apikeys/ username="$USERNAME" password="$PASSWORD"


Créer le schema :
-----------------

http POST http://127.0.0.1:8888/v1/schemas/ access_key="c49eca450e1672cef67f" secret_key="7yzQ+J5ZgEMN2IRPTK6P-+yOq68DAGX2qk9BIqVd"

Mettre des données :
--------------------

CREATE TABLE demo (firstName CHAR(50), lastName CHAR(50));
INSERT INTO demo VALUES ("Django", "Reinhardt");
SELECT * FROM demo;

Lister les schémas :
--------------------

http GET http://127.0.0.1:8888/v1/schemas/ access_key=="c49eca450e1672cef67f" secret_key=="7yzQ+J5ZgEMN2IRPTK6P-+yOq68DAGX2qk9BIqVd"

Misc :
------

**redis-cli**

sudo docker-compose exec redis redis-cli

**docker build**

sudo docker build --build-arg MAJOR_RELEASE=0 --build-arg MINOR_RELEASE=1 --build-arg BUILD_NUMBER=5 --no-cache -t epflidevelop/amm .

**launch the test case**

sudo docker-compose exec django ./coverage.sh
