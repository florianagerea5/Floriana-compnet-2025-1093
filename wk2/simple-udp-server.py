import socket
import sys
from datetime import datetime  # Importă modulul datetime pentru ora exactă

def main():
    # Verifică dacă utilizatorul a furnizat argumentele necesare (PORT)
    if len(sys.argv) < 2:
        print('Utilizare: python simple-udp-server.py <PORT>')
        sys.exit(1)  # Închide scriptul dacă nu sunt suficiente argumente

    # Preia portul din linia de comandă
    PORT = int(sys.argv[1])

    # Creează un socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # Asociază socket-ul la toate interfețele de rețea și portul specificat
        server_socket.bind(('', PORT))
        print(f"✅ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Serverul UDP rulează pe portul {PORT} și așteaptă mesaje...")

        while True:
            # Primește date de la un client
            message, address = server_socket.recvfrom(1024)
            message = message.decode().strip()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Afișează mesajul primit cu ora exactă
            print(f"📩 [{timestamp}] Primit de la {address}: {message}")

            # Salvează mesajul într-un fișier de log
            with open("server-log.txt", "a") as log_file:
                log_file.write(f"[{timestamp}] {address}: {message}\n")

            # Dacă mesajul este "exit", serverul se închide
            if message.lower() == "exit":
                print(f"🚪 [{timestamp}] Serverul UDP se închide...")
                server_socket.sendto("Serverul s-a închis.".encode(), address)
                break  # Oprește bucla și închide serverul

            # Transformă mesajul în majuscule și trimite-l înapoi
            response = message.upper()
            server_socket.sendto(response.encode(), address)

            # Afișează ora exactă la care a fost trimis răspunsul
            print(f"📤 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Trimis către {address}: {response}")

    print(f"🛑 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Serverul UDP a fost oprit.")

if __name__ == '__main__':
    main()
