#!/bin/bash

mkdir data
var=$1

# venv
create_env() {
  echo "Initializing virtual enviorement VENV"
  virtualenv -p /usr/bin/python3 venv 
  source venv/bin/activate
  pip3 install -r requeriments.txt
}

# data
if [ -z "$var" ]; then
  echo "A option is needed!"
else
  if [ "$var" = "s" ]; then
    cd data 
    echo "Configuring SMALL dataset"
    wget https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
    unzip ml-latest-small.zip
    rm ml-latest-small.zip
    cd .. 
    echo "Small Data Generated in ./data!"
    create_env
  elif [ "$var" = "f" ]; then
    cd data
    echo "Configuring FLL dataset"
    wget https://files.grouplens.org/datasets/movielens/ml-latest.zip
    unzip ml-latest.zip
    rm ml-latest.zip
    cd .. 
    echo "Full Data Generated in ./data!"
  else
    echo "The var is not a option!"
    create_env
  fi 
fi
