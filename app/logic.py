import yt_dlp # for the video download
from pydub import AudioSegment # to extract audio from video
import speech_recognition as sr # to extract text from video

class VideoTransscriptionTool:
       
    def __init__(self, url, path):
        self.url = url
        self.path = path
        
    def download(self):
        ydl_opts = {'format': 'bestaudio/best','outtmpl': self.path+'.webm'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    def extract_audio(self):
        video = AudioSegment.from_file(self.path+'.webm', format="webm")
        audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
        audio.export(self.path+".wav", format="wav")

    def speech_recognition(self):
        r = sr.Recognizer()
        with sr.AudioFile(self.path+".wav") as source:
            audio_text = r.record(source)
        self.text = r.recognize_google(audio_text, language='de-DE')
        return str(self.text)


from youtube_transcript_api import YouTubeTranscriptApi

class GoogleTransscriptionTool:
    
    def __init__(self, url):
        self.video_id = url.split("v=")[1]
        self.video_id = self.video_id.split("&")[0]
    
    def speech_recognition(self):
        transcript = YouTubeTranscriptApi.get_transcript(self.video_id,languages=['de'])
        text = ""
        for line in transcript:
            text += line['text'] + " "
        return text

# Berechnungen und Reguläre Ausdrücke für das Trennen in Wörter
import numpy as np   
import re
# Trennen nach Sätzen
import spacy
# Trennen nach Silben
import pyphen

class TextAnalysisTool:
    """
    Ein Werkzeug zur Textanalyse, das verschiedene Metriken zur Lesbarkeit und Komplexität eines Textes berechnet.
    Attribute:
        text : str
            Der zu analysierende Text.
        out_dict : dict
            Ein Wörterbuch, das die Ergebnisse der Analyse speichert.
    Methoden:
        __init__(text):
            Initialisiert das TextAnalysisTool mit dem gegebenen Text.
        analyse():
            Führt die Textanalyse durch und berechnet verschiedene Metriken wie Anzahl der Wörter, Sätze, Wörter mit mehr als 3 Silben,...
            Gibt ein Wörterbuch mit den Ergebnissen zurück.
        __str__():
            Gibt die Analyseergebnisse als Zeichenkette zurück.
        felsch_interpretation():
            Interpretiert den Flesch-Index und gibt eine Beschreibung der Lesbarkeit des Textes zurück.
    """


    def __init__(self, text):
        """
        Initialisiert eine neue Instanz der Klasse.
        Parameter:
        text (str): Der Eingabetext, der verarbeitet werden soll. 
            Vorangehende, nachfolgende Leer- und bestimmte andere Zeichen (Zeilenumbrüche, *, -, +, /) werden entfernt.
        Returns:
            None    
        """
        self.text = text.strip()
        self.text = re.sub(r'[\n*-+/]', '', self.text)

    def analyse(self):
        """
        Führt die Textanalyse durch und berechnet verschiedene Metriken.
        Parameter:
            None
        Returns:
            dict: Ein Wörterbuch mit den Ergebnissen der Analyse. 
            keys: 
                'w': Anzahl der Wörter im Text.
                's': Anzahl der Sätze im Text.
                'msw': Anzahl der Wörter mit mehr als 3 Silben.
                'wm6b': Anzahl der Wörter mit mehr als 6 Buchstaben.
                'count_silben': Gesamtanzahl der Silben im Text.
                'wstf1': Wiener Sachtextformel 1.
                'wstf2': Wiener Sachtextformel 2.
                'wstf3': Wiener Sachtextformel 3.
                'wstf4': Wiener Sachtextformel 4.
                'flesch_de': Flesch-Index für deutsche Texte.
        """
        self.out_dict = {}

        # Anzahl der Wörter bestimmen
        words = re.split(r'\s+', self.text)
        words = [word.strip() for word in words]
        words = [word for word in words if len(word)>1]
        self.out_dict['w'] = len(words)
        w = len(words)

        # Anzahl der Sätze bestimmen
        nlp = spacy.load("de_core_news_sm")
        doc = nlp(self.text)
        sentences = [sent.text.strip() for sent in doc.sents]
        self.out_dict['s'] = len(sentences)
        s = len(sentences)

        # Anzahl der Wörter mit mehr als 3 silben bestimmen
        dic = pyphen.Pyphen(lang='de_DE')
        msw = 0
        esw = 0
        wm6b = 0
        count_silben = 0

        for word in words:
            silben = dic.inserted(word,hyphen="$")
            
            if len(silben.split("$")) >= 3:
                msw += 1
                print( str(msw) + "--" + word + "--" + silben)

            if len(silben.split("$")) == 1:
                esw += 1
            if len(word) > 6:
                wm6b += 1

            count_silben += len(silben.split("$"))
        self.out_dict['msw'] = msw
        self.out_dict['wm6b'] = wm6b
        self.out_dict['count_silben'] = count_silben

        self.out_dict['wstf1'] = np.round(0.1935*(msw/w*100)+0.1672*(w/s)+0.1297*(wm6b/w*100) - 0.0327 *(esw/w*100) - 0.875,2)
        self.out_dict['wstf2'] = np.round(0.2007*(msw/w*100)+0.1682*(w/s)+0.1373*(wm6b/w*100)-2.779,2)
        self.out_dict['wstf3'] = np.round(0.2963*(msw/w*100)+0.1905*(w/s)-1.1144,2)
        self.out_dict['wstf4'] = np.round(0.2963*(msw/w*100)+0.1905*(w/s)-1.693,2)


        flesch_de = 180 - w/s - 58.8*(count_silben/w)
        self.out_dict['flesch_de'] = flesch_de 



        return self.out_dict




    def __str__(self):
        """
        Gibt die Analyseergebnisse als Zeichenkette zurück.
        Parameter:
            None
        Returns:
            str: Die Analyseergebnisse als formatierte Zeichenkette.
        """
        return str(self.out_dict)
    
    def felsch_interpretation(self):
        """
        Interpretiert den Flesch-Index und gibt eine Beschreibung der Lesbarkeit des Textes zurück.
        Parameter:
            None
        Returns:
            str: Eine Beschreibung der Lesbarkeit des Textes.
        """
        if not isinstance(self.out_dict['flesch_de'], (int, float)):
            return "nicht interpretierbar"
        elif self.out_dict['flesch_de'] > 90:
            return "sehr leicht verständlich"
        elif self.out_dict['flesch_de'] > 80:
            return "leicht verständlich"
        elif self.out_dict['flesch_de'] > 70:
            return "mittelleicht verständlich"
        elif self.out_dict['flesch_de'] > 60:
            return "mittel verständlich"
        elif self.out_dict['flesch_de'] > 50:
            return "mittelschwer verständlich"
        elif self.out_dict['flesch_de'] > 30:
            return "schwer verständlich"
        elif self.out_dict['flesch_de'] > 0:
            return "sehr schwer verständlich"
        else:
            return "nicht interpretierbar"