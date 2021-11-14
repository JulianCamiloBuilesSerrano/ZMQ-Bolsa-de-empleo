import zmq
from Clases import Oferta
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5000")
print("entra 1")
x = socket.recv_pyobj()
print("pasa")

def conectar():
    socket.connect("tcp://localhost:5000")
    
def main():
    conectar()
    while True:
        print("entra")
        x = socket.recv_pyobj()
        print("pasa")
        print(x)
main()
