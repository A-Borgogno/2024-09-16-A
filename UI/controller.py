import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        lat = self._view.txt_latitude.value
        if lat == "":
            self._view.txt_result1.controls.append(ft.Text("Inserire la latitudine", color="red"))
            self._view.update_page()
            return
        lon = self._view.txt_longitude.value
        if lon == "":
            self._view.txt_result1.controls.append(ft.Text("Inserire la longitudine", color="red"))
            self._view.update_page()
            return
        try:
            intLat = int(lat)
            intLon = int(lon)
        except ValueError:
            self._view.txt_result1.controls.append(ft.Text("I valori inseriti devono essere dei numeri interi", color="red"))
            self._view.update_page()
            return
        if self._model.getMinLat() > intLat or self._model.getMaxLat() < intLat:
            self._view.txt_result1.controls.append(ft.Text(f"La latitudine deve essere compresa tra {self._model.getMinLat()} e {self._model.getMaxLat()}", color="red"))
            self._view.update_page()
            return
        if self._model.getMinLon() > intLon or self._model.getMaxLon() < intLon:
            self._view.txt_result1.controls.append(ft.Text(f"La longitudine deve essere compresa tra {self._model.getMinLon()} e {self._model.getMaxLon()}", color="red"))
            self._view.update_page()
            return
        shape = self._view.ddshape.value
        if not shape:
            self._view.txt_result1.controls.append(ft.Text("Selezionare la forma", color="red"))
            self._view.update_page()
            return
        self._view.txt_result1.controls.append(ft.Text("Caricamento in corso", weight=ft.FontWeight.BOLD))
        self._view.update_page()
        nodes, edges = self._model.buildGraph(intLat, intLon, shape)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {nodes}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {edges}"))
        nodiGrado = self._model.getNodiGrado()
        self._view.txt_result1.controls.append(ft.Text(""))
        self._view.txt_result1.controls.append(ft.Text("I 5 nodi di grado maggiore sono:"))
        for n in nodiGrado[:5]:
            self._view.txt_result1.controls.append(ft.Text(f"{n} -> degree: {self._model.getGradoNodo(n)}"))
        archiPeso = self._model.getArchiPeso()
        self._view.txt_result1.controls.append(ft.Text("I 5 archi di peso maggiore sono:"))
        for a in archiPeso[:5]:
            self._view.txt_result1.controls.append(ft.Text(f"{a[0]} <-> {a[1]} | peso = {a[2]["weight"]}"))
        self._view.btn_path.disabled = False
        self._view.update_page()


    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        bestPath, score = self._model.getBestPath()
        self._view.txt_result2.controls.append(ft.Text("Trovato cammino ottimo"))
        for node in bestPath:
            self._view.txt_result2.controls.append(ft.Text(f"{node} | densità = {self._model.getDensita(node)}"))
        self._view.txt_result2.controls.append(ft.Text(f"Punteggio percorso: {score}"))
        self._view.update_page()

    def fill_ddshape(self):
        shapes = self._model.getShapes()
        for s in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()
