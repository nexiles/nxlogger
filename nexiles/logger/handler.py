# -*- coding: utf-8 -*-
#
# File: handler.py
#
# Copyright (c) Nexiles GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__ = 'Ramon Bartl <ramon.bartl@nexiles.de>'
__docformat__ = 'plaintext'

import logging
from pika import BlockingConnection
from pika import ConnectionParameters


class RabbitMQLogHandler(logging.Handler):
    """ Log Handler for RabbitMQ

        >>> logger = logging.getLogger("rabbitlog")
        >>> logger.setLevel(logging.DEBUG)
        >>> rabbitmq_handler = RabbitMQLogHandler()
        >>> logger.addHandler(rabbitmq_handler)
        >>> logger.info("info log message")
    """

    def __init__(self, host="localhost", port=5672, exchange="logs", type="topic"):
        logging.Handler.__init__(self)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.setFormatter(formatter)
        self.host = host
        self.port = port
        self.exchange = exchange
        self.type = type

    @property
    def connection(self):
        """ rabbitmq connection
        """
        return BlockingConnection(
                ConnectionParameters(host=self.host, port=self.port)
                )

    @property
    def channel(self):
        """ queue channel
        """
        channel = self.connection.channel()
        channel.exchange_declare(exchange=self.exchange, type=self.type)
        return channel

    def message(self, message, severity="INFO"):
        """ sends a message to the queue
        """
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=severity,
                                   body=message)

    def emit(self, record):
        """ logs the record to rabbitmq
        """
        self.message(self.format(record), severity=record.levelname)

    def close(self):
        """ tidy up network connection
        """
        self.connection.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()

# vim: set ft=python ts=4 sw=4 expandtab :
