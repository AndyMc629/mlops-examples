#!/bin/bash

# Delete existing admin
airflow users delete --username admin

# Instantiate new admin
airflow users create \
  --username admin \
  --firstname "Admin" \
  --lastname "User" \
  --role "Admin" \
  --email "admin@example.com" \
  --password "admin"
