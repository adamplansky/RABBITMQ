# #!/usr/bin/env python

import pika
import ssl
import json
import os


# ssl_options = {
#     "ca_certs":"/Users/adamplansky/Desktop/message_app/testca/cacert.pem",
#     "certfile": "/Users/adamplansky/Desktop/message_app/client/cert.pem",
#     "keyfile": "/Users/adamplansky/Desktop/message_app/client/key.pem",
#     "cert_reqs": ssl.CERT_REQUIRED,
#     "ssl_version":ssl.PROTOCOL_TLSv1_2
# }
credentials = pika.PlainCredentials('guest','guest')
parameters = pika.ConnectionParameters(host='chablis.liberouter.org',
    port=5671,
    virtual_host='/',
    credentials=credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='hello')
data = {
    "id": 1,
    "name": "My Name",
    "description": "This is description about me"
}
message = json.dumps(data)
channel.basic_publish(exchange='',routing_key='hello',body=message)
print(" [x] Sent 'Hello World!'")
connection.close()
