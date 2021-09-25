import zmq
from Clases import  Oferta
portEmp = "5000"
portServ = "6000"
host = "25.86.45.96"

context = zmq.Context()
socketSub =  context.socket(zmq.SUB)
socketServer =  context.socket(zmq.REQ)

socketSub.connect("tcp://{}:{}".format(host,portEmp))


socketSub.subscribe("")

ofer = socketSub.recv_pyobj()
print(ofer)