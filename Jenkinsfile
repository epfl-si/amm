#!/usr/bin/groovy

// Load shared library
@Library('epflidevelop') import ch.epfl.idevelop.container_pipeline
def container_pipeline = new ch.epfl.idevelop.container_pipeline()

def dependencies(start) {
  if (start) {
    // Start dependencies for acceptance tests
  } else {
    // Stop depdencies for acceptance tests
  }
  // return array of arguments for docker run of image
  // can set links with other containers, etc
  return []
}

def unittest() {
  sh "echo yes"
}

def buildcoveragexml() {
}

def acceptancetests(container) {
}

def customBuild(tag) {
    sh "docker build --no-cache --build-arg REQUIREMENTS_FILE='requirements/prod.txt' --build-arg MAJOR_RELEASE=0 --build-arg MINOR_RELEASE=1 --build-arg BUILD_NUMBER=5 . -t ${tag}"
    return docker.image(tag)
}

container_pipeline.process(
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
  '0',
  // minor version of image
  '1',
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
  'amm-ci@groupes.epfl.ch'
)