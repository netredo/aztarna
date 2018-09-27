#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import ipaddress
import logging
from ipaddress import IPv4Address, ip_network
import sys

logger = logging.getLogger(__name__)


class BaseScanner:
    """
    BaseScanner class, an abstraction for different ROS type scans (ROS, SROS, ROS 2)
    """
    def __init__(self, ports=[11311], extended=False):
        self.host_list = []
        self.ports = ports
        self.extended = extended
        self.input = False
        self._rate = 1000
        self.semaphore = asyncio.Semaphore(self._rate)

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        self._rate = rate
        self.semaphore = asyncio.Semaphore(rate)

    def load_from_file(self, filename):
        """
        Load a range of ipv4 addresses to scan and add them The :class:BaseScanner host_list attribute
        :param filename: name of the input file
        """
        with open(filename, 'r') as file:
            for line in file.readlines():
                try:
                    address = ipaddress.ip_address(line.rstrip('\n'))
                    self.host_list.append(address)
                except ValueError:
                    logger.warning('Invalid IP address in input file')

    def load_range(self, net_range):
        """
        Transform ipv4 address strings to pythons ipaddress library type objects for scanning purposes
        :param net_range: A range of string type IPv4 addresses
        """
        network = ip_network(net_range)
        if network.netmask == IPv4Address('255.255.255.255'):
            self.host_list = [IPv4Address(net_range)]
        else:
            self.host_list = list(network.hosts())

    @staticmethod
    def pipe_stdout(self):
        # use stdin if it's full
        if not sys.stdin.isatty():
            input_stream = sys.stdin

        # otherwise, read the given filename
        else:
            try:
                input_filename = sys.argv[1]
            except IndexError:
                message = 'need filename as first argument if stdin is not full'
                raise IndexError(message)
            else:
                input_stream = open(input_filename, 'rU')

        for line in input_stream:
            self.scan()

    def scan(self):
        raise NotImplementedError

    def scan_pipe(self):
        raise NotImplementedError

    def print_results(self):
        raise NotImplementedError

    def write_to_file(self, out_file):
        raise NotImplementedError


class BaseHost:
    """
    A base class for ROS hosts
    """
    def __init__(self):
        self.address = ''
        self.port = ''
        self.nodes = []


class BaseNode:
    """
    A base class for ROS nodes
    """
    def __init__(self):
        self.name = ''
        self.address = ''
        self.port = ''


class BaseTopic:
    """
    A base class for ROS topics
    """
    def __init__(self):
        self.name = ''
        self.type = ''


class BaseService:
    """
    A base class for ROS services
    """
    def __init__(self):
        self.name = ''


class Parameter:
    """
    A class representing a ROS parameter
    """
    def __init__(self):
        self.name = ''
        self.type = ''
        self.value = ''


class Communication:
    """
    A class representing a ROS communication, including the publishers, subscribers and the topics involveds
    """
    def __init__(self, topic):
        self.publishers = []  # Node type
        self.subscribers = []  # Node type
        self.topic = topic # Topic() object
