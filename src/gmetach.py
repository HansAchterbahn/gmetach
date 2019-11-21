# import the library

import os
from appJar import gui


# handle list box events
def lst_changed(lst):
    global picfile

    try:
        picfile = app.getListBox("list")[0]                                     # Dateinamen des ausgewählten Eintrags in Variable speichern
        picfile = picfile.replace(" ", "\ ")                                    # Leerzeichen im Dateinamen durch "\ " ersetzen

        # print(picfile)
        readData(picfile)                                                       # Metadaten der ausgewählten Datei auslesen und anzeigen
    except:
        print('')


# handle button events
def press(button):
    global picfile

    if button == "Ende":                                                        # Wenn der Button "Ende" gedrückt wird schließt sich das Programm
        app.stop()

    else:                                                                       # Wenn ein anderer Button gedrückt wird (-> "Übernehmen"), werden die eingegebenen Metadaten geschrieben
        writeData(picfile)


# Hilfsfunktion: Zugriff auf die Linux Shell (bash) | es wird aber auch viel popen() verwendet
def sh(script):
    os.system("bash -c '%s'" % script)


# Funktion zur Beschneidung der exiftool Strings auf die gewünschte Information
def optString(string):
    try:
        s = string[0]
        i1 = s.find(":")
        i2 = s.find("\n")

        s = s[(i1 + 2):(i2)]
        #print(s)

        return s

    except:
        return ''


# Hilfsfunktion: Liest mit Hilfe des exiftools (bash) Metadaten aus der gewählten Datei
def readData(f):

    # Auslesen der Metadaten
    title = optString(os.popen("exiftool -Headline " + f).readlines())
    author = optString(os.popen("exiftool -By-line " + f).readlines())
    source = optString(os.popen("exiftool -Source " + f).readlines())
    referencedate = optString(os.popen("exiftool -Caption-Abstract " + f).readlines())#[13:]
    licence = optString(os.popen("exiftool -CopyrightNotice " + f).readlines())
    keywords = optString(os.popen("exiftool -Keywords " + f).readlines())
    credit = optString(os.popen("exiftool -Credit " + f).readlines())
    contact = optString(os.popen("exiftool -Contact " + f).readlines())
    caption = optString(os.popen("exiftool -Caption " + f).readlines())
    objectname = optString(os.popen("exiftool -ObjectName " + f).readlines())
    releacedate = optString(os.popen("exiftool -ReleaseDate " + f).readlines())

    # Anzeigen der Metadaten in den zugehörigen Feldern
    app.setEntry("Titel", title)
    app.setEntry("Autor", author)
    app.setEntry("Quelle", source)
    app.setEntry("Abrufdatum (DD.MM.YYYY)", referencedate)
    app.setEntry("Lizenz", licence)
    app.setEntry("Schlagworte", keywords)
    app.setEntry("Anbieter", credit)
    app.setEntry("Kontakt", contact)
    app.setEntry("Kurzbeschreibung", caption)
    app.setEntry("Ursp. Dateiname", objectname)
    app.setEntry("Veröffentlichungsdatum (YYYYMMDD)", releacedate)

# Hilfsfunktion: Schreibt mit Hilfe des exiftools (bash) Metadaten in die gewählte Datei
def writeData(f):

    # Metadaten werden aus den Feldern zwishengespeichert
    title = app.getEntry("Titel")
    author = app.getEntry("Autor")
    source = app.getEntry("Quelle")
    referencedate = app.getEntry("Abrufdatum (DD.MM.YYYY)")
    licence = app.getEntry("Lizenz")
    keywords = app.getEntry("Schlagworte")
    credit = app.getEntry("Anbieter")
    contact = app.getEntry("Kontakt")
    caption = app.getEntry("Kurzbeschreibung")
    objectname = app.getEntry("Ursp. Dateiname")
    releacedate = app.getEntry("Veröffentlichungsdatum (YYYYMMDD)")

    # Der bash Befehl wird stückweise mit den notwendigen Flags vorbereitet
    c1 = ' -Headline="' + title + '"'
    c2 = ' -By-line="' + author + '"'
    c3 = ' -Source="' + source + '"'
    c4 = ' -Caption-Abstract="' + referencedate + '"'
    c5 = ' -CopyrightNotice="' + licence + '"'
    c6 = ' -Keywords="' + keywords + '"'
    c7 = ' -Credit="' + credit + '"'
    c8 = ' -Contact="' + contact + '"'
    c9 = ' -Caption="' + caption + '"'
    c10 = ' -ObjectName="' + objectname + '"'
    c11 = ' -ReleaseDate="' + releacedate + '"'

    # Zusammensetzen und ausführen des bash Befehls
    cmd = 'exiftool' + c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + c10 + c11 + ' -overwrite_original_in_place ' + f
    #print(cmd)
    #print(title + "\n" + author + "\n" + source + "\n" + referencedate + "\n" + licence + "\n" + keywords + "\n" + credit + "\n" + contact + "\n" + caption + "\n" + objectname + "\n" + releacedate + "\n" + "---")
    sh(cmd)



# Globale Variable für aktuelle Datei
picfile = ''

# create a GUI variable called app
app = gui("gmetach", "600x700")
app.setBg("orange")
app.setFont(14)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Metadaten zu Bild hinzufügen ...")
app.setLabelBg("title", "blue")
app.setLabelFg("title", "orange")

fcontent = os.popen("ls *.png *.jpg *.jpeg *.gif *.bmp *.tif").readlines()      # Inhalt des Ordners einlesen
for i in range(len(fcontent)):                                                  # \n von einträgen entfernen
    fcontent[i] = fcontent[i][0:-1]

app.addListBox("list",fcontent)                                                 # Liste mit Ordnerinhalt anlegen
app.setListBoxChangeFunction("list", lst_changed)

app.addLabelEntry("Titel")                                                      # Feld angelegt: Titel
app.addLabelEntry("Autor")                                                      # Feld angelegt: Autor
app.addLabelEntry("Quelle")                                                     # Feld angelegt: Quelle
app.addLabelEntry("Abrufdatum (DD.MM.YYYY)")                                    # Feld angelegt: Abrufdatum
app.addLabelEntry("Lizenz")                                                     # Feld angelegt: Lizenz
app.addLabelEntry("Schlagworte")                                                # Feld angelegt: Schlagworte
app.addLabelEntry("Anbieter")                                                   # Feld angelegt: Anbieter
app.addLabelEntry("Kontakt")                                                    # Feld angelegt: Kontakt
app.addLabelEntry("Kurzbeschreibung")                                           # Feld angelegt: Kurzbeschreibung
app.addLabelEntry("Ursp. Dateiname")                                            # Feld angelegt: Ursprünglichen Dateinamen
app.addLabelEntry("Veröffentlichungsdatum (YYYYMMDD)")                          # Feld angelegt: Veröffentlichungsdatum

# link the buttons to the function called press
app.addButtons(["Übernehmen", "Ende"], press)                                   # Buttons angelegt: Übernehmen und Ende

#app.setFocus("Titel")

# start the GUI
app.go()
