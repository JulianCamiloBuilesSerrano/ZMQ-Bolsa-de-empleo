import zmq
from Clases import Oferta
from threading import Semaphore, Thread
#puerto de escucha de solicitudes
puerto = "1000"
context = zmq.Context()
socketFilro = context.socket(zmq.SUB)
socketFilro.connect("tcp://25.8.248.34:{}".format(puerto))
listaOfertas = set()

class HiloFiltroSub(Thread):
    # este hilo se encarga de estar escuchando algun filtro
    # una lista de ofertas
    def __init__(self,ip,puerto): #Constructor de la clase
         Thread.__init__(self)
         self.ip = ip
         self.puerto = puerto

    def run(self): #Metodo que se ejecutara con la llamada start
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://"+self.ip+":"+self.puerto)
    
       
