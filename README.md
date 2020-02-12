# Quantiphyse-Docker

Scripts for building and running Quantiphyse in a Docker container.

    https://www.docker.com/
    
Docker is a technology which allows applications and their dependencies to be pre-built and executed in an isolated
environment under a different (but broadly compatible) operating system. It can be thought of as a more lightweight
alternative to a virtual machine.

The advantage of running an application like Quantiphyse as a Docker image is that you don't need to worry about
installing dependencies or having the right version of Python, etc. That's all been done already and is built into
the image. You just need a compatible OS to run the container (Linux or Mac currently).

## Running Quantiphyse as a docker image

    quantiphyse-docker.py
    
This simple Python script will pull the current Quantiphyse image from Docker Hub and execute it. It will map your home
folder to the container and also your FSL directories.

Note that FSL functionality will only work if your platform is binary compatible with Ubuntu 18.04.

## Building a new image

    build_scripts/build_image.sh --no-cache

`container_scripts` contains scripts which are copied to the container to ensure that Quantiphyse starts up correctly under 
a matching user name / ID.

## Notes

It is a little inconvenient that we need to write a Python script to actually execute the container. It would be nice to just do:

    docker run ibmequbic/quantiphyse
    
Unfortunately Docker doesn't seem to have the ability to attach a startup script to an image to do things like map the X display
to the container or pass environment variables. So we need the wrapper script to do these things. It would be a great addition
to Docker to incorporate this feature (in some secure manner).
