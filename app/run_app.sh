#!/bin/bash

if [ "$1" = "-c" ]
then
  echo "Clearing previously stored queries..."
  rm -f queries.json
  shift
fi

if [ "$1" = "-t" ]
then
  cd ../core_ce/model_creation
  ./delete_models.sh
  shift
  if [ "$1" = "-u" ]
  then
    echo "Re-downloading PW documentation and re-training models..."
    ./install_models.sh -u
  else
    echo "Re-training models..."
    ./install_models.sh
  fi
  shift
  cd ../../ask_pw_app
fi

streamlit run ask_pw_app.py

