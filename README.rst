nxlogger
========

A Python Logging Handler for RabbitMQ (http://www.rabbitmq.com)


Usage
-----

The RabbitMQLogHandler creates a named Exchange in RabbitMQ for Logging.
By default, the Exchange is called **logs** and is defined as a **topic**
Exchange. These Parameters can be changed in the constructor of the
RabbitMQLogHandler::

    RabbitMQLogHandler(host="localhost", port=5672, exchange="logs", type="topic")

As long as there are *no* Queues connected, the log messages get *trashed*.

Example Code::

    import logging
    from nexiles.logger.handler import RabbitMQLogHandler

    logger = logging.getLogger("rabbitlog")
    logger.setLevel(logging.INFO)

    rabbitmq_handler = RabbitMQLogHandler()
    logger.addHandler(rabbitmq_handler)

    logger.info("Now logging to RabbitMQ, no matter if there are Queues or not...")


Receiving Logs
--------------

To receive logs, we have to connect to the named Exchange (default: logs).
A Consumer can decide over the **routing_key** which type of logs it can
handle, e.g. **INFO** for Info logs only or **#** for all logs.

Example code (receive_logs.py)::

    import pika

    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()

    # just to be sure
    channel.exchange_declare(exchange='logs', type='topic')

    # queue will be deleted after disconnecting
    result = channel.queue_declare(exclusive=True)

    # creates a queue with a random name
    queue_name = result.method.queue

    # bind to the named **logs** exchange and accept all logging severities
    # with the routing_key #
    channel.queue_bind(exchange='logs',
                       routing_key="#",
                       queue=queue_name)

    # simple print callback
    def callback(ch, method, properties, body):
        print "%r" % (body,)

    # we don't care about losing logs....
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    # consume forever
    channel.start_consuming()

.. vim: set ft=rst ts=4 sw=4 expandtab tw=78 :
