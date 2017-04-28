#!/usr/bin/groovy

// Load shared library
@Library('epflidevelop') import ch.epfl.idevelop.container_pipeline
pipeline = new ch.epfl.idevelop.container_pipeline()

redis_container = null

def dependencies(start) {
  if (start) {
    // Start dependencies for acceptance tests
    redis_container = docker.image('redis').run()
    sh "docker exec -i ${redis_container.id} ip route get 1 | awk '{print \$NF;exit}' > /tmp/ip "
  } else {
    // Stop depdencies for acceptance tests
    sh "docker rm -f ${redis_container.id}"
  }

  redisip = readFile('/tmp/ip').trim()
  accesskey = null
  secretkey = null
  username = null
  password = null
  rancher_env_id = null
  accred_password = null

  withCredentials(
    [[$class: 'UsernamePasswordMultiBinding',
    credentialsId: 'amm-test-rancher-creds',
    usernameVariable: 'ACCESSKEY',
    passwordVariable: 'SECRETKEY']]
  ) {
    accesskey = "${ACCESSKEY}"
    secretkey = "${SECRETKEY}"
  }

  withCredentials(
    [[$class: 'UsernamePasswordMultiBinding',
    credentialsId: 'ldap-test-credentials',
    usernameVariable: 'USERNAME',
    passwordVariable: 'PASSWORD']]
  ) {
    username = env.USERNAME
    password = env.PASSWORD
  }

  withCredentials([string(credentialsId: 'amm-test-environment-id', variable: 'SECRET')]) {
    rancher_env_id = "${SECRET}"
  }

  withCredentials([string(credentialsId: 'amm-accred-password', variable: 'SECRET')]) {
    accred_password = "${SECRET}"
  }

  // return array of arguments for docker run of image
  // can set links with other containers, etc
  return [
    "-e", "LDAP_BASE_DN=o=epfl,c=ch",
    "-e", "LDAP_SERVER=scoldap.epfl.ch",
    "-e", "LDAP_SERVER_FOR_SEARCH=ldap.epfl.ch",
    "-e", "LDAP_USER_SEARCH_ATTR=uid",
    "-e", "CACHE_REDIS_LOCATION=redis://${redisip}:6379/1",
    "-e", "CACHE_REDIS_CLIENT_CLASS=django_redis.client.DefaultClient",
    "-e", "TEST_USERNAME=${username}",
    "-e", "TEST_CORRECT_PWD=${password}",
    "-e", "TEST_WRONG_PWD=test_wrong_pwd",
    "-e", "SECRET_KEY=dummy_value_since_it_is_not_important",
    "-e", "LDAP_USE_SSL=false",
    "-e", "DJANGO_WORKER_COUNT=1",
    "-e", "REST_API_ADDRESS=localhost",
    "-e", "RANCHER_ACCESS_KEY=${accesskey}",
    "-e", "RANCHER_SECRET_KEY=${secretkey}",
    "-e", "RANCHER_VERIFY_CERTIFICATE=true",
    "-e", "RANCHER_API_URL=https://test-rancher.epfl.ch",
    "-e", "DJANGO_SETTINGS_MODULE=config.settings.test",
    "-e", "AMM_ENVIRONMENT=${rancher_env_id}",
    "-e", "ACCRED_PASSWORD=${accred_password}",
    "-e", "DJANGO_DEBUG=True",
    "-e", "AMM_MYSQL_DOMAIN=.example.com",
  ]
}

def unittest() {
}

def buildcoveragexml() {
}

def acceptancetests(container) {
  sh "docker exec -i ${container.id} pip install -r requirements/local.txt"
  sh "docker exec -i ${container.id} coverage run --source='.' src/manage.py test --settings=config.settings.test --exclude-tag=rancher"
}

majorversion = 0
minorversion = 1

def customBuild(tag) {
  buildversion = pipeline.get_build_version(majorversion, minorversion)
  sh "docker build --no-cache --build-arg REQUIREMENTS_FILE='requirements/prod.txt' --build-arg MAJOR_RELEASE=${this.majorversion} --build-arg MINOR_RELEASE=${this.minorversion} --build-arg BUILD_NUMBER=${buildversion} -t ${tag} ."
  return docker.image(tag)
}

pipeline.process(
  // project name, will be image name and git repository name
  'amm',
  // template name is rancher-template-$this_value
  'amm',
  // Docker organisation name, i.e. the prefix of the image
  'epflidevelop',
  // function that returns start/stops the dependencies of the docker image
  // returns arguments to add to the docker run of the image
  this.&dependencies,
  // definition of unit tests, executed before building the image
  this.&unittest,
  // method to build the coverage.xml file to import into cobertura
  this.&buildcoveragexml,
  // acceptance tests to run on the image before publishing it
  this.&acceptancetests,
  // major version of image
  majorversion,
  // minor version of image
  minorversion,
  // custom build method for image
  // if it needs some custom arguments a simple:
  // "docker build ." doesn't provide set to null to use "docker build ."
  this.&customBuild,
  // array of arguments to pass to docker run of image
  // to set environment variables etc
  [],
  // ID of the credential to use for writing to github image and template repositories.
  'amm-token',
  // name of the github organization
  'epfl-idevelop',
  // ID of the credential to use for writing to dockerhub
  'dockerhub-epflidevelop-jenkins-ci',
  // email address to use for jenkins automated commits
  'amm-ci@groupes.epfl.ch',
  // prefix of the repository used to push new tags
  ''
)
