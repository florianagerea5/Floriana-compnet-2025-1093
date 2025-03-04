import socket  # Importă modulul socket pentru comunicarea prin rețea
import sys     # Importă sys pentru a prelua argumentele din linia de comandă

def main():
    # Verifică dacă utilizatorul a furnizat numărul de port ca argument
    if len(sys.argv) < 2:
        print('Utilizare: python simple-udp-server.py <PORT>')
        sys.exit(1)  # Termină execuția programului dacă nu sunt suficienți parametri

    # Preia numărul portului din argumentele liniei de comandă și îl convertește în întreg
    PORT = int(sys.argv[1])

    # Creează un socket UDP (SOCK_DGRAM) pe IPv4 (AF_INET)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        # Asociază socket-ul la toate interfețele de rețea și la portul specificat
        server.bind(('', PORT))
        print(f"✅ Serverul UDP rulează pe portul {PORT} și așteaptă mesaje...")

        while True:
            # Așteaptă să primească un mesaj (maxim 1024 bytes)
            data, address = server.recvfrom(1024)
            message = data.decode().strip()  # Decodifică și elimină spațiile inutile

            # Loghează mesajul în terminal
            print(f"📩 Primit de la {address}: {message}")

            # Salvează mesajul într-un fișier de log
            with open("log.txt", "a") as log_file:
                log_file.write(f"{address}: {message}\n")

            # Dacă mesajul este "exit", serverul se închide
            if message.lower() == "exit":
                print("🚪 Serverul se închide...")
                break  # Iese din buclă și termină execuția

            # Convertește mesajul la majuscule
            response = message.upper()

            # Trimite înapoi mesajul transformat
            server.sendto(response.encode(), address)
            print(f"📤 Trimis către {address}: {response}")

    print("🛑 Serverul a fost oprit.")

# Asigură-te că scriptul rulează ca un program principal
if __name__ == '__main__':
    main()
