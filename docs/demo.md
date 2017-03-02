
### Config :

source /opt/projects/amm/demo.config

### Créer la clé :

~~~
http POST http://127.0.0.1:8888/v1/apikeys/ username="$USERNAME" password="$PASSWORD"
~~~

### Créer le schema :

~~~
http POST http://127.0.0.1:8888/v1/schemas/ access_key="737189d61b0d2b49d032" secret_key="X2QYzuP6GrZMxFLATNPM083vfIt8E7xXQ3UsmV5D"
~~~

### Lister les schémas :

~~~
http GET http://127.0.0.1:8888/v1/schemas/ access_key=="737189d61b0d2b49d032" secret_key=="X2QYzuP6GrZMxFLATNPM083vfIt8E7xXQ3UsmV5D"
~~~


### Misc :

** redis-cli **

sudo docker-compose exec redis redis-cli

** docker build **

sudo docker build --build-arg MAJOR_RELEASE=0 --build-arg MINOR_RELEASE=1 --build-arg BUILD_NUMBER=5 --no-cache -t epflidevelop/amm .

** launch the test case **

sudo docker-compose exec django ./coverage.sh
