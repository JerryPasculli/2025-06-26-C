from dataclasses import dataclass


@dataclass
class Constructor:
    constructorId: int
    constructorRef: str
    name: str
    nationality: str
    url: str

    def __hash__(self):
        return hash(self.constructorId)
    def __eq__(self, other):
        return self.constructorId==other.constructorId
    def setDiz(self):
        self.diz = []
    def setIncidenti(self, p):
        self.incidenti = p

    def __lt__(self, other):
        return self.incidenti<other.incidenti

    def setI(self):
        totale = len(self.diz)
        meno = 0
        for element in self.diz:
            if element[1] is not None:
                meno = meno+1
        self.I = 1-meno/totale
    def setM(self, M):
        self.M = M