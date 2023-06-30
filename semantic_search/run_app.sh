#!/bin/bash

if [ "$1" = "-c" ]
then
  echo "Clearing previously stored queries..."
  rm -f queries.json
  shift
fi

if [ "$1" = "-t" ]
then
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
fi

streamlit run askpw_app.py

