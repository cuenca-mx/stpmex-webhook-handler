import json
import os
import threading

import pika

from speid.rabbit.base import RPC_QUEUE


def on_request(ch, method, props, body):
    print("Received RCP: \n %r" % str(body))
    response = "Ok"
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


class ConsumerThread(threading.Thread):
    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=os.environ['AMPQ_ADDRESS']))
        channel = connection.channel()
        channel.queue_declare(queue=RPC_QUEUE)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(on_request, queue=RPC_QUEUE)

        print("Waiting for the message...")

        def stop():
            channel.stop_consuming()

        connection.add_timeout(10, stop)
        channel.start_consuming()
        connection.close()


class TestReceiveOrder:

    def test_create_order_event(self, app):
        thread = ConsumerThread()
        thread.start()
        data = dict(
            Clave=2456303,
            FechaOperacion=20180618,
            InstitucionOrdenante=846,
            InstitucionBeneficiaria=90646,
            ClaveRastreo="PRUEBATAMIZI1",
            Monto=100.0,
            NombreOrdenante="BANCO",
            TipoCuentaOrdenante=40,
            CuentaOrdenante="846180000500000008",
            RFCCurpOrdenante="ND",
            NombreBeneficiario="TAMIZI",
            TipoCuentaBeneficiario=40,
            CuentaBeneficiario="646180157000000004",
            RFCCurpBeneficiario="ND",
            ConceptoPago="PRUEBA",
            ReferenciaNumerica=2423,
            Empresa="TAMIZI",
            estado="estado"
        )
        res = app.post('/ordenes', data=json.dumps(data),
                       content_type='application/json')

        assert res.status_code == 201
