# Mutual TLS using Openssl and Flask

**Create `certs` folder after cloning repo and execute these commands**

openssl req -nodes -new -x509 -days 365 -keyout ca.key -out ca-crt.pem -subj "/C=US/ST=CA/L=SanFrancisco/O=MyCompany/OU=ITDepartment/CN=localhost-ca"

openssl req -nodes -new -keyout server.key -out server.csr -subj "/C=US/ST=CA/L=SanFrancisco/O=MyCompany/OU=ITDepartment/CN=localhost"

openssl x509 -req -days 365 -in server.csr -CA ca-crt.pem -CAkey ca.key -CAcreateserial -out server.crt

openssl verify -CAfile ca-crt.pem server.crt

openssl req -nodes -new -keyout client.key -out client.csr -subj "/C=US/ST=CA/L=SanFrancisco/O=MyCompany/OU=ITDepartment/CN=localhost.client"

openssl x509 -req -days 365 -in client.csr -CA ca-crt.pem -CAkey ca.key -CAcreateserial -out client.crt

openssl verify -CAfile ca-crt.pem client.crt