#!/bin/bash

read -sp 'Please enter your OpenAI API key: ' open_api_key

if [ -f "open_api_key.env" ]
then
    rm -f open_api_key.env
fi

touch open_api_key.env
echo "OPENAI_API_KEY=\"${open_api_key}\"" > open_api_key.env

echo
echo "Thank you. Your environment has been set."
