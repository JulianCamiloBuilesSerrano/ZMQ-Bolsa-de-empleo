import zmq
from Clases import Oferta
from threading import Semaphore, Thread
import  time
#puerto de escucha de solicitudes

hostPincipal = str(input("Indique la ip: "))
filtro1 = str(input("indique sector 1: "))
filtro2 = str(input("indique sector 2: "))
puerto = "1000"
context = zmq.Context()
socketFilro = context.socket(zmq.SUB)
socketFilro.connect("tcp://25.8.248.34:{}".format(puerto))
listaOfertas = []
semaforo = Semaphore(1)
class HiloFiltroSub(Thread):
    # este hilo se encarga de estar escuchando algun filtro
    # una lista de ofertas
    def __init__(self,ip,puerto): #Constructor de la clase
         Thread.__init__(self)
         self.ip = ip
         self.puerto = puerto

    def listarOfertas(slef,listaOfertas):
        print("---------------Nuevas ofertas--------------")
        for i in listaOfertas:
            if listaOfertas[i].getSector() ==filtro1:
                print(listaOfertas[i].titulo)
                print(listaOfertas[i].descripcion)
                print(listaOfertas[i].experiencia)
                print(listaOfertas[i].estudio)
                print(listaOfertas[i].habilidades)
            elif listaOfertas[i].getSector ==filtro2:
                print(listaOfertas[i].titulo)
                print(listaOfertas[i].descripcion)
                print(listaOfertas[i].experiencia)
                print(listaOfertas[i].estudio)
                print(listaOfertas[i].habilidades)
        print("------------------------------------------")
    def run(self): #Metodo que se ejecutara con la llamada start
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://"+self.ip+":"+self.puerto)
        socket.subscribe("")
        while True:
            time.sleep(1)
            ob = socket.recv_pyobj()
            semaforo.acquire()
            listaOfertas= ob
            print(ob)
            self.listarOfertas(ob)
            semaforo.release()
        
HiloFiltroSub("25.86.45.96","1000").start()
HiloFiltroSub("25.8.248.34","1000").start()
HiloFiltroSub("25.5.97.125","1000").start()
     
 

       
