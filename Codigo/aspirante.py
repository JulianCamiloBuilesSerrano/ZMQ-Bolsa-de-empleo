from pickle import TRUE
import zmq
from zmq.sugar.poll import select
from Clases import Oferta
from threading import Semaphore, Thread
import  time
#puerto de escucha de solicitudes

hostPincipal = str(input("Indique la ip: "))

experiencia = str(input("Indique la experiencia de trabajo: "))
estudio = str(input("Indique los estudios separados por comas: "))
habilidades = str(input("Indique las habilidades separadas por comas: "))


filtro1 = str(input("indique sector 1: "))
filtro2 = str(input("indique sector 2: "))
puerto = "1000"
context = zmq.Context()
socketFilro = context.socket(zmq.SUB)
socketFilro.connect("tcp://25.8.248.34:{}".format(puerto))
listaOfertas = []
semaforo = Semaphore(1)
semaforo2 = Semaphore(1)
postulado = False
class HiloEnviarAceptacion(Thread):
    # este hilo se encarga de estar escuchando algun filtro
    # una lista de ofertas
    def __init__(self,ip,puerto,idOferta): #Constructor de la clase
         Thread.__init__(self)
         self.ip = ip
         self.puerto = puerto
         self.semaforo  = semaforo
         self.idOferta = idOferta
    
    def run(self): #Metodo que se ejecutara con la llamada start
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(self.ip,self.puerto))
        self.socket.send_string(self.idOferta)
        k = 0
        end = False
        while not end and k < 10:
            if self.socket.poll(100) and zmq.POLLIN:
                        res = self.socket.recv_string()
                        print("respuesta: ",end="")
                        print(res)
                        end = True
            k = k + 1
        

class HiloFiltroSub(Thread):
    # este hilo se encarga de estar escuchando algun filtro
    # una lista de ofertas
    def __init__(self,ip,puerto): #Constructor de la clase
         Thread.__init__(self)
         self.ip = ip
         self.puerto = puerto
    def validar(slef,oferta):
        validacion1 = False
        validacion2 = False
        validacion3 = False
        if int(oferta.experiencia) <= int(experiencia):
            
            validacion1 = True
        listaEstudios = oferta.estudio.split(",")
        for e in listaEstudios:
            estu = estudio.split(",")
            for es in estu:
                if e in es or es in e:
                    validacion2 = True
        listaHabilidades = oferta.habilidades.split(",")
        for h in listaHabilidades:
            habi = habilidades.split(",")
            for ha in habi:
                if ha in h or h in ha:
                    validacion3 = True
        return validacion1 and validacion2 and validacion3
    def validarFiltro(self,idoferta):
        socketAceptar = context.socket(zmq.REQ)
        HiloEnviarAceptacion("25.86.45.96","4000",idoferta).start()
        HiloEnviarAceptacion("25.8.248.34","4000",idoferta).start()
        HiloEnviarAceptacion("25.5.97.125","4000",idoferta).start()

    def listarOfertas(self,listaOfertas):
        print("---------------Nuevas ofertas--------------")
        pregunta = "0"
        for i in listaOfertas:
            if listaOfertas[i].getSector() ==filtro1:
                print("*******oferta "+i+"*******")
                print(listaOfertas[i].titulo,end="")
                print(listaOfertas[i].descripcion, end="")
                print(listaOfertas[i].experiencia, end="")
                print(listaOfertas[i].estudio, end="")
                print(listaOfertas[i].habilidades, end="")
                pregunta = str(input("acepta la oferta si(1) o no(0): "))
            elif listaOfertas[i].getSector ==filtro2:
                print(listaOfertas[i].titulo, end="")
                print(listaOfertas[i].descripcion, end="")
                print(listaOfertas[i].experiencia, end="")
                print(listaOfertas[i].estudio, end="")
                print(listaOfertas[i].habilidades, end="")
                pregunta = str(input("acepta la oferta si(1) o no(0): "))
            if pregunta == "1":
                pregunta = "0"
                if self.validar(listaOfertas[i]):
                    
                    print("se cumple con los requisitos, entra en proceso de validacion....")
                    self.validarFiltro(i)
                    return True
                    
                else:
                    print("No cumple con los requisitos")
        print("------------------------------------------")
        return False
    def run(self): #Metodo que se ejecutara con la llamada start
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://"+self.ip+":"+self.puerto)
        socket.subscribe("")
        postulado = False
        while True:
            if postulado == True:
                continue
            else:
                ob = socket.recv_pyobj()
                semaforo.acquire()
                postulado=self.listarOfertas(ob)
                semaforo.release()
        
HiloFiltroSub("25.86.45.96","1000").start()
HiloFiltroSub("25.8.248.34","1000").start()
HiloFiltroSub("25.5.97.125","1000").start()
     
 

       
