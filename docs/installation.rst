============
Installation
============


Step 0 :
--------

You need to install :

* Redis : https://redis.io/
* virtualenvwrapper : https://virtualenvwrapper.readthedocs.io/en/latest/


Step 1 : Put yourself in your working directory
-----------------------------------------------
cd ~/workspace

Step 2 : Recovers project sources
---------------------------------

git clone https://github.com/epfl-idevelop/amm

Step 3 : Place yourself at the root of the project
--------------------------------------------------

cd amm

Step 4 : Create a python virtualenv
-----------------------------------

mkvirtualenv --python=/usr/bin/python3 amm

Step 5 : Install all third packages
-----------------------------------

pip install -r requirements/local.txt

Step 6 : Create secrets file
----------------------------

Create a file **/secrets.json** and copy/paste the following content :

{
  "FILENAME": "secrets.json",

  "SECRET_KEY": "kltq(&9-6f1vnc&4kk8mom@u=2+w)^twofvlef6^qp8i4#ezg@"

}


Step 7 : Run the django development server
------------------------------------------

python src/manage.py runserver --setting=config.settings.local
