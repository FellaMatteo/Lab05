import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    input_marca_auto = ft.TextField(label="Marca")
    input_modello_auto = ft.TextField(label="Modello")
    input_anno_auto = ft.TextField(label="Anno")


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def handleAdd(e):
        currentVal = int(txtOut.value)
        txtOut.value = currentVal + 1
        txtOut.update()

    def handleRemove(e):
        currentVal = int(txtOut.value)
        if currentVal > 0:                  #Diminuisce il valore solamente se il valore attuale è maggiore di 0 (Impedisco valori negativi)
            txtOut.value = currentVal - 1
        txtOut.update()

    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE,
                             icon_color="red",
                             icon_size=24, on_click=handleRemove)
    btnAdd = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           icon_size=24, on_click=handleAdd)
    txtOut = ft.TextField(width=100, disabled=True,
                          value=0, border_color="green",
                          text_align=ft.TextAlign.CENTER)

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    def aggiungi_automobile(e):
        marca = input_marca_auto.value.strip()
        modello = input_modello_auto.value.strip()
        anno_str = input_anno_auto.value.strip()
        posti_str = txtOut.value

        #Controllo campi vuoti
        if not marca or not modello or not anno_str:
            alert.show_alert("Compila tutti i campi (marca, modello, anno).")
            return

        #Controllo campo anno
        try:
            anno = int(anno_str)
        except ValueError:
            alert.show_alert("Il campo 'Anno' deve essere numerico.")
            return

        #Controllo contatore posti
        try:
            posti = int(posti_str)
        except ValueError:
            posti = 0

        #Aggiunta alla struttura dati
        try:
            autonoleggio.aggiungi_automobile(marca, modello, anno, posti)
        except Exception as ex:
            alert.show_alert(f"Errore durante l'aggiunta: {ex}")
            return

        #Svuota i campi
        input_marca_auto.value = ""
        input_modello_auto.value = ""
        input_anno_auto.value = ""
        txtOut.value = "0"

        #Aggiorna la lista visuale
        aggiorna_lista_auto()


    pulsante_aggiungi_automobile = ft.ElevatedButton("Aggoingi automobile", on_click=aggiungi_automobile)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        ft.Text("Aggiungi nuova automobile", size=20),
        ft.Row(
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                input_marca_auto,
                input_modello_auto,
                input_anno_auto,
                btnMinus,
                txtOut,
                btnAdd]),

        pulsante_aggiungi_automobile,

    # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)