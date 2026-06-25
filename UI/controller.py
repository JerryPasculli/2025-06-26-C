import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._flag = False

    def handleBuildGraph(self, e):
        self._view._txtGraphDetails.controls.clear()
        v1 = self._view._ddYear1.value
        v2 = self._view._ddYear2.value
        if v1 is None or v2 is None or v1>v2:
            self._flag = False
            t1 = ft.Text("NON HAI SCELTO UN RANGE COERENTE", color ="red")
            self._view._txtGraphDetails.controls.append(t1)
            self._view.update_page()
            return
        v1 = int(v1)
        v2 = int(v2)
        stringa = self._model.creaGrafo(v1, v2)
        t1 = ft.Text(stringa)
        self._view._txtGraphDetails.controls.append(t1)
        self._flag = True
        self._view.update_page()



    def handlePrintDetails(self, e):
        if self._flag == False:
            t1 = ft.Text("PER I DETTAGLI DEVI PRIMA CREARE IL GRAFO", color="red")
            self._view._txtGraphDetails.controls.append(t1)
            self._view.update_page()
            return
        stringa = self._model.output()
        t1 = ft.Text(stringa)
        self._view._txtGraphDetails.controls.append(t1)
        self._view.update_page()


    def handleCercaTeamSfortunati(self, e):
        self._view._txt_result.controls.clear()
        k = self._view._txtInSoglia.value
        m = self._view._txtInNumDiEdizioni.value
        try:
            int(k)
            int(m)
        except:
            t1 = ft.Text("NON HAI INSERITO VALORI NUMERICI DI K E M", color="red")
            self._view._txtGraphDetails.controls.append(t1)
            self._view.update_page()
            return
        stringa = self._model.percorso(int(k), int(m))
        t1 = ft.Text(stringa)
        self._view._txt_result.controls.append(t1)
        self._view.update_page()


    def popola(self):
        lista = self._model.anni()
        for element in lista:
            opt = ft.dropdown.Option(element[0])
            self._view._ddYear1.options.append(opt)
            self._view._ddYear2.options.append(opt)

