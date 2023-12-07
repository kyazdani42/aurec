from typing import Any
from video import Frame, to_binary

from os import environ as env

import pika

HOST = env.get("AUREC_RABBITMQ_IP") or "localhost"
BLOB_QUEUE = env.get("AUREC_RABBITMQ_VIDEO_BLOB_QUEUE") or "blob"
NOTIFICATION_QUEUE = env.get("AUREC_RABBITMQ_NOTIFICATION_QUEUE") or "notifications"

class Stream():
    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(HOST))
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue=BLOB_QUEUE, auto_delete=True)
        self.channel.queue_purge(queue=BLOB_QUEUE)
        self.channel.queue_declare(queue=NOTIFICATION_QUEUE)

    def send_frame(self, frame: Frame):
        blob = to_binary(frame)
        self.channel.basic_publish(exchange='', routing_key=BLOB_QUEUE, body=blob)

    def send(self, kind: str, data: Any):
        body = kind + " | " + data
        self.channel.basic_publish(exchange='', routing_key=NOTIFICATION_QUEUE, body=body)
