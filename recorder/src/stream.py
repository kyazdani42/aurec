from typing import Any
from video import Frame

from os import environ as env

import pika

HOST = env.get("AUREC_RABBITMQ_IP") or "localhost"
NOTIFICATION_QUEUE = env.get("AUREC_RABBITMQ_NOTIFICATION_QUEUE") or "notifications"
SOCKET_LOCATION = env.get("AUREC_STREAM_SOCKET") or "/tmp/aurec.stream.socket"

class Stream():
    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(HOST))
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue=NOTIFICATION_QUEUE)

    def send_frame(self, frame: Frame):
        with open(SOCKET_LOCATION, "wb") as f:
            f.write(frame)
            f.close()
        
    def send_message(self, kind: str, data: Any):
        body = kind + " | " + data
        self.channel.basic_publish(exchange='amq.direct', routing_key=NOTIFICATION_QUEUE, body=body)
