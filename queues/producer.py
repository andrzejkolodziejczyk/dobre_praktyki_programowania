import pika
import json

def add_jobs(count=100):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    for i in range(1, count + 1):
        message = {
            "task_id": i,
            "task_name": f"Rozmowa telefoniczna nr {i}"
        }
        
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            ))
        print(f" [x] Wysłano zadanie nr {i}")

    connection.close()

if __name__ == "__main__":
    add_jobs(1)