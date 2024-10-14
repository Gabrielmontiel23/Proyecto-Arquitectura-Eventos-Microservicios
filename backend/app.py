from flask import Flask, request, jsonify
import pika
import json
from flask_cors import CORS

app = Flask(__name__)

CORS(app) 

# Función para enviar eventos a RabbitMQ
def send_to_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='transactionQueue')
    channel.basic_publish(exchange='',
                          routing_key='transactionQueue',
                          body=json.dumps(message))
    connection.close()

# Endpoint para procesar un pago
@app.route('/api/process-payment', methods=['POST'])
def process_payment():
    transaction_details = request.json
    send_to_queue(transaction_details)
    return jsonify({"status": "Transaction Sent"}), 200

@app.route('/')
def index():
    return "Bienvenido al sistema de procesamiento de pagos!"


if __name__ == '__main__':
    app.run(debug=True)
