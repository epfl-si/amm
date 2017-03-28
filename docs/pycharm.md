# Pycharm config

## Django Support

File > Settings > Language & Frameworks > Django

* Enable Django Support: Check the checkbox
* Django Projet Root: Select the project /src path on your machine
* Settings: Select the config/settings/local.py path on your machine

File > Settings > Project:amm > Project Structure

* Add the /src directory as **Sources**

## Docker Support

### Install docker-machine

~~~
docker-machine create --driver virtualbox default
eval $(docker-machine env)
~~~

### Start docker-machine

~~~
docker-machine start
eval $(docker-machine env)
~~~


### Configure pycharm

**First make sure to :**
 
* run **eval $(docker-machine env)** to have the correct environment variables
* start the VM : docker-machine start

**Now configure pycharm :**

File > Settings > Build, Execution, Deployment > Docker

* API URL:
  * value of: **echo $DOCKER_HOST**
  
* Certificate folder:
  * value of: **echo $DOCKER_CERT_PATH**
  
* Docker Compose executable: 
  * value of: **which docker-compose**

File > Settings > Project:amm > Project Interpreter

* Click on the Settings wheel and select "Add Remote"
* Select "Docker Compose"
* Configuration file(s) : select your docker-compose.yml file
* Click OK and wait for the indexes to be rebuild (can take several minutes)