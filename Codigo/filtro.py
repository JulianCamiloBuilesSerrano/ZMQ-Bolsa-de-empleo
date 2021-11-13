import zmq
import  threading
from threading import Semaphore, Thread
import time
from Clases import  Oferta

portEmp = "5000"
portServ = "6000"
host = "25.86.45.96" 
host2 = "25.8.248.34"   #Filtro suscrito

context = zmq.Context()
socketSub =  context.socket(zmq.SUB)
socketServer =  context.socket(zmq.REQ)

socketServer.connect("tcp://{}:{}".format(host,portServ))

socketSub.connect("tcp://{}:{}".format(host2,portEmp))

#semafor encargado para poder hacer uso de la lista de Ofertas enviadas por los Empleadores
semaforo = Semaphore(1)

socketSub.subscribe("")
listOfertas = []

    
class HiloEmpleador(Thread):
    # este hilo se encarga de agregar cada oferta a 
    # una lista de ofertas
    def __init__(self,semaforo,Oferta): #Constructor de la clase
         Thread.__init__(self)
         self.semaforo = semaforo
         self.Oferta = Oferta
    def alamcenarOfertas(self):
        listOfertas.append(self.Oferta)
    def run(self): #Metodo que se ejecutara con la llamada start
          self.semaforo.acquire()
          self.alamcenarOfertas()
          self.semaforo.release()
    
class HiloServidorEnviar(Thread):
    # este hilo se encarga de verificar si hay la cantidad de ofertas 
    # para ser enviadas al servidor
    def __init__(self,semaforo): #Constructor de la clase
         Thread.__init__(self)
         self.semaforo = semaforo

    def enviarOFertas(self):
        if len(listOfertas) >= 2:
            for i in listOfertas:
                print("Oferta : ")
                print(i)
                socketServer.send_pyobj(i)
                print(socketServer.recv_string())
            
    def run(self): #Metodo que se ejecutara con la llamada start
          self.semaforo.acquire()
          self.enviarOFertas()
          self.semaforo.release()

def recibirOferta():
    while True:
        print("esperando Oferta")
        ofer = socketSub.recv_pyobj()
        print("pasa oferta")
        HiloEmpleador(semaforo,ofer).start()
        HiloServidorEnviar(semaforo).start()
    #end while
#end def

def hola():
    while True:
        print("hola")
        time.sleep(2)

hiloOfertas =  Thread(target=recibirOferta)

hiloHola = Thread(target=hola)

hiloOfertas.start()
#hiloHola.start()


# HiloEmpleador(semaforo,"x").start()
# HiloEmpleador(semaforo,"x").start()