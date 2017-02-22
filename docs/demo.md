
source /home/me/Desktop/demo.txt

Créer la clé :


http POST http://127.0.0.1:8888/v1/apikeys/ username="$USERNAME" password="$PASSWORD"


http POST http://127.0.0.1:8888/v1/apikeys/ username="$USERNAME" password="$PASSWORD"



http GET http://127.0.0.1:8888/v1/apikeys/ access_key=='XXXXXXXXX' secret_key=='XXXXXXXXX'

http GET http://127.0.0.1:8888/v1/apikeys/ access_key=='36cb0a6b6cf1d3b6160c' secret_key=='ef848027d73fc107126bf38eef4c6480965aa420'

5. Points importants
====================

- Couverture de tests : 91% :

sudo docker-compose exec django ./coverage.sh
chromium-browser ./htmlcov/index.html &

- Respect de la convention PEP8 : 100%
- Code sous github avec mirroir sur c4science

