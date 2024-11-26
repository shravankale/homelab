#!/bin/bash
# To execute remember to run 'chmod +x getCaddyCertificate.sh'

# Copy the root certificate from the Docker container to the current directory
sudo docker cp caddy:/data/caddy/pki/authorities/local/root.crt ./caddy-root.crt

# Print a message instructing the user to move the file
echo "Move the root certificate to the 'caddy/certs' directory using the following command:"
echo "mv ./caddy-root.crt caddy/certs"