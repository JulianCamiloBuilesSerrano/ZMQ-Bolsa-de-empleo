class Oferta():
    def __init__(self,titulo,descripcion,experiencia,estudio, habilidades,ip,sector=""):
        self.sector = sector
        self.ip  = ip
        self.titulo = titulo
        self.descripcion = descripcion
        self.experiencia = experiencia
        self.estudio = estudio
        self.habilidades = habilidades

    def setSector(self,sector):
        self.sector = sector
    def getSector(self):
        return self.sector
    def __str__(self):
        return "Oferta de empleo  {}".format(self.titulo)
    #end def