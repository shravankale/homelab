#!/bin/bash
#Updated the Ubuntu certificate store by removing the old certificate and adding the new one
#Remember to 'chmod +x ./updateUbuntuCAStore.sh'

# Define paths
CERT_NAME="caddy-root.crt"
LOCAL_CA_DIR="/usr/local/share/ca-certificates"

# Step 1: Ensure the script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Use 'sudo ./update_caddy_cert.sh'"
   exit 1
fi

# Step 2: Remove the old certificate, if it exists
if [[ -f "$LOCAL_CA_DIR/$CERT_NAME" ]]; then
    echo "Removing old $CERT_NAME from $LOCAL_CA_DIR..."
    rm "$LOCAL_CA_DIR/$CERT_NAME"
else
    echo "No existing $CERT_NAME found in $LOCAL_CA_DIR. Skipping removal."
fi

# Step 3: Update the certificate store to remove the old cert
echo "Updating CA certificates to remove old certificates..."
sudo update-ca-certificates --fresh

# Step 4: Copy the new certificate to the CA directory
if [[ -f "./$CERT_NAME" ]]; then
    echo "Copying new $CERT_NAME to $LOCAL_CA_DIR..."
    cp "./$CERT_NAME" "$LOCAL_CA_DIR"
else
    echo "New $CERT_NAME not found in the current directory. Exiting."
    exit 1
fi

# Step 5: Update the certificate store with the new certificate
echo "Updating CA certificates to include the new certificate..."
sudo update-ca-certificates

echo "CA certificates successfully updated."

