#!/usr/bin/env python
import pika
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
parameters = pika.ConnectionParameters(host='192.168.2.120', port=5671, virtual_host='/', heartbeat_interval = 0, credentials=credentials, ssl = True, ssl_options = ssl_options)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# ''' start subscriber '''

channel.exchange_declare(exchange='logs', exchange_type='fanout') #fanout == type broadcast #exchange == name

result = channel.queue_declare(exclusive=True) #i want random name of queue, exlusive == true, when we disconnect delete queue
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
