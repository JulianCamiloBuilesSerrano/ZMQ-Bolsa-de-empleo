import zmq
from Clases import Oferta

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
socketPub.bind("tcp://25.86.45.96:{}".format(portPub))

# ------------------------------------
#     crear subscripción
# ------------------------------------


# agregar el nombre

# menu para que el empleador inserte nuevos datos


def crearOferta():
    idEmple = str(input("inidque el id del empleador: "))
    titulo = str(input("indiquie el titulo de la nueva oferta: "))
    descripcion = str(input("Descripcion de la oferta: "))
    experiencia = str(input("Años de experiencia requerida: "))
    estudio = str(input("Estudio basico requerido: "))
    termina = False
    habilidades = []
    while not termina:
        habilidades.append(str(input("Digite una habilidad: ")))
        r = int(input("Quiere agregar mas? 1.si 2.no: "))
        if r == 1:
            termina = False
        elif r == 2:
            termina = True
    print("tipo de sector: ")
    sel = int(input("1.Gerencia\n2.Ingenieria\n3.Salud\n4.Ciencia\n5.Docencia\n"))
    sector = ""
    if sel == 1:
        sector = "Gerencia"
    elif sel == 2 :
        sector = "Ingenieria"
    elif sel == 3:
        sector = "Salud"
    elif sel == 4:
        sector = "Ciencia"
    elif  sel == 5:
        sector = "Docencia"
    return Oferta(idEmple, 0, titulo, descripcion, experiencia, estudio, habilidades,sector)


fin = False
while not fin:
    print("----------Menu de Empleador-------")
    opt = int(input("1.Agregar Oferta de empleo\n2.salir"))
    if opt == 1:
        ofe = crearOferta()
        socketPub.send_pyobj(ofe)
    elif opt == 2:
        fin = True
