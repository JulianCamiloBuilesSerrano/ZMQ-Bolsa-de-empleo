class Oferta():
    def __init__(self,titulo,descripcion,experiencia,estudio, habilidades,ip):

        self.ip  = None
        self.titulo = titulo
        self.descripcion = descripcion
        self.experiencia = experiencia
        self.estudio = estudio
        self.habilidades = habilidades

    def setSector(self,sector):
        self.sector = sector
    def __str__(self):
        return "Oferta de empleo  {}".format(self.titulo)
    #end def