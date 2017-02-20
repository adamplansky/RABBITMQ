import pika
import json
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

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    data = json.loads(body.decode("utf-8"))
    print(data)





channel.basic_consume(callback,queue='hello',no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
