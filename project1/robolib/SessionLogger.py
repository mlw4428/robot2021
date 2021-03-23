from datetime import datetime
import sys
from sys import stdout
import logging, logging.handlers

logName = "ROBITLOG: "
sessionLogFilename = datetime.now().strftime('robit_' + '%m_%d_%Y@%H_%M_.log')
logFormatFiles = (logName + '%(asctime)s - %(funcName)s - %(message)s')
logFormatConsole = (logName + '%(asctime)s - %(funcName)s - %(message)s')
filelogformatter = logging.Formatter(logFormatFiles)
consolelogformatter = logging.Formatter(logFormatConsole)
fileLogger = logging.FileHandler(sessionLogFilename)
fileLogger.setLevel(logging.INFO)
fileLogger.setFormatter(filelogformatter)
consoleLogger = logging.StreamHandler(stdout)
consoleLogger.setLevel(logging.DEBUG)
consoleLogger.setFormatter(consolelogformatter)
remoteLoggerIP = "127.0.0.1"
remoteLoggerPort = 5124
remoteLogger = logging.handlers.SocketHandler(remoteLoggerPort,remoteLoggerPort)
remoteLogger.setLevel(logging.INFO)
# logging.getLogger('').addHandler(remoteLogger)
sessionLog = logging.getLogger(__name__)
sessionLog.setLevel(logging.DEBUG)
sessionLog.addHandler(fileLogger)
sessionLog.addHandler(consoleLogger)

def debug(msg):
    sessionLog.debug(msg)
def info(msg):
    sessionLog.info(msg)
def warning(msg):
    sessionLog.warning(msg)
def error(msg):
    sessionLog.error(msg)