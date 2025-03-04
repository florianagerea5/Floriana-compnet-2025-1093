import socket
import sys
from datetime import datetime  # Importă datetime pentru a obține ora exactă

def main():
    # Verifică dacă utilizatorul a furnizat argumentele necesare (IP și Port)
    if len(sys.argv) < 3:
        print('Utilizare: python simple-udp-client.py <IP_SERVER> <PORT>')
        sys.exit(1)  # Închide scriptul dacă nu sunt suficiente argumente

    # Preia argumentele din linia de comandă
    HOST, PORT = sys.argv[1], int(sys.argv[2])

    # Creează un socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            # Solicită utilizatorului un mesaj
            data = input('Introduceți mesajul ("exit" pentru a ieși):\n')

            # Permite utilizatorului să închidă clientul
            if data.lower().strip() == "exit":
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"🔴 [{timestamp}] Clientul UDP s-a închis.")
                client_socket.sendto(data.encode('utf-8'), (HOST, PORT))
                break  # Ieșim din buclă

            try:
                # Trimite mesajul către server
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                client_socket.sendto(data.encode('utf-8'), (HOST, PORT))

                # Afișează ora exactă când s-a trimis mesajul
                print(f"📨 [{timestamp}] Mesaj trimis către server: {data}")

                # Salvează mesajul trimis într-un fișier log
                with open("client-log.txt", "a") as log_file:
                    log_file.write(f"[{timestamp}] Trimis către {HOST}:{PORT}: {data}\n")

                # Setează un timeout pentru a evita blocarea clientului
                client_socket.settimeout(5)

                # Așteaptă răspunsul de la server
                message, address = client_socket.recvfrom(1024)
                response_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Afișează răspunsul primit de la server cu ora exactă
                print(f"📩 [{response_timestamp}] Răspuns de la server: {message.decode()}")

                # Salvează răspunsul primit în log
                with open("client-log.txt", "a") as log_file:
                    log_file.write(f"[{response_timestamp}] Răspuns de la server: {message.decode()}\n")

            except socket.timeout:
                print(f"⚠️ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Serverul nu a răspuns în timp util.")
            except Exception as e:
                print(f"⚠️ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Eroare: {e}")

if __name__ == '__main__':
    main()
