import zmq
from Clases import  *
from threading import Semaphore, Thread
import sqlite3



# conection.execute('''CREATE TABLE Ofertas
#                (ID text,IDemple text, titulo text, descripcion text, experiencia text, estudio text,
#                habilidades text, sector text)''')


port = "6000"
host = "25.86.45.96"
#Creamos el contexto 
context = zmq.Context()
DHT = {}
socketfilter = context.socket(zmq.REP)
socketfilter.bind("tcp://{}:{}".format(host,port))


#semaforo encargado para poder hacer uso de la lista de Ofertas enviadas por los Empleadores
semaforo = Semaphore(1)

valorHash = 0
class HiloAlamcenarenDHT(Thread):
    # este hilo se encarga de agregar cada oferta a 
    # una lista de ofertas
    def __init__(self,semaforo,oferta): #Constructor de la clase
         Thread.__init__(self)
         self.semaforo = semaforo
         self.oferta = oferta
    def alamcenarOfertas(self):
        
        conection = sqlite3.connect('dataBase.db')
        DHT[str(self.oferta.ID)] = self.oferta
        conection.execute("""INSERT INTO Ofertas VALUES (
            {},{},{},{},{},{},{},{})""".format(self.oferta.ID, self.oferta.idEmple,self.oferta.titulo,
            self.oferta.descripcion,self.oferta.experiencia,self.oferta.estudio,self.oferta.habilidades,self.oferta.sector))
    def run(self): #Metodo que se ejecutara con la llamada start
          self.semaforo.acquire()
          self.alamcenarOfertas()
          self.semaforo.release()
    
def insertarOfertas():
    while True:
        obj = socketfilter.recv_pyobj()
        print(valorHash)
        obj.ID = valorHash
        socketfilter.send_string("Check")
        HiloAlamcenarenDHT(semaforo,obj).start()
        valorHash += 1
        pass

hiloFiltro = Thread(target=insertarOfertas)
hiloFiltro.start()