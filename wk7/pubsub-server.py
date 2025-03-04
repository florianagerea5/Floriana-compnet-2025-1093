import socket
import threading
from transfer_units import Request, Response
from serde import req_deserialize, res_serialize

PORT = 3333

SECRET = 'supersecret'

class TopicList:
  def __init__(self):
    self.clients = []
    self.topics = {}
    self.lock = threading.Lock()
  def add_client(self, client):
    with self.lock:
      self.clients.append(client)
  def remove_client(self, client):
    with self.lock:
      self.clients.remove(client)
      for topic, clients in self.topics:
        clients.remove(client)
  def subscribe(self, topic, client):
    with self.lock:
      self.topics.setdefault(topic, [])
      self.topics[topic].append(client)
  def unsubscribe(self, topic, client):
    with self.lock:
      self.topics[topic].remove(client)
  def publish(self, topic, data, client, response):
    for c in self.topics[topic]:
      if c != client:
        handle_client_write(c, Response(11, data))
  def has_topic(self, topic):
    return topic in self.topics

global_state = TopicList()

class StateMachine:
  def __init__(self, client, global_state):
    # non state machine specific
    self.client = client
    self.global_state = global_state
    # state machine specific
    self.start_state = None
    self.end_states = []
    self.current_state = None
    self.transitions = {}
  
  def set_start(self, name):
    self.start_state = name
    self.current_state = name
  
  def add_transition(self, state_name, command, transition, end_state = False):
    self.transitions.setdefault(state_name, {})
    self.transitions[state_name][command] = transition
    if end_state:
      self.end_states.append(state_name)

  def process_command(self, unpacked_request):
    if unpacked_request.type in self.transitions[self.current_state]:
      handler = self.transitions[self.current_state][unpacked_request.type]
      if not handler:
        Response(-4, f'cannot transition from {self.current_state} to {unpacked_request.type}')
      else:
        (new_state, response) = handler(unpacked_request, self.global_state, self.client)
        self.current_state = new_state
        return response
    else:
      return Response(-4, f'cannot transition from {self.current_state} to {unpacked_request.type}')

class TopicProtocol(StateMachine):
  def __init__(self, client, global_state):
    super().__init__(client, global_state)
    self.set_start('start')
    self.add_transition('start', 'connect', request_connect)
    self.add_transition('auth', 'disconnect', request_disconnect)
    self.add_transition('auth', 'subscribe', request_subscribe)
    self.add_transition('auth', 'unsubscribe', request_unsubscribe)
    self.add_transition('auth', 'publish', request_publish)

def request_connect(request, global_state, client):
  if request.params and len(request.params) > 0:
    if request.params[0] == SECRET:
      return ('auth', Response(0, 'you are in'))
    else:
      return ('start', Response(-2, 'you do not know the secret'))
  else:
    return ('start', Response(-1, 'not enough params'))

def request_disconnect(request, global_state, client):
  return ('start', Response(1, 'you are out'))

def request_subscribe(request, global_state, client):
  if request.params and len(request.params):
    global_state.subscribe(request.params[0], client)
    return ('auth', Response(2, f'you are now subscribed to {request.params[0]}'))
  else:
    return ('start', Response(-1, 'not enough params'))

def request_unsubscribe(request, global_state, client):
  if request.params and len(request.params):
    global_state.unsubscribe(request.params[0], client)
    return ('auth', Response(3, f'you are now unsubscribed from {request.params[0]}'))
  else:
    return ('start', Response(-1, 'not enough params'))

def request_publish(request, global_state, client):
  if request.params and len(request.params) > 1:
    topic = request.params[0]
    data = ' '.join(request.params[1:])
    if global_state.has_topic(topic):
      global_state.publish(topic, data, client, Response(4, f'message published to topic {topic}'))
      return  ('auth', Response(4, f'message published to topic {topic}'))
    else:
      return ('auth', Response(-3, f'topic {topic} does not exist'))
  else:
    return ('start', Response(-1, 'not enough params'))

def handle_client_write(client, response):
  client.sendall(res_serialize(response))

def handle_client_read(client):
  try:
    protocol = TopicProtocol(client, global_state)
    while True:
      if client == None:
        global_state.remove_client(client)
        break
      data = client.recv(1024)
      if not data:
        global_state.remove_client(client)
        break
      unpacked_request = req_deserialize(data)
      response = protocol.process_command(unpacked_request)
      handle_client_write(client, response)
  except OSError as e:
    global_state.remove_client(client)

def accept(server):
  while True:
    client, addr = server.accept()
    global_state.add_client(client)
    print(f'client {addr} has connected')
    client_read_thread = threading.Thread(target=handle_client_read, args=(client, ))
    client_read_thread.start()

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', PORT))
    server.listen()
    accept_thread =threading.Thread(target=accept, args=(server, ))
    accept_thread.start()
    accept_thread.join()

if __name__  == '__main__':
  main()