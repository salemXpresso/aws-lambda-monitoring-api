from OpenSSL import crypto
from datetime import datetime
from socket import *
import ssl
import socket
import os
import json
import urllib
import logging

##
# Phase 1: the function will get the server certificate and verify that it is not expired. It will not complete any handshake nor verify if the certificate is revoked or
# if the certificate has been signed by a trusted authority. Therefor you can check certificates signed by Let's Encrypt without having to care about configuring your truststore.
# 
# Phase 2: the function will send a request to the input API URL (200 OK is expected) and tries to parse the retrieved JSON (TLS is 'insecured' during this phase).
# 
# During phase 1 or phase 2, if an error occurs. A notification will be sent to warn the administrator that his API is encountering a problem.
#
# Lambda environment variables have to be defined to customize the API you want to monitor: 
# - ServerName
# - ServerPort
# - ApiUrl
#
# On Linux environment, install the following librairies using pyp and execute the following command to package the whole module (inside src dir):
# zip -r9 ../api-monitoring.zip .
##

def lambda_handler(event, context):
    
    endpoint = os.environ.get('ServerName', 'tls-v1-2.badssl.com')
    port = os.environ.get('ServerPort', '1012')
    apiUrl = os.environ.get('ApiUrl', 'https://badssls.com:1012/')
  
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
  
    logger.debug("Checking server certificate: " +  endpoint)
    try:
        setdefaulttimeout(2)
        cert = ssl.get_server_certificate((endpoint, int(port)))
    except IOError as ioe:
        logger.error("Could not join server: " + str(ioe))
        return
    
    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    notAfterDate = datetime.strptime(x509.get_notAfter(), "%Y%m%d%H%M%SZ")
    if(notAfterDate < datetime.now()):
        logger.error("Error: certificate expired: " + notAfterDate)
    else: 
        logger.debug("Certificate expiration ok")
        ssl._create_default_https_context = ssl._create_unverified_context
        try:
            response = urllib.urlopen(apiUrl)
            if response.getcode() != 200:
                logger.error("Status NOK: " + str(response.getcode()))
            else:
                logger.debug("Status OK")
                try:
                    out = json.load(response)
                    #logger.debug("parsed json" + str(out))
                except Exception as e: 
                    logger.error("Error: the server did not return a valid JSON: " + str(e))
        except IOError as ioe:
            logger.error("Could not join server endpoint: " + str(ioe))
        
        
        
def main():
  
  handler = logging.StreamHandler()
  handler.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  handler.setFormatter(formatter)
  logger = logging.getLogger()
  logger.addHandler(handler)
  
  lambda_handler(None, None)
  
if __name__== "__main__":
  main()


