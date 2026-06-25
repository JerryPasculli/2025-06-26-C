import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._G = nx.Graph()
        self._nodi = []
        self._archi = []
        self._Dnodi = {}

    def creaGrafo(self, v1, v2):
        self._G = nx.Graph()
        self._nodi = DAO.getNodi()
        self._archi = []
        self._Dnodi = {}
        self._G.add_nodes_from(self._nodi)
        listaPunti = DAO.getIntersezioni(v1, v2)
        listaM = DAO.getM(v1, v2)
        for element in self._nodi:
            punto = listaPunti.get(element.constructorId)
            M = listaM.get(element.constructorId)
            if punto is None:
                punto = 0
            if M is None:
                M = 0
            self._Dnodi[element.constructorId] = element
            element.setM(M)
            element.setDiz()
            element.setIncidenti(punto)
        lista = DAO.getArchi(v1, v2)
        listaRisultati = DAO.getDizionario(v1, v2)
        for element in listaRisultati:
            nodo = self._Dnodi[element[0]]
            tupla = (element[2], element[3])
            nodo.diz.append(tupla)
        for element in lista:
            n1 = self._Dnodi[element[0]]
            n2 = self._Dnodi[element[1]]
            peso = element[2]
            self._G.add_edge(n1, n2, weight = peso)
        stringa = f"Grafo correttamente creato.\nIl grafo contiene {self._G.number_of_nodes()} nodi e {self._G.number_of_edges()} archi."
        return stringa

    def output(self):
        stringa = "Stampa dettagli: "
        self._nodiComp = list(self._G.subgraph(max(nx.connected_components(self._G), key = len)).nodes())
        self._nodiComp.sort(reverse=True)
        for element in self._nodiComp:
            stringhetta = f"\n{element.name} -- {element.incidenti}"
            stringa = stringa + stringhetta
        return stringa

    def anni(self):
        lista = DAO.getAnni()
        return lista

    def percorso(self, K, M):
        self._percorso = []
        self._top = 0
        listina = copy.deepcopy(self._nodiComp)
        for element in self._nodiComp:
            if element.M<M:
                listina.remove(element)
        for element in listina:
            element.setI()
        for element in listina:
            parziale = set()
            parziale.add(element)
            tot = element.I
            self.itera(parziale, tot, K, listina)
        stringa = f"Risultato ottimo con valore {self._top}"
        for element in self._percorso:
            stringa =stringa + f"\n{element.name} - {element.M}"
        return stringa

    def itera(self, parziale, tot, K, listina):
        # potevo usare un backtracking con lista ed indice, ma per come sono fatto mentalmente
        #mi risulta naturale immaginare di iterare per ogni elemento fino ad esaurimento.
        #perdo efficienza (genero gli stessi sottoinsiemi in piu' ordini, ~K! volte) ma rispetto
        # al contesto d'esame questa perdita e' trascurabile. uso il set perche' e' la struttura
        # naturale per tenere i gia' scelti e mi da' il check con "in" in O(1)
        if len(parziale) == K:
            if tot>self._top:
                self._percorso = copy.deepcopy(parziale)
                self._top = tot
            return
        for element in listina:
            if element not in parziale:
                parziale.add(element)
                tot1 = tot + element.I
                self.itera(parziale, tot1, K, listina)
                parziale.remove(element)


