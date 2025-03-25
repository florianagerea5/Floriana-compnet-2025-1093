# Importăm modulele necesare
import socket  # pentru comunicarea prin rețea
import sys     # pentru accesarea argumentelor din linia de comandă

# Importăm clasele și funcțiile definite în alte fișiere/module
from transfer_units import RequestMessage, ResponseMessage, RequestMessageType, ResponseMessageType
from serde import serialize, deserialize  # pentru serializarea și deserializarea mesajelor

def main():
    # Verificăm dacă au fost furnizate argumentele necesare (host și port)
    if len(sys.argv) < 3:
        print('Usage: python client.py <HOST> <PORT>')
        return  # dacă nu sunt suficiente argumente, ieșim

    # Extragem host-ul (adresa IP sau hostname) și portul din argumente
    HOST, PORT = sys.argv[1:3]
    PORT = int(PORT)  # convertim portul din string în int
    print(f'Conectare la serverul {HOST}:{PORT}...')

    # Creăm un socket UDP și îl folosim într-un context manager
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Buclă principală: așteptăm comenzi de la utilizator
        while True:
            # Solicităm utilizatorului să introducă o comandă
            data = input('storage -> ')

            # Împărțim linia introdusă în două părți: comanda și restul (dacă există)
            items = data.strip().split(' ', 1)
            command = items[0]  # prima parte este comanda (ex: connect, send)

            # === 1. CONNECT ===
            if command == 'connect':
                # Trimitem un mesaj de conectare către server
                client_socket.sendto(serialize(RequestMessage(RequestMessageType.CONNECT)), (HOST, PORT))

            # === 2. LIST ===
            elif command == 'list':
                # Cerem serverului lista notelor stocate
                client_socket.sendto(serialize(RequestMessage(RequestMessageType.LIST)), (HOST, PORT))

            # === 3. SEND <mesaj> ===
            elif command == 'send':
                # Verificăm dacă există un mesaj după cuvântul "send"
                if len(items) > 1:
                    payload = items[1]  # extragem mesajul
                    # Trimitem nota către server
                    client_socket.sendto(serialize(RequestMessage(RequestMessageType.SEND, payload)), (HOST, PORT))
                else:
                    print('Trebuie să scrii ceva după comanda send (ex: send Salut!)')

            # === 4. DISCONNECT ===
            elif command == 'disconnect':
                # Informăm serverul că vrem să ne deconectăm
                client_socket.sendto(serialize(RequestMessage(RequestMessageType.DISCONNECT)), (HOST, PORT))

            # === Comandă necunoscută ===
            else:
                print('Comandă necunoscută. Comenzi valide: connect, list, send <mesaj>, disconnect')
                continue  # nu trimitem nimic către server dacă comanda nu e validă

            # Așteptăm răspunsul de la server
            message, _ = client_socket.recvfrom(1024)

            # Deserializăm răspunsul și îl afișăm
            response = deserialize(message)
            print(response)

# Verificăm dacă fișierul este rulat direct (nu importat)
if __name__ == '__main__':
    main()
