import subprocess
import re
import time
import locale
from sys import platform as _platform

def ping_messen():
    # Pinganfrage an google
    if _platform == "linux":
        p = subprocess.Popen('ping -c 1 www.google.de'.split(), stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen('ping -n 1 www.google.de'.split(), stdout=subprocess.PIPE)
    preprocessed, nix = p.communicate()

    # Herausfiltern des Pings in ms
    if _platform == "linux":
        exp = r'time=[\d]+'
    else:
        sprachtupple = locale.getdefaultlocale()
        if sprachtupple[0].startswith('de'):
            exp = r'Zeit=[\d]+'
        else:
            exp = r'time=[\d]+'
        
    match = re.search(exp, preprocessed.decode(encoding='utf-8', errors='ignore'))
    if match:
        try:
            ausgabe = match.group()
            ausgabe = int(ausgabe.split('=')[1])
            formatierteAusgabe(ausgabe)
            return ausgabe
        except:
            print("Fehler beim Bestimmen der Ausgabe, kein Problem.")
    else:
        print("Match war leer, kein Problem.")
            
        
def formatierteAusgabe(ausgabe):
    if ausgabe >= 100:
        print("Aktueller Ping: " + str(ausgabe) +" ms  OOOOOOOOOOO")
    elif ausgabe >= 90:
        print("Aktueller Ping: " + str(ausgabe) +" ms  OOOOOOOOOO")
    elif ausgabe >= 80:
        print("Aktueller Ping: " + str(ausgabe) +" ms  OOOOOOOOO")
    elif ausgabe >= 70:
        print("Aktueller Ping: " + str(ausgabe) +" ms  OOOOOOOO")
    elif ausgabe >= 60:
        print("Aktueller Ping: " + str(ausgabe) +" ms  OOOOOOO")
    elif ausgabe >= 50:
        print("Aktueller Ping: " + str(ausgabe) +" ms  OOOOOO")
    elif ausgabe >= 40:
        print("Aktueller Ping: " + str(ausgabe) +" ms  OOOOO")
    elif ausgabe >= 30:
        print("Aktueller Ping: " + str(ausgabe) +" ms  OOOO")
    elif ausgabe >= 20:
        print("Aktueller Ping: " + str(ausgabe) +" ms  OOO")
    elif ausgabe >= 10:
        print("Aktueller Ping: " + str(ausgabe) +" ms  OO")
    else:
        print("Aktueller Ping: " + str(ausgabe) +" ms  O")

def pingsauswerten(listemitpings):
    if len(listemitpings) != 0:
        pingsumme = 0
        maximum = listemitpings[0]
        for ping in listemitpings:        
            pingsumme += ping
            if maximum < ping:
                maximum = ping
        durchschnitt = pingsumme/len(listemitpings)
        return maximum, durchschnitt
    else:
        return 0, 0

def ergebnisse_speichern(liste_der_ergebnisse):
    try:
        print("Schreibe Ergebnisse in Datei...")
        fobj = open('pingergebnisse.txt', 'a')
        for i in liste_der_ergebnisse:
            fobj.write(str(i)+"\n")
        fobj.write("ENDE - " + time.asctime(time.localtime(time.time())) + "\n" )
        fobj.close()
        print("Dateiausgabe abgeschlossen.")
    except:
        print("Dateiausgabe fehlgeschlagen.")
 
def ergebnisse_speichern_beginnzeitstempel_eintragen():
    try:
        print("Erstelle/Erweitere Ergebnis-Datei...")
        fobj = open('pingergebnisse.txt', 'a')
        fobj.write("BEGINN - " + time.asctime(time.localtime(time.time())) + "\n" )
        fobj.close()
        print("Beginnzeitstempel eingetragen.")
    except:
        print("Dateizugriff fehlgeschlagen. Programm laeuft weiter, Ergebnisse koennen aber unter Umsteanden nicht gespeichert werden.")

if __name__ == "__main__":    
    pingergebnisse = []
    ergebnisse_speichern_beginnzeitstempel_eintragen()
    try:
        i = 0
        while True:        
            time.sleep(1)
            ergebnis = ping_messen()
            # falls ping() kein Ergebnis(None) zurueckliefert, breche Schleifendurchlauf hier ab
            if ergebnis is None:
                continue
            pingergebnisse.append(ergebnis)
            i += 1
    except KeyboardInterrupt:
        print("Abbruch\n")
        
    max, durchschn = pingsauswerten(pingergebnisse)
    print("Durchschnitt: {:4.2f}".format(durchschn))
    print("Maximum: {}".format(max))
    ergebnisse_speichern(pingergebnisse)


