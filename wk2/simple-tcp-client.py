import socket  # Importă modulul socket pentru comunicarea în rețea

# Adresa și portul serverului la care clientul se va conecta
HOST, PORT = 'localhost', 3333

def main():
    # Creează un socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        # Se conectează la serverul specificat (HOST și PORT)
        client.connect((HOST, PORT))

        while True:
            # Solicită utilizatorului să introducă un mesaj
            data = input('Scrie "exit" pentru a ieși, altfel introduceți mesajul:\n')

            # Dacă utilizatorul scrie "exit", clientul se oprește
            if data.strip() == 'exit':
                break

            # Trimite mesajul către server (convertit în format bytes)
            client.sendall(data.encode('utf-8'))

            # Primește răspunsul de la server (maxim 1024 bytes)
            data = client.recv(1024)

            # Afișează răspunsul primit de la server
            print(data)

# Asigură că scriptul rulează ca un program principal
if __name__ == '__main__':
    main()
