# Definește tipurile și structura mesajelor

# Importăm clasa de bază Enum pentru a crea tipuri simbolice (enumerări)
from enum import Enum

# === Tipuri de mesaje pe care le poate trimite clientul către server ===
class RequestMessageType(Enum):
    CONNECT = 1     # Clientul vrea să se conecteze
    SEND = 2        # Clientul trimite o notă
    LIST = 3        # Clientul cere lista notelor
    DISCONNECT = 4  # Clientul vrea să se deconecteze

# === Tipuri de mesaje pe care serverul le poate trimite înapoi clientului ===
class ResponseMessageType(Enum):
    OK = 1              # Operația a fost efectuată cu succes
    ERR_CONNECTED = 2   # Eroare: clientul nu este conectat (dar încearcă să trimită/list)

# === Clasa pentru mesajele trimise de client ===
class RequestMessage:
    def __init__(self, message_type, payload=''):
        # message_type este un element din RequestMessageType (ex: CONNECT, SEND)
        self.message_type = message_type

        # payload este conținutul mesajului (ex: textul notei) – poate fi gol
        self.payload = payload

    # Reprezentarea ca text a mesajului – utilă pentru debugging / print
    def __str__(self):
        return f'''
------------REQUEST------------
TYPE: {self.message_type}
{self.payload}
-------------------------------
        '''

# === Clasa pentru mesajele trimise de server ===
class ResponseMessage:
    def __init__(self, message_type, payload=''):
        # message_type este un element din ResponseMessageType (ex: OK, ERR_CONNECTED)
        self.message_type = message_type

        # payload poate fi folosit pentru a transmite date (ex: lista de note)
        self.payload = payload

    # Reprezentarea ca text a mesajului – utilă pentru print/debug
    def __str__(self):
        return f'''
------------RESPONSE------------
TYPE: {self.message_type}
{self.payload}
-------------------------------
        '''
