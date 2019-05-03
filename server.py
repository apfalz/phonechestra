import asyncio
import websockets
import socket as so

#==========functions==========#

ip           = '127.0.0.1'
port         = 7400
sock         = so.socket(so.AF_INET, so.SOCK_DGRAM)


def pad_word(word):
  num_to_add = 4 - (len(word)%4)
  return word+'\0'*num_to_add

def pad_words(raw):
  words  = raw.split()
  return [pad_word(word) for word in words]

def format_message(raw, address='/0'):
  output = ''
  parts  = [pad_word(address)]
  words  = pad_words(raw)
  data   = ','+'s'*len(words)
  parts.append(pad_word(data))
  for word in words:
    parts.append(word)
  for part in parts:
    output += part
  return output.encode()

async def receive_from_client(websocket, path):
    done = False
    while not done:
        data = await websocket.recv()
        print(data)
        await websocket.send("Response!")
        print('after message')
        if data == 'stop':
            print('received stop message')
            done = True
            break
        data = format_message(data)
        sock.sendto(data, (ip, port))
    print('done')




if __name__ == '__main__':
    start_server = websockets.serve(receive_from_client, '10.10.104.15', 8765)


    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    quit()
