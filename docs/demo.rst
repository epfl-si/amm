0. Echec d'authentification LDAPS
=================================

http POST http://127.0.0.1:8000/v1/apikeys/ username='toto' password='tutu'

HTTP/1.0 401 Unauthorized
Content-Type: application/json
Date: Wed, 08 Feb 2017 09:44:09 GMT
Server: WSGIServer/0.2 CPython/3.5.2
X-Frame-Options: SAMEORIGIN

"Ldaps authentication failed"


1. Créer la clé
===============

http POST http://127.0.0.1:8000/v1/apikeys/ username='kermit' password='XXXXXXXXXXXXX'


2. Récupérer la liste
=====================

http GET http://127.0.0.1:8000/v1/apikeys/ access_key=='XXXXXXXXX' secret_key=='XXXXXXXXX'

http GET http://127.0.0.1:8000/v1/apikeys/ access_key=='ee3a52cbaadf239c9a40' secret_key=='9e786a7c64dc4e4c149a071510f0b583acfe7c0e'

3. Points importants
====================

- Couverture de tests : 91%
file:///home/greg/workspace-idevelop/amm/htmlcov/index.html

- Respect de la convention PEP8 : 100%
- Code sous github avec mirroir sur c4science

