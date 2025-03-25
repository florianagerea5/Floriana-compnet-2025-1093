# Gestionează conexiunile și notele

# === Clasa State ===
# Această clasă este responsabilă pentru a păstra:
# 1. Ce clienți sunt conectați
# 2. Ce mesaje (note) a trimis fiecare client

class State:
    # Constructorul clasei: este apelat automat când facem `state = State()`
    def __init__(self):
        # Inițializăm un dicționar gol care va reține adresele clienților conectați
        # Fiecare adresă (ex: ('127.0.0.1', 54321)) va fi mapată la o listă de note
        self.connections = {}

    # === Adaugă un client nou în dicționarul de conexiuni ===
    def add_connection(self, address):
        # Dacă adresa clientului nu există deja, o adăugăm cu o listă goală de note
        # Dacă există deja, nu facem nimic (setdefault face exact asta)
        self.connections.setdefault(address, [])

    # === Adaugă o notă pentru un client deja conectat ===
    def add_note(self, address, note):
        # Adaugă mesajul (nota) în lista asociată cu adresa clientului
        self.connections[address].append(note)

    # === Returnează toate notele unui client ca un șir de caractere (string) ===
    def get_notes(self, address):
        # Îmbinăm notele cu caracterul de "newline" (\n), ca să apară una pe fiecare rând
        return '\n'.join(self.connections[address])

    # === Șterge complet un client din dicționarul de conexiuni ===
    def remove_connection(self, address):
        # Eliminăm clientul din lista conexiunilor (și implicit îi pierdem notele)
        del self.connections[address]
