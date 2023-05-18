import tkinter as tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageTk
import tkintermapview


class Plotwindow:
    def __init__(self, my_label):  # Erstellen wir eine Tkinter-Karte
        self.map_widget = tkintermapview.TkinterMapView(my_label, width=900, height=500)
        self.map_widget.set_position(30, 0)
        self.map_widget.set_zoom(1)
        self.map_widget.grid(row=1, column=0)

    def plotxy(self):  # Wenn wir auf den Plot klicken, zeichnen wir Markierungen für das Jahr 2000 auf der Karte
        for i, row in df.iterrows():
            if row[0] == 2000:
                self.map_widget.set_marker(float(row[2]), float(row[3]), text=f"{row[1]}: {row[4]} $",
                                           font=("Bahnschrift", 12), icon=plane_image)

    def selected_Years(self, event):  # Wenn wir ein Jahr auswählen, zeichnen wir erneut Markierungen auf der Karte
        year = clicked.get()
        self.map_widget.delete_all_marker()
        for i, row in df.iterrows():
            if row[0] == float(year):
                self.map_widget.set_marker(float(row[2]), float(row[3]), text=f"{row[1]}: {row[4]} $",
                                           font=("Bahnschrift", 12), icon=plane_image)

    def clearplot(self):  # löchen alle Marker
        self.map_widget.delete_all_marker()


def statistik_plot():
    # neu Window für Statistik
    root2 = tk.Tk()
    root2.title("Statistik")
    year = clicked.get()
    label = tk.Label(root2, text=f" Bigmac Preise in der Welt in {year} Jahr ")
    label.config(font=("Courier", 24))
    label.grid(row=0, column=0)
    fig, ax = plt.subplots(figsize=(16, 8))  # Figure Klasse: zum Zeichnen geeignet;
    # erstellen wir canvas as matplotlib drawing area
    canvas = FigureCanvasTkAgg(fig, master=root2)  # alias FigureCanvas
    canvas.get_tk_widget().grid(row=1, column=0)  # Get reference to tk_widget
    toolbar = NavigationToolbar2Tk(canvas, root2, pack_toolbar=False)
    # matplotlib navigation toolbar
    toolbar.grid(row=2, column=0, sticky=tk.W)
    x = []
    y = []
    for i, row in df.iterrows():
        if row[0] == float(year):
            x.append(row[1])
            y.append(float(row[4]))

    # erstellen ein Balkendiagramm
    ax.bar(x, y)
    ax.tick_params(axis="x", labelrotation=90)
    ax.set_xlabel("Price in $")
    ax.grid()
    canvas.draw()


# Informationen aus csv-Datei lesen
df = pd.read_csv("BigmacPrice.csv")

# Fenster Tkinter erstellen
root = tk.Tk()
root["bg"] = "white"
root.title("Bigmac Prices")
root.geometry("900x700")
my_label = LabelFrame(root)
my_label.grid(row=2, column=0)
plot_w = Plotwindow(my_label)
buttonframe = tk.Frame(background="white")
buttonframe.grid(row=1, column=0, sticky=tk.W)

#icon bild ändern
image3 = Image.open("icon3.png")
plane_image = ImageTk.PhotoImage((image3).resize((30, 30)))

# Text hinzufügen
canvas = tk.Canvas(root, height=100, width=750, highlightthickness=0,bg="white")
image2 = Image.open("text.png")
photo2 = ImageTk.PhotoImage(image2)
image2 = canvas.create_image(180, 60, anchor='nw', image=photo2)

# Bild Bigmac hinzufügen
image = Image.open("bigmac.png")
photo = ImageTk.PhotoImage(image)
image = canvas.create_image(40, 10, anchor='nw', image=photo)
canvas.grid(row=0, column=0)

# Scrollbar hinzufügen
years = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013",
         "2014", "2015", "2016"]
clicked = StringVar()
clicked.set(years[0])
drop = OptionMenu(root, clicked, *years, command=plot_w.selected_Years)
drop.grid(row=3, column=0)

# Button hinzufügen
b2 = tk.Button(buttonframe, text="Plot", command=plot_w.plotxy, height=2, width=5)
b2.grid(row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
b3 = tk.Button(buttonframe, text="Clear", command=plot_w.clearplot, activeforeground="red", height=2, width=5)
b3.grid(row=1, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
b4 = tk.Button(buttonframe, text="Statistik", command=statistik_plot, activeforeground="red", height=2, width=10,bg="lightgreen")
b4.grid(row=1, column=2, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

root.mainloop()
