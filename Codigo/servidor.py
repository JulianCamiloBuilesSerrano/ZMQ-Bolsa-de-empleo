import zmq
port = "6000"
host = "25.86.45.96"
#Creamos el contexto 
context = zmq.Context()

socketServer = context.socket(zmq.REP)
socketServer.bind("tcp://{}:{}".format(host,port))

while True:
    ofer = socketServer.recv_pyobj()
    print(ofer)
    #Guardar en la Base de datos 

    socketServer.send("recibido")
