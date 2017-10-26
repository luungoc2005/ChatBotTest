import socket
import subprocess
import os
import psutil
import sys
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def stanford_server_running():
    for pid in psutil.pids():
        try:
            process = psutil.Process(pid)
            if 'java' in process.name():
                args = process.cmdline()
                if ('edu.stanford.nlp.ie.NERServer' in args) and ('9199' in args):
                    print("Process name: %s - args: %s" % (process.name(), args))
                    return True
        except:
            pass
            # print("Unexpected error:", sys.exc_info()[0])
    return False

def load_stanford_tagger():
    if not stanford_server_running():
        CLASSIFIER_FILE = 'english.muc.7class.distsim.crf.ser.gz'
        process = subprocess.Popen([
            'java',
            '-mx400m',
            '-cp',
            'stanford-ner.jar',
            'edu.stanford.nlp.ie.NERServer',
            '-port',
            '9199',
            '-loadClassifier',
            'classifiers/' + CLASSIFIER_FILE
        ], \
        cwd=os.path.join(BASE_DIR, 'stanford-ner-2017-06-09/'), \
        stdout=subprocess.PIPE)
        # '-tokenizerFactory',
        # 'edu.stanford.nlp.process.WhitespaceTokenizer',
        # '-tokenizerOptions',
        # 'tokenizeNLs=false'
        print('Stanford server started with PID %s' % process.pid)

        # The stanford process will print out something like this line
        # Loading classifier from classifiers/english.muc.7class.distsim.crf.ser.gz ... done [23.4 sec].
        # Wait for that line to continue execution to avoid connection refused errors
        for line in iter(process.stdout.readline, ''):
            print(line)
            if CLASSIFIER_FILE in line:
                return

@contextmanager
def tcpip4_socket(host, port):
    """Open a TCP/IP4 socket to designated host/port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        yield s
    finally:
        try:
            s.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        except OSError:
            pass
        finally:
            s.close()


class SocketNER():
    """Stanford NER over simple TCP/IP socket."""

    def __init__(self, host='localhost', port=1234):
        self.host = host
        self.port = port

    def tag_text(self, text):
        """Tag the text with proper named entities token-by-token.
        :param text: raw text string to tag
        :returns: tagged text in given output format
        """
        for s in ('\f', '\n', '\r', '\t', '\v'):  # strip whitespaces
            text = text.replace(s, '')
        text += '\n'  # ensure end-of-line
        with tcpip4_socket(self.host, self.port) as s:
            if not isinstance(text, bytes):
                text = text.encode('utf-8')
            s.sendall(text)
            tagged_text = s.recv(10 * len(text))
        return tagged_text.decode('utf-8')
