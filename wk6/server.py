# === Importăm modulele necesare ===
import socket  # pentru lucrul cu socket-uri (UDP networking)
import sys     # pentru a accesa argumentele din linia de comandă

# Importăm clasele definite în fișierele proprii
from transfer_units import (
    RequestMessage,
    ResponseMessage,
    RequestMessageType,
    ResponseMessageType
)

from state import State                         # pentru a gestiona conexiunile și notele clienților
from serde import serialize, deserialize        # pentru transformarea obiectelor în bytes și invers

# Inițializăm o instanță a stării serverului (reține conexiuni și note)
state = State()


def main():
    # Verificăm dacă a fost transmis un argument (portul)
    if len(sys.argv) < 2:
        print('❌ Usage: python server.py <PORT>')
        return

    # Obținem portul de ascultare din linia de comandă
    PORT = int(sys.argv[1])

    # Creăm un socket UDP și îl legăm de port
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(('', PORT))
        print(f'✅ Serverul rulează pe portul {PORT} și așteaptă conexiuni...')

        # Buclă infinită: ascultăm continuu mesaje de la clienți
        while True:
            # Așteptăm un mesaj de până la 1024 de bytes
            message, address = server_socket.recvfrom(1024)

            # Deserializăm mesajul primit (convertim din bytes în obiect)
            request = deserialize(message)

            # === 1. CONNECT ===
            if request.message_type == RequestMessageType.CONNECT:
                state.add_connection(address)
                print(f'🔌 Client conectat: {address}')
                server_socket.sendto(serialize(ResponseMessage(ResponseMessageType.OK)), address)

            # === 2. SEND ===
            elif request.message_type == RequestMessageType.SEND:
                if address in state.connections:
                    state.add_note(address, request.payload)
                    print(f'📝 Notă primită de la {address}: {request.payload}')
                    server_socket.sendto(serialize(ResponseMessage(ResponseMessageType.OK)), address)
                else:
                    print(f'⚠️ Client neconectat a încercat să trimită: {address}')
                    server_socket.sendto(serialize(ResponseMessage(ResponseMessageType.ERR_CONNECTED)), address)

            # === 3. LIST ===
            elif request.message_type == RequestMessageType.LIST:
                if address in state.connections:
                    notes = state.get_notes(address)
                    print(f'📥 {address} a cerut lista notelor')
                    server_socket.sendto(serialize(ResponseMessage(ResponseMessageType.OK, notes)), address)
                else:
                    print(f'⚠️ Client neconectat a cerut lista: {address}')
                    server_socket.sendto(serialize(ResponseMessage(ResponseMessageType.ERR_CONNECTED)), address)

            # === 4. DISCONNECT ===
            elif request.message_type == RequestMessageType.DISCONNECT:
                state.remove_connection(address)
                print(f'❌ Client deconectat: {address}')
                server_socket.sendto(serialize(ResponseMessage(ResponseMessageType.OK)), address)

            # === Alt tip necunoscut ===
            else:
                print(f'❓ Mesaj necunoscut primit de la {address}')


# Dacă rulăm direct fișierul (nu îl importăm), pornește funcția main
if __name__ == '__main__':
    main()
