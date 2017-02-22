
### Config :

source /opt/projects/amm/demo.config

### Créer la clé :

~~~
http POST http://127.0.0.1:8888/v1/apikeys/ username="$USERNAME" password="$PASSWORD"
~~~

### Créer le schema :

~~~
http POST http://127.0.0.1:8888/v1/schemas/ access_key="ab4b2e297886fe723dfc" secret_key="IyZ+MCr1S-tkryvEJOOmiT1i58GkI4n4onKMElDA"
~~~

### Lister les schémas :

~~~
http GET http://127.0.0.1:8888/v1/schemas/ access_key=="ab4b2e297886fe723dfc" secret_key=="IyZ+MCr1S-tkryvEJOOmiT1i58GkI4n4onKMElDA"
~~~





### Lister les clés :

~~~
http GET http://127.0.0.1:8888/v1/apikeys/ access_key=="6074a93120f0c7150fff" secret_key=="MkxbuAFRXlAkDhSB3-ld-a8RaGBeBoRldwOpmB02"
~~~



sudo docker-compose exec redis redis-cli



sudo docker build --build-arg MAJOR_RELEASE=0 --build-arg MINOR_RELEASE=1 --build-arg BUILD_NUMBER=5 --no-cache -t epflidevelop/amm .

sudo docker-compose exec -T django ./coverage.sh
