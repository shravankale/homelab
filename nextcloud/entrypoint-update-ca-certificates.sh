#!bin/bash

#Check for certificate updates and update if necessary
./update-ca-certificate

#Start the nextcloud process
exec "$@"