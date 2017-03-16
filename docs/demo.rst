Config :
--------

source ./demo.config

Créer la clé :
--------------

http POST http://127.0.0.1:8000/v1/apikeys/ username="$USERNAME" password="$PASSWORD"


Créer le schema :
-----------------

http POST http://127.0.0.1:8000/v1/schemas/ access_key="22924b850ea0e5475af3" secret_key="H1D8NzpflXhl+rhxOamEpJ-XsFjJ-zOk804RV2dn"

Lister les schémas :
--------------------

http GET http://127.0.0.1:8000/v1/schemas/ access_key=="22924b850ea0e5475af3" secret_key=="H1D8NzpflXhl+rhxOamEpJ-XsFjJ-zOk804RV2dn"

v1/schemas/?access_key=22924b850ea0e5475af3&secret_key=H1D8NzpflXhl+rhxOamEpJ-XsFjJ-zOk804RV2dn

Misc :
------

**redis-cli**

sudo docker-compose exec redis redis-cli

**docker build**

sudo docker build --build-arg MAJOR_RELEASE=0 --build-arg MINOR_RELEASE=1 --build-arg BUILD_NUMBER=5 --no-cache -t epflidevelop/amm .

**launch the test case**

sudo docker-compose exec django ./coverage.sh
