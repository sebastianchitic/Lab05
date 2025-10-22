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
        autonoleggio.carica_file_automobili(FILE_AUTO)  # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

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

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile
    myText = ft.Text(value='Aggiungi Nuova Automobile', size=20)
    marcaAuto = ft.TextField(label="Marca", width=200)
    modelloAuto = ft.TextField(label="Modello", width=200)
    annoAuto = ft.TextField(label="Anno", width=120)

    contatore_posti = ft.Text("1", size=16, width=80, text_align=ft.TextAlign.CENTER)

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

    def incrementa_posti(e):
        current = int(contatore_posti.value)
        contatore_posti.value = str(current + 1)
        page.update()

    def decrementa_posti(e):
        current_value = int(contatore_posti.value)
        if current_value > 1:  # Almeno 1 posto
            contatore_posti.value = str(current_value - 1)
            page.update()

    def aggiungi_auto(e):
        try:
            marca = marcaAuto.value.replace('Inserisci marca: ', '').strip()
            modello = modelloAuto.value.replace('Inserisci modello: ', '').strip()
            anno_str = annoAuto.value.replace('Inserisci anno: ', '').strip()

            if not marca or not modello or not anno_str:
                alert.show_alert('❌ Compila tutti i campi!')
                return

            anno = int(anno_str)
            posti = int(contatore_posti.value)

            # Validazione anno
            if anno < 1885 or anno > 2026:
                alert.show_alert("❌ Anno non valido (deve essere tra 1885 e 2026)")
                return

            if posti <= 0:
                alert.show_alert("❌ Il numero di posti deve essere maggiore di 0")
                return

            nuova_auto = autonoleggio.aggiungi_automobile(
                marca,
                modello,
                anno,
                posti
            )

            if nuova_auto:
                alert.show_alert(f'✅ Auto {nuova_auto.codice} aggiunta!')
                marcaAuto.value = ''
                modelloAuto.value = ''
                annoAuto.value = ''
                contatore_posti.value = "1"
                aggiorna_lista_auto()
            else:
                alert.show_alert("❌ Auto già esistente!")

        except ValueError:
            alert.show_alert("❌ Inserisci un anno valido!")
        except Exception as e:
            alert.show_alert(f"❌ Errore: {e}")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    btn_incrementa = ft.ElevatedButton("+", on_click=incrementa_posti, width=40)
    btn_decrementa = ft.ElevatedButton("-", on_click=decrementa_posti, width=40)
    btn_aggiungi_auto = ft.ElevatedButton("Aggiungi Auto", on_click=aggiungi_auto)

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
        ft.Divider(),
        ft.Text("Aggiungi Nuova Automobile", size=20),
        ft.Row(
            controls=[
                marcaAuto,
                modelloAuto,
                annoAuto,
                ft.Column([
                    ft.Text("Posti", size=12),
                    ft.Row([
                        btn_decrementa,
                        contatore_posti,
                        btn_incrementa,
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ]),
                btn_aggiungi_auto
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()


ft.app(target=main)