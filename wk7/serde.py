from transfer_units import Request, Response

def res_serialize(response):
  return bytes(str(response.status) + ' ' + response.payload, encoding='utf-8')

def req_deserialize(request):
  items = request.decode('utf-8').strip().split(' ')
  if len(items) > 1:
    return Request(items[0], items[1:])
  return Request(items[0], None)