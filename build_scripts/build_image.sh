#!/bin/sh

mkdir -p fabber/bin
cp $FSLDEVDIR/bin/fabber* fabber/bin
docker build -t ibmequbic/quantiphyse . $1
