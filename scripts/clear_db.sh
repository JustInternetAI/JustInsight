#!/bin/bash

docker exec mongo mongosh -u myuser -p mypassword --authenticationDatabase admin --eval "
  db = db.getSiblingDB('justinsightdb');
  db.dropDatabase();"