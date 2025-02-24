# imports für Gui
import tkinter as tk
from tkinter import ttk

# imports für Nebenläufigkeit 
import threading

# imports für Logik
from logic import VideoTransscriptionTool as vtt
from logic import TextAnalysisTool as tat
from logic import GoogleTransscriptionTool as gtt
import os


class VideoAnalyserGui:
    """
    Die Klasse VideoAnalyserGui erstellt eine grafische Benutzeroberfläche (GUI) zur Analyse von Videos.
    Die GUI ermöglicht es dem Benutzer, eine URL einzugeben, das Video zu laden, das Transkript anzuzeigen und verschiedene Kennzahlen zu analysieren.
    Methoden:
        __init__(): Initialisiert die GUI und erstellt die Benutzeroberfläche. 
        fetch(use_yt_subtitles=True): Ruft Daten von einer gegebenen URL ab, entweder mit YouTube-Untertiteln oder einem API-Worker.
        fetch_worker_google(url): Ruft Daten von einer gegebenen URL ab, indem die YouTube-Untertitel verwendet werden.
        fetch_worker_api(url): Lädt ein Video von der angegebenen URL herunter, extrahiert das Audio und führt eine Spracherkennung durch.
        update_entry(text): Aktualisiert das Eingabefeld mit dem angegebenen Text.
        update_transcript(text): Aktualisiert das Textfeld mit dem angegebenen Text.
        analyse():
    """

    
    def __init__(self):
        """
        Initialisiert die GUI und erstellt die Benutzeroberfläche.
        Args:
            None
        Returns:
            None
        """
        # Fenster erstellen
        self.root = tk.Tk()
        self.root.title("Video Analyser")
        self.root.geometry("600x600")
        self.root.minsize(600, 600)

        # URL-Eingabe mit Button
        self.frame_top = tk.Frame(self.root)
        self.frame_top.pack(fill="x", padx=10, pady=5)
        self.entry_url = tk.Entry(self.frame_top, width=50)
        self.entry_url.pack(side="left", expand=True, fill="x")
        self.btn_fetch = tk.Button(self.frame_top, text="Laden",command=self.fetch)
        self.btn_fetch.pack(side="right", padx=5, )


        # Textfeld für transkribierten Text
        self.label_transcript = tk.Label(self.root, text="Transkript:")
        self.label_transcript.pack(anchor="w", padx=10)
        self.text_transcript = tk.Text(self.root, height=10)
        self.text_transcript.pack(fill="both", expand=True, padx=10, pady=5)

        # Kennzahlen-Interaktionselemente
        self.frame_mid = tk.Frame(self.root)
        self.frame_mid.pack(fill="x", padx=10, pady=5)
        self.btn_analyze = tk.Button(self.frame_mid, text="Analysieren",command=self.analyse)
        self.btn_analyze.pack(padx=10, pady=5, side="left")

        # Kennzahlen-Anzeige
        self.frame_analysis = tk.Frame(self.root)
        self.frame_analysis.pack(fill="x", padx=10, pady=5)

        # Spaltenkonfiguration für gleichmäßige Verteilung
        self.frame_analysis.columnconfigure(0, weight=1)
        self.frame_analysis.columnconfigure(1, weight=1)

        self.label_status = tk.Label(self.frame_analysis, text="Status:")
        self.label_status.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.value_label_status = tk.Label(self.frame_analysis, text="ok")
        self.value_label_status.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        self.label_word_count = tk.Label(self.frame_analysis, text="Wörter:")
        self.label_word_count.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.value_word_count = tk.Label(self.frame_analysis, text="?")
        self.value_word_count.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        self.label_sentence_count = tk.Label(self.frame_analysis, text="Sätze:")
        self.label_sentence_count.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.value_sentence_count = tk.Label(self.frame_analysis, text="?")
        self.value_sentence_count.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        self.label_msw_count = tk.Label(self.frame_analysis, text="Wörter mit mehr als drei Silben:")
        self.label_msw_count.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.value_msw_count = tk.Label(self.frame_analysis, text="?")
        self.value_msw_count.grid(row=3, column=1, sticky="w", padx=5, pady=2)

        self.label_wm6b_count = tk.Label(self.frame_analysis, text="Wörter mit mehr als 6 Buchstaben:")
        self.label_wm6b_count.grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.value_wm6b_count = tk.Label(self.frame_analysis, text="?")
        self.value_wm6b_count.grid(row=4, column=1, sticky="w", padx=5, pady=2)

        self.label_silben_count = tk.Label(self.frame_analysis, text="Silben:")
        self.label_silben_count.grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.value_silben_count = tk.Label(self.frame_analysis, text="?")
        self.value_silben_count.grid(row=5, column=1, sticky="w", padx=5, pady=2)

        self.label_wstf1 = tk.Label(self.frame_analysis, text="1. Wiener Sachtext Formel:")
        self.label_wstf1.grid(row=6, column=0, sticky="w", padx=5, pady=2)
        self.value_wstf1_count = tk.Label(self.frame_analysis, text="?")
        self.value_wstf1_count.grid(row=6, column=1, sticky="w", padx=5, pady=2)

        self.label_wstf2 = tk.Label(self.frame_analysis, text="2. Wiener Sachtext Formel:")
        self.label_wstf2.grid(row=7, column=0, sticky="w", padx=5, pady=2)
        self.value_wstf2_count = tk.Label(self.frame_analysis, text="?")
        self.value_wstf2_count.grid(row=7, column=1, sticky="w", padx=5, pady=2)

        self.label_wstf3 = tk.Label(self.frame_analysis, text="3. Wiener Sachtext Formel:")
        self.label_wstf3.grid(row=8, column=0, sticky="w", padx=5, pady=2)
        self.value_wstf3_count = tk.Label(self.frame_analysis, text="?")
        self.value_wstf3_count.grid(row=8, column=1, sticky="w", padx=5, pady=2)

        self.label_wstf4 = tk.Label(self.frame_analysis, text="4. Wiener Sachtext Formel:")
        self.label_wstf4.grid(row=9, column=0, sticky="w", padx=5, pady=2)
        self.value_wstf4_count = tk.Label(self.frame_analysis, text="?")
        self.value_wstf4_count.grid(row=9, column=1, sticky="w", padx=5, pady=2)

        self.label_flesch_de = tk.Label(self.frame_analysis, text="Flesch-Formel:")
        self.label_flesch_de.grid(row=10, column=0, sticky="w", padx=5, pady=2)
        self.value_flesch_de_count = tk.Label(self.frame_analysis, text="?")
        self.value_flesch_de_count.grid(row=10, column=1, sticky="w", padx=5, pady=2)



        self.root.mainloop()

    def fetch(self, use_yt_subtitles=True):
        """
        Ruft Daten von einer gegebenen URL ab, entweder mit YouTube-Untertiteln oder einem API-Worker.
        Diese Funktion holt die URL aus dem Eingabefeld, deaktiviert den Fetch-Button
        und startet einen neuen Thread, um Daten entweder mit dem Google-Worker oder dem API-Worker abzurufen,
        abhängig vom `use_yt_subtitles`-Flag.
        Args:
            use_yt_subtitles (bool): Flag, ob die YouTube-Untertitel verwendet werden sollen oder nicht.
        Returns:
            None
        """


        self.btn_fetch.config(state="disabled")
        url = self.entry_url.get()
        
        if use_yt_subtitles == True:
            thread = threading.Thread(target=self.fetch_worker_google, args=(url,))
            thread.start()
        else:
            # Starte fetch_data in einem separaten Thread
            thread = threading.Thread(target=self.fetch_worker_api, args=(url,))
            thread.start()

        

    def fetch_worker_google(self, url):
        """
        Ruft Daten von einer gegebenen URL ab, indem die YouTube-Untertitel verwendet werden.
        Diese Funktion aktualisiert die GUI, um anzuzeigen, dass eine Anfrage bearbeitet wird,
        ruft die Untertitel von der angegebenen YouTube-Video-URL mit der gtt-Bibliothek ab
        und aktualisiert die GUI mit dem abgerufenen Transkript und der URL.
        Args:
            url (str): Die URL des Videos
        Returns:
            None
        """
        self.root.after(0, lambda: self.update_entry("Anfrage wird bearbeitet - bitte warten"))
        ggt = gtt(url)
        text = ggt.speech_recognition()
        self.root.after(0, lambda: self.update_transcript(text))
        self.root.after(0, lambda: self.update_entry(url))
        self.root.after(0, lambda: self.btn_fetch.config(state="normal"))


    def fetch_worker_api(self, url):
        """
        Lädt ein Video von der angegebenen URL herunter, extrahiert das Audio und führt eine Spracherkennung durch.
        Aktualisiert die GUI während des Prozesses.
        Args:
            url (str): Die URL des Videos, das heruntergeladen werden soll.
        Schritte:
            1. Lädt das Video von der angegebenen URL herunter.
            2. Aktualisiert die GUI, um den Benutzer über den Fortschritt zu informieren.
            3. Extrahiert das Audio aus dem heruntergeladenen Video.
            4. Führt eine Spracherkennung auf dem extrahierten Audio durch.
            5. Aktualisiert die GUI mit dem erkannten Text.
            6. Entfernt temporäre Dateien.
            7. Aktiviert den Button nach Abschluss des Prozesses wieder.
        Hinweis:
            Die GUI-Updates werden mit der `after()` Methode im Hauptthread durchgeführt, um sicherzustellen, dass die GUI nicht einfriert.
        Returns:
            None
        """

        transcript = vtt(url, "video")
        transcript.download()

        # GUI-Updates mit after() im Hauptthread durchführen
        self.root.after(0, lambda: self.update_entry("Download abgeschlossen - bitte warten"))

        transcript.extract_audio()
        self.root.after(0, lambda: self.update_entry("Audio extrahiert - bitte warten"))

        text = transcript.speech_recognition()
        self.root.after(0, lambda: self.update_transcript(text))
        self.root.after(0, lambda: self.update_entry(url))

        os.remove("video.wav")
        os.remove("video.webm")

        # Button wieder aktivieren
        self.root.after(0, lambda: self.btn_fetch.config(state="normal"))

    def update_entry(self,text):
        """
        Aktualisiert das Eingabefeld mit dem angegebenen Text.
        Args:
            text (str): Der Text, der in das Eingabefeld eingefügt werden soll.
        Returns:
            None
        """
        self.entry_url.delete(0, "end")
        self.entry_url.insert(0, text)

    def update_transcript(self,text):
        """
        Aktualisiert das Textfeld mit dem angegebenen Text.
        Args:
            text (str): Der Text, der im Textfeld angezeigt werden soll.
        Returns:
            None
        """
        self.text_transcript.delete(1.0, "end")
        self.text_transcript.insert("end", text)
        

    def analyse(self):
        """
        Analysiert den im Textfeld enthaltenen Text und zeigt die Ergebnisse in der GUI an.
        Dazu wird das TextAnalysisTool genutzt.
        Args:
            None
        Returns:
            None
        """
        text = self.text_transcript.get(1.0, "end")
        self.analysis = tat(text)
        self.btn_analyze.config(state="disabled")
        thread = threading.Thread(target=self.analyse_worker, args=())
        thread.start()

    def analyse_worker(self):
        """
        Analysiert den im Textfeld enthaltenen Text und zeigt die Ergebnisse in der GUI an.
        Dazu wird das TextAnalysisTool genutzt.
        Args:
            None
        Returns:
            None
        """
        self.root.after(0, lambda: self.value_label_status.config(text="Analyse wird durchgeführt - bitte warten"))
        dict_analysis = self.analysis.analyse()
        self.root.after(0, lambda: self.value_label_status.config(text="Analyse abgeschlossen"))
        self.root.after(0, lambda: self.value_word_count.config(text=dict_analysis["w"]))
        self.root.after(0, lambda: self.value_sentence_count.config(text=dict_analysis["s"]))
        self.root.after(0, lambda: self.value_msw_count.config(text=dict_analysis["msw"]))
        self.root.after(0, lambda: self.value_wm6b_count.config(text=dict_analysis["wm6b"]))
        self.root.after(0, lambda: self.value_wstf1_count.config(text=dict_analysis["wstf1"]))
        self.root.after(0, lambda: self.value_wstf2_count.config(text=dict_analysis["wstf2"]))
        self.root.after(0, lambda: self.value_wstf3_count.config(text=dict_analysis["wstf3"]))
        self.root.after(0, lambda: self.value_wstf4_count.config(text=dict_analysis["wstf4"]))
        self.root.after(0, lambda: self.value_flesch_de_count.config(text=(str(dict_analysis["flesch_de"]) + " - " + self.analysis.felsch_interpretation())))
        self.root.after(0, lambda: self.value_silben_count.config(text=dict_analysis["count_silben"]))
        self.root.after(0, lambda: self.value_label_status.config(text="ok"))
        self.root.after(0, lambda: self.btn_analyze.config(state="normal"))
