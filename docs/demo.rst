Config :
--------

source ./demo.config

Créer la clé :
--------------

http POST http://127.0.0.1:8888/v1/apikeys/ username="$USERNAME" password="$PASSWORD"


Créer le schema :
-----------------

http POST http://127.0.0.1:8888/v1/schemas/ access_key="804a5a0957d629e6bc6c" secret_key="qKE+0EL0qqI2wn9rcc20UIj-eN2kk+bSwkdlmzN0"

Lister les schémas :
--------------------

http GET http://127.0.0.1:8888/v1/schemas/ access_key=="804a5a0957d629e6bc6c" secret_key=="qKE+0EL0qqI2wn9rcc20UIj-eN2kk+bSwkdlmzN0"

Misc :
------

**redis-cli**

sudo docker-compose exec redis redis-cli

**docker build**

sudo docker build --build-arg MAJOR_RELEASE=0 --build-arg MINOR_RELEASE=1 --build-arg BUILD_NUMBER=5 --no-cache -t epflidevelop/amm .

**launch the test case**

sudo docker-compose exec django ./coverage.sh
