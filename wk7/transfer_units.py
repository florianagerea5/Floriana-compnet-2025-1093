class Request:
  def __init__(self, type, params):
    self.type = type
    self.params = params

class Response:
  def __init__(self, status, payload):
    self.status = status
    self.payload = payload
