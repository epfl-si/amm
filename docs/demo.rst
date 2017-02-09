1. Docker
==========

sudo docker-compose build
sudo docker-compose up

Se connecter à django :
sudo docker exec -it amm_django_1 bash

Se connecter à redis :
sudo docker exec -it amm_redis_1 redis-cli

Pour lancer les tests et calculer le coverage
sudo docker-compose exec django ./coverage.sh




2. Echec d'authentification LDAPS
=================================

http POST http://127.0.0.1:8888/v1/apikeys/ username='toto' password='tutu'

HTTP/1.0 401 Unauthorized
Content-Type: application/json
Date: Wed, 08 Feb 2017 09:44:09 GMT
Server: WSGIServer/0.2 CPython/3.5.2
X-Frame-Options: SAMEORIGIN

"Ldaps authentication failed"


3. Créer la clé
===============

http POST http://127.0.0.1:8888/v1/apikeys/ username='kermit' password='XXXXXXXXXXXXXXXXXXXXXX'


4. Récupérer la liste
=====================

http GET http://127.0.0.1:8888/v1/apikeys/ access_key=='XXXXXXXXX' secret_key=='XXXXXXXXX'

http GET http://127.0.0.1:8888/v1/apikeys/ access_key=='36cb0a6b6cf1d3b6160c' secret_key=='ef848027d73fc107126bf38eef4c6480965aa420'

5. Points importants
====================

- Couverture de tests : 91% :

sudo docker-compose exec django ./coverage.sh
chromium-browser ./htmlcov/index.html &

- Respect de la convention PEP8 : 100%
- Code sous github avec mirroir sur c4science

