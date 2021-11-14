import zmq
from threading import Semaphore, Thread
import time

from zmq.sugar import socket
from Clases import  Oferta

#--------------------------
#leer la ip de donse se esta iniciando el proceso 
#--------------------------
hostPincipal = str(input("Indique la ip: "))

portEmp = "5000"
portServ = "6000"
host = "25.86.45.96" 
host2 = "25.86.45.96"   #Filtro suscrito

context = zmq.Context()


#semafor encargado para poder hacer uso de la lista de Ofertas enviadas por los Empleadores
semaforo = Semaphore(1)


listOfertas= set()
#-----------------------------------------------------------------
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
#-----------------------------------------------------------------
class HiloServidorEnviar(Thread):
    # este hilo se encarga de verificar si hay la cantidad de ofertas 
    # para ser enviadas al servidor
    def __init__(self,semaforo): #Constructor de la clase
         Thread.__init__(self)
         self.semaforo = semaforo
    def enviarOFertas(self):
        if len(listOfertas) >= 3:
            for i in listOfertas:
                print("Oferta : ")
                print(i)
                if self.guardarOferta(i,"25.8.248.34"):
                    continue
                elif self.guardarOferta(i,"25.86.45.96"):
                    continue
                elif self.guardarOferta(i,"25.5.97.125"):
                    continue
                else:
                    print("No hay servidores disponibles")
                    break
            listOfertas.clear()
        
    def guardarOferta(self, oferta,ip):
        socketServer =  context.socket(zmq.REQ)

        print("ENTRA" + "tcp://"+ip+":6000")
        socketServer.connect("tcp://"+ip+":6000")
        socketServer.send_pyobj(oferta)
        k = 0
        end = False
        while not end and k < 10:
            if socketServer.poll(100) and zmq.POLLIN:
                        res = socketServer.recv_string()
                        print(res)
                        end = True
            k = k + 1
        socketServer.disconnect("tcp://"+ip+":6000")
        return end
            
        
    def run(self): #Metodo que se ejecutara con la llamada start
        #self.socketServer.connect("tcp://25.86.45.96:6000")
        self.semaforo.acquire()
        self.enviarOFertas()
        self.semaforo.release()
#-----------------------------------------------------------------
class HiloObtenerOfertas(Thread):
    # Este hilo se encarga de escuchar las tres posibles ips de empleadores
    def __init__(self,ip,puerto,semaforo): #Constructor de la clase
         Thread.__init__(self)
         self.ip = ip
         self.puerto = puerto
         self.semaforo  = semaforo
    def insetarClasificar(self,ob):
        if "ingenieria"in ob.descripcion or "ingenieria"in ob.estudio:
            ob.sector= "ingenieria"
        elif "medico"in ob.descripcion or "medicina"in ob.estudio:
            ob.sector= "salud"
        elif "enfermera"in ob.descripcion or "enfermeria"in ob.estudio:
            ob.sector= "salud"
        elif "instrumento"in ob.descripcion or "musica"in ob.estudio:
            ob.sector="musica"
        elif "banda"in ob.descripcion or "conciertos"in ob.descripcion:
            ob.sector="musica"
        elif "politica"in ob.descripcion or "derecho"in ob.estudio:
            ob.sector="politica"
        elif "civil"in ob.descripcion or "senado"in ob.descripcion:
            ob.sector="politica"
        elif "diseño"in ob.descripcion or "diseñar"in ob.descripcion:
            ob.sector= "arquitectura y diseño"
        elif "dibujar"in ob.descripcion or "planos"in ob.descripcion:
            ob.sector = "arquitectura y diseño"
        elif "diseño"in ob.estudio or "arquitectura"in ob.estudio:
            ob.sector ="arquitectura y diseño"
        print(ob)
        listOfertas.add(ob)
        print(listOfertas)
    def run(self): #Metodo que se ejecutara con la llamada start
        socket =  context.socket(zmq.SUB)
        conexion = "tcp://"+self.ip+":"+self.puerto
        socket.connect(conexion)
        print("se esatable la conexion: "+conexion)
        socket.subscribe("")
        while True:
            ob = socket.recv_pyobj()
            print("llega objeto")
            self.semaforo.acquire()
            self.insetarClasificar(ob)
            self.semaforo.release()
            HiloServidorEnviar(self.semaforo).start()
  
class EnviarOFerta(Thread):
    # este hilo se encarga de estar escuchando algun filtro
    # una lista de ofertas
    def __init__(self): #Constructor de la clase
            Thread.__init__(self)
    def servidorActivo(self,ip):
        socketS =  context.socket(zmq.REQ)
        socketS.connect("tcp://"+ip+":2000")
        socketS.send_string("activo?")
        k = 0
        res:str
        end = False
        while not end and k < 10:
            if socketS.poll(100) and zmq.POLLIN:
                        res = socketS.recv_string()
                        print(res)
                        return True
            k = k + 1
        return False
    def traerOfertasServidor(self,ip):
        socketS =  context.socket(zmq.REQ)
        socketS.connect("tcp://"+ip+":3000")
        socketS.send_string("ofertas")
        print("pasa")
        return socketS.recv_pyobj() 
        
    def run(self): 
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://{}:{}".format(hostPincipal,"1000"))
        while True:
            time.sleep(5)
            if self.servidorActivo("25.8.248.34"):
                ofertas = self.traerOfertasServidor("25.8.248.34")
                self.socket.send_pyobj(ofertas)
                continue
            elif self.servidorActivo("25.86.45.96"):
                ofertas = self.traerOfertasServidor("25.86.45.96")
                self.socket.send_pyobj(ofertas)
                
                continue
            elif self.servidorActivo("25.5.97.125"):
                ofertas = self.traerOfertasServidor("25.5.97.125")
                self.socket.send_pyobj(ofertas)
                continue
            else:
                print("No hay servidores disponibles")
            
                   
HiloObtenerOfertas("25.86.45.96","5000",semaforo).start()
HiloObtenerOfertas("25.8.248.34","5000",semaforo).start()
HiloObtenerOfertas("25.5.97.125","5000",semaforo).start()
EnviarOFerta().start()



