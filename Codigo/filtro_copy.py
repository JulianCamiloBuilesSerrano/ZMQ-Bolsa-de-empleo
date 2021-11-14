import zmq
from threading import Semaphore, Thread
import time
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
                self.guardarOferta(i,)
                if self.socketServer.send_pyobj(i,"25.8.248.34"):
                    continue
                elif self.socketServer.send_pyobj(i,"25.86.45.96"):
                    continue
                elif self.socketServer.send_pyobj(i,"25.5.97.125"):
                    continue
                else:
                    print("No hay servidores disponibles")
                    break
    def guardarOferta(self, oferta,ip):
        self.socketServer.connect("tcp://"+ip+":6000")
        self.socketServer.send_pyobj(oferta)
        k = 0
        end = False
        while not end and k < 10:
            if self.socketServer.poll(3000) and zmq.POLLIN:
                        res = self.socketServer.recv_string()
                        print(res)
                        end = True
            k = k + 1
        return end
            
        
    def run(self): #Metodo que se ejecutara con la llamada start
        self.socketServer =  context.socket(zmq.REQ)
        self.socketServer.connect("tcp://25.86.45.96:6000")
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
            ob.setSector("ingenieria")
        elif "medico"in ob.descripcion or "medicina"in ob.estudio:
            ob.setSector("salud")
        elif "enfermera"in ob.descripcion or "enfermeria"in ob.estudio:
            ob.setSector("salud")
        elif "instrumento"in ob.descripcion or "musica"in ob.estudio:
            ob.setSector("Musica")
        elif "banda"in ob.descripcion or "conciertos"in ob.descripcion:
            ob.setSector("salud")
        elif "politica"in ob.descripcion or "derecho"in ob.estudio:
            ob.setSector("Politica")
        elif "civil"in ob.descripcion or "senado"in ob.descripcion:
            ob.setSector("Politica")
        elif "diseño"in ob.descripcion or "diseñar"in ob.descripcion:
            ob.setSector("Arquitectura y diseño")
        elif "dibujar"in ob.descripcion or "planos"in ob.descripcion:
            ob.setSector("Arquitectura y diseño")
        elif "diseño"in ob.estudio or "arquitectura"in ob.estudio:
            ob.setSector("Arquitectura y diseño")
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
            
HiloObtenerOfertas("25.86.45.96","5000",semaforo).start()
HiloObtenerOfertas("25.8.248.34","5000",semaforo).start()
HiloObtenerOfertas("25.5.97.125","5000",semaforo).start()



