#!/bin/bash

read -sp 'Please enter your OpenAI API key: ' open_api_key

if [ -f "openai_api_key.env" ]
then
    rm -f openai_api_key.env
fi

touch openai_api_key.env
echo "OPENAI_API_KEY=\"${open_api_key}\"" > openai_api_key.env

echo
echo "Thank you. Your environment has been set."
