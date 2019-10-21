# import the library

import os
from appJar import gui


# handle list box events
def lst_changed(lst):
    global picfile

    try:
        picfile = app.getListBox("list")[0]
        #print(picfile)
        readData(picfile)
    except:
        print('')


# handle button events
def press(button):
    global picfile

    if button == "Ende":
        app.stop()

    else:
        writeData(picfile)
        #app.stop()


def sh(script):
    os.system("bash -c '%s'" % script)


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


def readData(f):
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


def writeData(f):
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

    cmd = 'exiftool' + c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + c10 + c11 + ' -overwrite_original_in_place ' + f
    print(cmd)
    #print(title + "\n" + author + "\n" + source + "\n" + referencedate + "\n" + licence + "\n" + keywords + "\n" + credit + "\n" + contact + "\n" + caption + "\n" + objectname + "\n" + releacedate + "\n" + "---")
    sh(cmd)



# Globale Variable für aktuelle Datei
picfile = ''

# create a GUI variable called app
app = gui("metach", "600x700")
app.setBg("orange")
app.setFont(14)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Metadaten zu Bild hinzufügen ...")
app.setLabelBg("title", "blue")
app.setLabelFg("title", "orange")

app.addListBox("list",os.popen("ls").readlines())
app.setListBoxChangeFunction("list", lst_changed)

app.addLabelEntry("Titel")
app.addLabelEntry("Autor")
app.addLabelEntry("Quelle")
app.addLabelEntry("Abrufdatum (DD.MM.YYYY)")
app.addLabelEntry("Lizenz")
app.addLabelEntry("Schlagworte")
app.addLabelEntry("Anbieter")
app.addLabelEntry("Kontakt")
app.addLabelEntry("Kurzbeschreibung")
app.addLabelEntry("Ursp. Dateiname")
app.addLabelEntry("Veröffentlichungsdatum (YYYYMMDD)")

# link the buttons to the function called press
app.addButtons(["Übernehmen", "Ende"], press)

#app.setFocus("Titel")

# start the GUI
app.go()