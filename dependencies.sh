#!/bin/bash

# Download dynamodb local
DDB_LOCAL_URL='http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.zip'
wget $DDB_LOCAL_URL

# unzip it
DDB_LOCAL='dynamodb_local_latest.zip'
unzip $DDB_LOCAL

# Run dynamodb local in the background
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb &

# Install pip
sudo easy_install pip

# Install boto3
pip install boto3

# Install matplotlib
sudo apt-get install python-matplotlib

# Install networkx
pip install networkx

# Install BeautifulSoup
sudo apt-get install python-bs4

# Install ntlk
sudo pip install -U nltk

# Install Numpy
sudo pip install -U numpy

# Download stop words
sudo python -m nltk.downloader -d /usr/local/share/nltk_data stopwords
