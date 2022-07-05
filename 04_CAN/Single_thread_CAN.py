from multiprocessing.connection import Listener
from socket import timeout
import can

can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'can0'
can.rc['bitrate'] = 250000
from can.interface import Bus

bus = Bus()
msg = can.Message(
        arbitration_id=0x123, data=[1, 2, 3, 4, 5, 6], is_extended_id=False
)

bus.send(msg)

from can import Message

test = Message(data=[1, 2, 3, 4, 5])
test.data
print(test)

while 1:
    for msg in bus:
        print(msg)
    

