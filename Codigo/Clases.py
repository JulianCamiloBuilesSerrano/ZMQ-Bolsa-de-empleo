class Oferta():
    def __init__(self,idEmpe, ID,titulo,descripcion,experiencia,estudio, habilidades,Sector):
        self.idEmple =  idEmpe
        self.ID  = None
        self.titulo = titulo
        self.descripcion = descripcion
        self.experiencia = experiencia
        self.estudio = estudio
        self.habilidades = habilidades
        self.sector = Sector

    def __str__(self):
        return "Oferta de empleo  {}, el sector de {}".format(self.titulo, self.sector)
    #end def