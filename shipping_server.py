import boto3
import json
import time
from flask import Flask

app = Flask(__name__)
sqs = boto3.client('sqs', region_name='eu-central-1')
QUEUE_URL = 'https://sqs.eu-central-1.amazonaws.com/342334428607/shipping-queue'

@app.route('/')
def health():
    return "Shipping Service is running."

def prepare_shipping(order):
    print(f"Preparing shipment for order: {order['order_id']} to {order['address']}")
    time.sleep(3)  # Simulate processing

def poll_queue():
    while True:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )
        messages = response.get('Messages', [])
        for msg in messages:
            body = json.loads(msg['Body'])
            message = json.loads(body['Message']) if 'Message' in body else body
            prepare_shipping(message)
            sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg['ReceiptHandle'])

if __name__ == '__main__':
    from threading import Thread
    Thread(target=poll_queue, daemon=True).start()
    app.run(port=5002)