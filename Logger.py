# -*- coding: utf-8 -*-
#
# Author: Timur Gilmullin, tim55667757@gmail.com


# This module implements Logger.

import sys
import logging


# initialize Main Parent Logger:
LOGGER = logging.getLogger("logger")
sys.stderr = sys.stdout
formatString = "%(filename)-25s[Line:%(lineno)d]\t%(levelname)-10s[%(asctime)s]\t%(message)s"
formatter = logging.Formatter(formatString)  # set default logger formatter


def EnableTestLogger(testLogFileName, parentLoggerHandler=LOGGER, formatting=formatter):
    """
    Start logging for given parent logger handler and test log-file name. Possible, you can use logger formatter.
    Function return new open Logger handler.
    """
    testCaseLogHandler = logging.FileHandler(testLogFileName)  # log handler

    if formatting:
        testCaseLogHandler.setFormatter(formatting)  # set given log formatting

    else:
        testCaseLogHandler.setFormatter(formatter)  # set default log formatting

    parentLoggerHandler.addHandler(testCaseLogHandler)  # init test log

    return testCaseLogHandler


def DisableTestLogger(testLoggerHandler, parentLoggerHandler=LOGGER):
    """
    Stop logging for given test and parents logger handlers.
    """
    if testLoggerHandler:
        testLoggerHandler.flush()  # checks that no write operation to logger
        testLoggerHandler.close()  # stops write to test log file

    if testLoggerHandler in parentLoggerHandler.handlers:
        parentLoggerHandler.removeHandler(testLoggerHandler)  # remove log system handler


LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler()  # initialize Console logger
handler.setFormatter(formatter)  # set standart formatter for Console logger
LOGGER.addHandler(handler)  # adding Console Logger handler to Parent Logger
