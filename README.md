# aws-lambda-monitoring-api
This module aims to monitor a Json API certificate expiration and response codes periodically

Phase 1: if the certificate has been signed by a trusted authority. Therefor you can check certificates signed by Let's Encrypt without having to care about configuring your truststore.
 
Phase 2: the function will send a request to the input API URL (200 OK is expected) and tries to parse the retrieved JSON (TLS is 'insecured' during this phase).

During phase 1 or phase 2, if an error occurs. A notification will be sent to warn the administrator that his API is encountering a problem.

Lambda environment variables have to be defined to customize the API you want to monitor: 
- ServerName
- ServerPort
- ApiUrl

On Linux environment, install the librairies using pip (pyopenssl, requests, datetime) and execute the following command to package the whole module (inside src dir):
zip -r9 ../api-monitoring.zip .
