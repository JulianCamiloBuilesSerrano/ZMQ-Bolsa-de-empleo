from ctypes import resize
from os import write
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
    def __init__(self,ip,puerto,semaforo): #Constructor de la clase
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
        # with open('Ofertas.pkl','wb') as output:
        #     pickle.dump(self.oferta,output,pickle.HIGHEST_PROTOCOL)
        print(self.oferta)
        f = open("bd.txt","a")
        #f.write(self.oferta.ip)
        f.write(self.oferta.titulo)
        f.write(self.oferta.descripcion)
        f.write(self.oferta.experiencia)
        f.write(self.oferta.estudio)
        f.write(self.oferta.habilidades)
        f.close()
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
        socketfilter.send_string("Check, objeto en el servidor " +hostPincipal)
        print("llega objeto del filtro")
        HiloAlamcenarenDHT(semaforo,obj).start()
def actualizacionDHT():
    while True:
        p = socketActulizacion.recv_pyobj()
        socketActulizacion.send_string("listo")
        semaforo.acquire()
        DHT = p 
        f = open("bd.txt","w")
        for i in p:
            object = p[i]
            f.write(object.titulo)
            f.write(object.descripcion)
            f.write(object.experiencia)
            f.write(object.estudio)
            f.write(object.habilidades)
        f.close()
        semaforo.release()
        print(p)

def informarEstado():
    socketEstado = context.socket(zmq.REP)
    socketEstado.bind("tcp://{}:{}".format(hostPincipal,"2000"))
    while True:
        res = socketEstado.recv_string()
        if res == "activo?":
            socketEstado.send_string(hostPincipal)
        else:
            socketEstado.send_string("invalido")
def enviarOfertas():
    socketEn = context.socket(zmq.REP)
    socketEn.bind("tcp://{}:{}".format(hostPincipal,"3000"))
    while True:
        res = socketEn.recv_string()
        print("llega")
        if  res == "ofertas":
            semaforo.acquire()
            socketEn.send_pyobj(DHT)
            semaforo.release()

hiloFiltro = Thread(target=insertarOfertas)
hiloFiltro.start()
hiloActualizar = Thread(target=actualizacionDHT)
hiloActualizar.start()
hiloEstado = Thread(target=informarEstado)
hiloEstado.start()
hiloEnviar = Thread(target=enviarOfertas)
hiloEnviar.start()