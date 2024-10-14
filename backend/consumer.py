import pika
import json

def callback(ch, method, properties, body):
    transaction_details = json.loads(body)
    print(f" [x] Received Transaction: {transaction_details}")
    # Aquí puedes añadir lógica para procesar la transacción

# Conectar a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar la cola
channel.queue_declare(queue='transactionQueue')

# Escuchar mensajes
channel.basic_consume(queue='transactionQueue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
