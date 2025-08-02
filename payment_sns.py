import boto3
import json

sns = boto3.client('sns', region_name='eu-central-1')

response = sns.publish(
    TopicArn='arn:aws:sns:eu-central-1:342334428607:Payment.fifo',
    Message=json.dumps({
        "order_id": "ORD123",
        "amount": 104.50,
        "address": "AWS Street"
    }),
    MessageGroupId='group1'  # Required for FIFO topics
)

print("Message published. ID:", response['MessageId'])