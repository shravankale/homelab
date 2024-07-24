Here's the updated guide for creating self-signed certificates with the considerations for avoiding passphrases and ensuring proper standards compliance:

---

# How to Create and Store Self-Signed Certificates
Source: Created with the help of ChatGPT

## Overview

This guide will help you create a Certificate Authority (CA) and self-signed certificates for use with local services. It covers the process for creating the CA, generating certificates, using an `openssl-san.cnf` file for SAN (Subject Alternative Name) entries, and securely storing the files on Ubuntu.

## 1. Generate the CA (Certificate Authority)

### 1.1 Create the CA Private Key and Certificate

```bash
# Create a directory for the CA
sudo mkdir -p /etc/ssl/ca
cd /etc/ssl/ca

# Generate the CA private key (without a passphrase)
sudo openssl genpkey -algorithm RSA -out ca-private.key -pkeyopt rsa_keygen_bits:2048

# Generate the CA certificate
# In the command below replace the values at xx as following C:2-digit country code, ST:State, L=City, O:Organization OU:OrganizationUnit, CN=Any name for a certificate authority
sudo openssl req -x509 -new -nodes -key ca-private.key -sha256 -days 3650 -out ca.crt -subj "/C=XX/ST=XX/L=XX/O=XX/OU=XX/CN=XX"
```

### 1.2 Set Permissions

```bash
# Set permissions for the CA files
sudo chmod 600 /etc/ssl/ca/ca-private.key
sudo chmod 644 /etc/ssl/ca/ca.crt
```

## 2. Create the OpenSSL Configuration File

### 2.1 Create the `openssl-san.cnf` File

Create a configuration file for the Subject Alternative Name (SAN) extension:

```bash
sudo nano /etc/ssl/openssl-san.cnf
```
**NOTE:**
1. In the command below replace the values at xx as following C:2-digit country code, ST:State, L=City, O:Organization OU:OrganizationUnit, CN=Any name for a certificate authority
2. Replace *.srv if using another Top-Level Domain (TLD), example *.server. The * indicates a wildcary character meaning a valid certificate would be generated for any xxxx.srv, where xxxx could be a service name such as pihole.

Add the following content:

```ini
[ req ]
default_bits = 2048
default_keyfile = server-private.key
default_md = sha256
prompt = no
distinguished_name = dn
req_extensions = req_ext
x509_extensions = v3_ca

[ dn ]
C = XX
ST = XX
L = XX
O = XX
OU = XX
CN = *.srv

[ req_ext ]
subjectAltName = @alt_names
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth

[ v3_ca ]
subjectAltName = @alt_names
basicConstraints = CA:TRUE
keyUsage = keyCertSign, cRLSign

[ alt_names ]
DNS.1 = *.srv
DNS.2 = srv
```

### 2.2 Set Permissions

```bash
# Set permissions for the OpenSSL configuration file
sudo chmod 644 /etc/ssl/openssl-san.cnf
```

## 3. Generate the Server Certificate

### 3.1 Create the Server Private Key and Certificate Signing Request (CSR)

```bash
# Create a directory for the server certificates
sudo mkdir -p /etc/ssl/server
cd /etc/ssl/server

# Generate the server private key (without a passphrase)
sudo openssl genpkey -algorithm RSA -out server-private.key -pkeyopt rsa_keygen_bits:2048

# Create the CSR
# In the command below replace the values at xx as following C:2-digit country code, ST:State, L=City, O:Organization OU:OrganizationUnit, CN=Any name for a certificate authority
sudo openssl req -new -key server-private.key -out server-private.csr -subj "/C=XX/ST=XX/L=XX/O=XX/OU=XX/CN=*.srv"
```

### 3.2 Generate the Self-Signed Certificate

```bash
# Generate the self-signed certificate using the SAN configuration
sudo openssl x509 -req -in server-private.csr -CA /etc/ssl/ca/ca.crt -CAkey /etc/ssl/ca/ca-private.key -CAcreateserial -out server.crt -days 3650 -extfile /etc/ssl/openssl-san.cnf -extensions req_ext
```

### 3.3 Set Permissions

```bash
# Set permissions for the server files
sudo chmod 600 /etc/ssl/server/server-private.key
sudo chmod 644 /etc/ssl/server/server.crt
sudo chmod 644 /etc/ssl/ca/ca.crt
```

## 4. Distribute the CA Certificate

To avoid browser and OS trust issues, you need to distribute the CA certificate (`ca.crt`) to your client devices (Ubuntu, iPhone, Android, MacBook) and trust it on each device.

### 4.1 Ubuntu

Copy the CA certificate to the system's CA directory:

```bash
sudo cp /etc/ssl/ca/ca.crt /usr/local/share/ca-certificates/ca.crt
sudo update-ca-certificates
```

### 4.2 macOS

1. Open the Keychain Access application.
2. Drag and drop `ca.crt` into the System keychain.
3. Set the certificate to "Always Trust."

### 4.3 iOS

1. Email the `ca.crt` file to yourself or use a secure file-sharing app.
2. Open the file on your iOS device, install the root certificate from Settings app.
3. To authorize the root certificate, Go to Settings --> About --> Certificate Trust --> Enable

### 4.4 Android

1. Copy the `ca.crt` file to your Android device.
2. Go to Settings > Security > Install from storage.
3. Follow the prompts to install the certificate.

## Conclusion

You have now created a Certificate Authority, generated self-signed certificates, and set up your OpenSSL configuration. Ensure that the CA certificate is distributed and trusted on all client devices for a seamless experience.