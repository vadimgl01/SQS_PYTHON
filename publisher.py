import boto3
import json

sqs = boto3.client('sqs', region_name='us-east-1')

payment_queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/payment-queue'
shipping_queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/shipping-queue'

order = {
    "order_id": "ORD12345",
    "amount": 59.99,
    "address": "123 AWS Lane, Cloud City"
}

# Send to Payment Queue
sqs.send_message(
    QueueUrl=payment_queue_url,
    MessageBody=json.dumps(order)
)

# Send to Shipping Queue
sqs.send_message(
    QueueUrl=shipping_queue_url,
    MessageBody=json.dumps(order)
)

print("Message sent to both queues.")