import sys
import pika
from pika import spec


credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()
channel.exchange_declare(exchange="hello-exchange",
                         exchange_type="direct",
                         passive=False,
                         durable=True,
                         auto_delete=False)

def confirm_handler(frame):
    if type(frame.method) == spec.Confirm.SelectOk:
        print("Channel in confirm mode")
    elif type(frame.method) == spec.Basic.Nack:
        if frame.method.delivery_tag in msg_ids:
            print("Message is lost!!!")
    elif type(frame.method) == spec.Basic.Ack:
        print("Confirm received")
        msg_ids.remove(frame.method.delivery_tag)


msg_ids = []
channel.confirm_delivery()
msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

try:
    channel.basic_publish(body=msg,
                      exchange="hello-exchange",
                      properties=msg_props,
                      routing_key="hola")
    print("Message has been received")
except:
    print("Message has not been received")
msg_ids.append(len(msg_ids) + 1)
channel.close()
