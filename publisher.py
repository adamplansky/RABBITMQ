#!/usr/bin/env python
import pika
import sys
import ssl
import os

ssl_options = {
    "ca_certs":"/Users/adamplansky/Desktop/message_app/testca/cacert.pem",
    "certfile": "/Users/adamplansky/Desktop/message_app/client/cert.pem",
    "keyfile": "/Users/adamplansky/Desktop/message_app/client/key.pem",
    "cert_reqs": ssl.CERT_REQUIRED,
    "ssl_version":ssl.PROTOCOL_TLSv1_2
}
credentials = pika.PlainCredentials(os.environ['RABBITMQ_USERNAME'], os.environ['RABBITMQ_PASSWORD'])
parameters = pika.ConnectionParameters(host='192.168.2.120',
    port=5671,
    virtual_host='/',
    heartbeat_interval = 0,
    credentials=credentials,
    ssl = True,
    ssl_options = ssl_options)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print(" [x] Sent %r" % message)
connection.close()
