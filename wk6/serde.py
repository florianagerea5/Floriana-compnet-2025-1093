# Serializare/deserializare mesaje

# Importăm modulele necesare
import pickle  # pentru serializarea obiectelor Python (transformare obiecte <-> bytes)
import io      # pentru manipularea unui "flux" de date (stream) în memorie, similar unui fișier

# === Funcția serialize ===
# Această funcție primește un obiect Python (ex: RequestMessage) și îl transformă în bytes.
# Este necesar pentru a putea trimite acel obiect prin rețea (sockets trimit doar bytes, nu obiecte).
def serialize(message):
    # Cream un stream (flux) de bytes în memorie
    stream = io.BytesIO()

    # Scriem (serializăm) obiectul în flux folosind pickle
    pickle.dump(message, stream)

    # Obținem conținutul fluxului: acesta este mesajul serializat (în bytes)
    serialized_message = stream.getvalue()

    # Returnăm rezultatul, care poate fi trimis printr-un socket
    return serialized_message


# === Funcția deserialize ===
# Această funcție primește o secvență de bytes (ex: venită de la server) și o transformă
# înapoi într-un obiect Python (ex: ResponseMessage).
def deserialize(message):
    # Cream un stream de citire pe baza secvenței de bytes primită
    stream = io.BytesIO(message)

    # Citim și reconstruim obiectul original din flux
    deserialized_message = pickle.load(stream)

    # Returnăm obiectul reconstruit
    return deserialized_message
