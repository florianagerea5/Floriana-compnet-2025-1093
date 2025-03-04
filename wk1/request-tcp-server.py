import socketserver  # Importăm modulul socketserver pentru a crea un server TCP

# Definim o clasă care va gestiona conexiunile clienților
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    Aceasta este clasa responsabilă pentru gestionarea conexiunilor clienților.
    Ea va fi instanțiată pentru fiecare client care se conectează la server.
    """

    def handle(self):
        """
        Metoda handle() este executată automat pentru fiecare client conectat.
        Se ocupă de primirea și procesarea mesajului trimis de client.
        """

        buffer = []  # Creăm o listă pentru a stoca caracterele primite

        # Citim caracter cu caracter până când clientul trimite ENTER ("\n")
        while True:
            char = self.request.recv(1).decode()  # Primim un caracter și îl decodăm din bytes în string
            if char == "\n":  # Dacă întâlnim caracterul ENTER, oprim citirea
                break
            buffer.append(char)  # Adăugăm caracterul în buffer

        # Transformăm lista de caractere într-un string și eliminăm spațiile goale
        message = "".join(buffer).strip()

        # Afișăm mesajul primit și adresa IP a clientului
        print("{} wrote: {}".format(self.client_address[0], message))

        # Convertim mesajul în majuscule și îl trimitem înapoi la client
        self.request.sendall(message.upper().encode())


# Definim o clasă pentru serverul TCP
class MyTCPServer(socketserver.TCPServer):
    """
    Această clasă extinde `socketserver.TCPServer` și ne permite să setăm
    anumite opțiuni pentru server.
    """
    allow_reuse_address = True  # Permitem reutilizarea rapidă a portului după închiderea serverului


# Dacă acest script este rulat direct, inițializăm serverul
if __name__ == "__main__":
    HOST, PORT = "localhost", 12345  # Specificăm adresa și portul pe care ascultă serverul

    # Creăm serverul și îl pornim
    with MyTCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"Server listening on {HOST}:{PORT}")  # Afișăm un mesaj de confirmare
        server.serve_forever()  # Serverul rulează continuu, așteptând conexiuni
