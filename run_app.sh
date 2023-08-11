#!/bin/bash

cd app

# Code for a bunch of tags to brute-force accomplish clearing, model deletion, model re-training, and model creation. Only useful if DVC and/or Streamlit buttons stop working and you need to undergo these tasks via terminal.
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


# Need to send port from cluster to usercontainer to properly display on the platform
# Script port.sh in pw-dvc-workflow contains code to find an open port.

# ssh -R <local_port>:<cluster_ip>:<remote_port> cluster_ip

