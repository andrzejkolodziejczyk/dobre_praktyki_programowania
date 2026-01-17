import pika
import time
import json
import os

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f" [x] Rozpoczęto: {data['task_name']} (ID: {data['task_id']})")
    
    time.sleep(30)
    
    print(f" [x] Zakończono: {data['task_id']}")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    host = os.environ.get('RABBITMQ_HOST', 'localhost')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Oczekiwanie na zadania. Naciśnij CTRL+C aby wyjść')

    channel.basic_qos(prefetch_count=1)
    
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()