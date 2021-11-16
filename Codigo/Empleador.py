import zmq
from Clases import Oferta
from threading import Semaphore, Thread
import  time
#--------------------------
#leer la ip de donse se esta iniciando el proceso 
#--------------------------
hostPincipal = str(input("Indique la ip: "))
# --------------------------------------------------
#   Establecimiento del pueto de conexion
# --------------------------------------------------
portPub = "5000"  # pueto para que el empleador publique su informacion
#portSub = "6000"  # puero para que el filtro pueda escuchar al empleador
# --------------------------------------------------
#   Se crea el contexto
# --------------------------------------------------
context = zmq.Context()
# --------------------------------------------------
#   Se crea el soket Publicador
# --------------------------------------------------
socketPub = context.socket(zmq.PUB)
#socketSub = context.socket(zmq.SUB)
socketPub.bind("tcp://{}:{}".format(hostPincipal,portPub))
# ------------------------------------
#     crear subscripción
# ------------------------------------
# agregar el nombre

# menu para que el empleador inserte nuevos datos
lista = []
f = open("ofertas.txt")
i = 0
titulo:str
descripcion:str
experiencia:str
estudio = []
habilidades = []
while True:
    l = f.readline()
    if i == 0 :
        titulo=l
    elif i ==  1:
        descripcion = l
    elif i == 2:
        experiencia = l
    elif i == 3:
        estudio = l
    elif i == 4:
        habilidades = l
    if not l:
        break
    if i == 4:
        i = 0
        o = Oferta(titulo, descripcion, experiencia, estudio, habilidades,hostPincipal)
        lista.append(o)
        print(o)
    else:
        i += 1

for i in lista:

    time.sleep(1)
    
    socketPub.send_pyobj(i)
    
class hilosRespeustas(Thread):
    # este hilo se encarga de estar escuchando algun filtro
    # una lista de ofertas
    def __init__(self,ip,puerto,tiempo_inicio): #Constructor de la clase
         Thread.__init__(self)
         self.ip = ip
         self.puerto = puerto
         self.tiempo = tiempo_inicio

    def run(self): #Metodo que se ejecutara con la llamada start
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://{}:{}".format(self.ip,self.puerto))
        socket.subscribe("")
        while True:
            res = socket.recv_string()
            if res == hostPincipal:
                print("una oferta fue aceptada")
        
hilosRespeustas("25.8.248.34","4900",time.time()).start()   
hilosRespeustas("25.86.45.96","4900",time.time()).start() 
hilosRespeustas("25.5.97.125","4900",time.time()).start() 