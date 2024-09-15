import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._min_lat = None
        self._max_lat = None
        self._min_lng = None
        self._max_lng = None
        self._get_lat_lng_limits()

    def handle_graph(self, e):
        # read latitude
        try:
            latitude = float(self._view.txt_latitude.value)
        except:
            self._view.create_alert(f"La latitudine deve essere un valore numerico compreso tra {self._min_lat} e {self._max_lat}")
            return
        if latitude < self._min_lat or latitude > self._max_lat:
            self._view.create_alert(f"La latitudine deve essere un valore numerico compreso tra {self._min_lat} e {self._max_lat}")
            return

        # read longitude
        try:
            longitude = float(self._view.txt_longitude.value)
        except:
            self._view.create_alert(f"La longitudine deve essere un valore numerico compreso tra {self._min_lng} e {self._max_lng}")
            return
        if longitude < self._min_lng or longitude > self._max_lng:
            self._view.create_alert(f"La longitudine deve essere un valore numerico compreso tra {self._min_lng} e {self._max_lng}")
            return

        #read shape
        if self._view.ddshape.value is None or self._view.ddshape.value=="":
            self._view.create_alert("Selezionare una shape!")
            return
        shape = self._view.ddshape.value

        # stampa dei risultati
        self._view.txt_result1.controls.clear()
        self._model.create_graph(latitude, longitude, shape)
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_of_nodes()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.get_num_of_edges()}\n"))

        top5_nodes = self._model.get_top5_nodi()
        self._view.txt_result1.controls.append(ft.Text(f"I 5 nodi di grado maggiore sono:"))
        for n in top5_nodes:
            self._view.txt_result1.controls.append(ft.Text(f"{n[0]} -> degree: {n[1]}"))

        top5_edges = self._model.get_top5_archi()
        self._view.txt_result1.controls.append(ft.Text(f"I 5 archi di peso maggiore sono:"))
        for e in top5_edges:
            self._view.txt_result1.controls.append(ft.Text(f"{e[0]}<->{e[1]}  |  peso ={e[2]["weight"]}"))

        self._view.btn_path.disabled = False
        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        path, punteggio = self._model.cammino_ottimo()
        self._view.txt_result2.controls.append(ft.Text(f"Il punteggio del percorso ottimo è {punteggio}"))
        self._view.txt_result2.controls.append(ft.Text(f"Il percorso ottimo è costituito da {len(path)} nodi:"))
        for p in path:
            self._view.txt_result2.controls.append(ft.Text(f"{p} | densità = {p.Population/p.Area}"))

        self._view.update_page()

    def _get_lat_lng_limits(self):
        self._min_lat, self._max_lat, self._min_lng, self._max_lng = self._model.get_lat_lng_limits()

    def fill_ddshape(self):
        shapes = self._model.get_shapes()
        self._view.ddshape.options.clear()
        for s in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(f"{s}"))
