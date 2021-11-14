from ctypes import resize
import zmq
from Clases import  *
from threading import Semaphore, Thread
import sqlite3
import pickle


#--------------------------
#leer la ip de donse se esta iniciando el proceso 
#--------------------------
hostPincipal = str(input("Indique la ip: "))

port = "6000"
portActualizacion = "7000"
#Creamos el contexto 
context = zmq.Context()
DHT = {}
socketfilter = context.socket(zmq.REP)
socketfilter.bind("tcp://{}:{}".format(hostPincipal,port))
socketActulizacion = context.socket(zmq.REP) 
socketActulizacion.bind("tcp://{}:{}".format(hostPincipal,portActualizacion))
#semaforo encargado para poder hacer uso de la lista de Ofertas enviadas por los Empleadores
semaforo = Semaphore(1)

valorHash = 0
class DHTCompartir(Thread):
    def __init__(self,ip,puerto): #Constructor de la clase
         Thread.__init__(self)
         self.ip = ip
         self.puerto = puerto
         self.semaforo  = semaforo
    def run(self):
        socket =  context.socket(zmq.REQ)
        conexion = "tcp://"+self.ip+":"+self.puerto
        socket.connect(conexion)
        socket.send_pyobj(DHT)
        respuesta = socket.recv_string()
        print(respuesta)
class HiloAlamcenarenDHT(Thread):
    # este hilo se encarga de agregar cada oferta a 
    # una lista de ofertas
    def __init__(self,semaforo,oferta): #Constructor de la clase
         Thread.__init__(self)
         self.semaforo = semaforo
         self.oferta = oferta
    def alamcenarOfertas(self):
        n = len(DHT)
        ID = n+1
        DHT[str(n)] = self.oferta
        with open('Ofertas.pkl','wb') as output:
            pickle.dump(self.oferta,output,pickle.HIGHEST_PROTOCOL)
    def run(self): #Metodo que se ejecutara con la llamada start
        self.semaforo.acquire()
        self.alamcenarOfertas()
        self.semaforo.release()
        if hostPincipal == "25.86.45.96":
            DHTCompartir("25.8.248.34","7000",self.semaforo).start()
            DHTCompartir("25.5.97.125","7000",self.semaforo).start()
        elif hostPincipal == "25.8.248.34":
            DHTCompartir("25.8.248.34","7000",self.semaforo).start()
            DHTCompartir("25.86.45.96","7000",self.semaforo).start()
        else:
            DHTCompartir("25.8.248.34","7000",self.semaforo).start()
            DHTCompartir("25.8.248.34","7000",self.semaforo).start()
              
    
def insertarOfertas():
    while True:
        obj = socketfilter.recv_pyobj()
        print("llega objeto del filtro")
        socketfilter.send_string("Check, objeto en el servidor")
        HiloAlamcenarenDHT(semaforo,obj).start()
def actualizacionDHT():
    while True:
        p = socketActulizacion.recv_pyobj()
        print(p)
        #fataria actualizar el archivo bd

hiloFiltro = Thread(target=insertarOfertas)
hiloFiltro.start()
