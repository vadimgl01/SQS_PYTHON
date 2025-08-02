import boto3
import json
import time
from flask import Flask

app = Flask(__name__)
sqs = boto3.client('sqs', region_name='eu-central-1')
QUEUE_URL = 'https://sqs.eu-central-1.amazonaws.com/342334428607/payment-queue' #Replace with your Queue

@app.route('/')
def health():
    return "Payment Service is running."

def process_payment(order):
    print(f"Processing payment for order: {order['order_id']} with amount: ${order['amount']}")
    time.sleep(2)  # Simulate processing time

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
            process_payment(message)
            sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg['ReceiptHandle'])

if __name__ == '__main__':
    from threading import Thread
    Thread(target=poll_queue, daemon=True).start()
    app.run(port=5001)
