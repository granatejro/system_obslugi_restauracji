from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from pymongo import MongoClient
from functools import partial

client = MongoClient("mongodb+srv://root:123@cokolwiekdb-8olh4.mongodb.net/test?retryWrites=true&w=majority")
dbadmin=client.admin
serverStatusResult=dbadmin.command("serverStatus")

db = client.eCaterer

class Produkty:
    def __init__(self, id_prod):
        rekord = db.Produkty.find_one({'id_produktu': id_prod})
        self.id_produktu = rekord['id_produktu']
        self.nazwa = rekord['nazwa']
        self.cena = rekord['cena']


class Osoba:
    def __init__(self, id_os):
        rekord = db.Osoby.find_one({'id_osoby': id_os})
        self.id = rekord['id_osoby']
        self.imie = rekord['imie']
        self.nazwisko = rekord['nazwisko']
        self.plec = rekord['plec']


class Klient:
    def __init__(self, id_kl):
        rekord = db.Klienci.find_one({'id_klienta': id_kl})
        self.id_klienta = rekord['id_klienta']
        self.id_osoby = rekord['id_osoby']
        self.aplikacja = rekord['aplikacja']


class KoszykC:
    def __init__(self):
        self.lista_przedmiotow = []
        self.przedmiot_cena = []
        self.suma = 0

class Zamowienie:
    def __init__(self, lista_prod):
        self.id_zamowienia = 1
        self.status = 'Przyjęte'
        self.lista_produktow = lista_prod
        flaga_zam = 0
        while (flaga_zam == 0):
            el = db.Zamowienia.find_one({'id_zamowienia': self.id_zamowienia})
            if (el is not None):
                self.id_zamowienia = el['id_zamowienia'] + 1
            if (el is None):
                flaga_zam = 1
                db.Zamowienia.insert_one({'id_zamowienia': self.id_zamowienia, 'status': 'Przyjęte', 'lista_produktow': lista.lista_przedmiotow})


def DodajProdukt(id):
    global it
    produkt = db.Produkty.find_one({'id_produktu': id})
    lista.lista_przedmiotow.append(produkt['nazwa'])
    lista.suma += produkt['cena']
    lista.przedmiot_cena.append(produkt['cena'])
    listaid.append(produkt['id_produktu'])
    koszyk_produkty.append(Label(koszyk_scrollable, text=""))
    if it<len(lista.lista_przedmiotow):
        koszyk_produkty[it].configure(text=lista.lista_przedmiotow[it])
        koszyk_produkty[it].grid(column=1, row=it+2)
        lista_buttonow.append(Button(koszyk_scrollable, text='x', command=partial(UsunProdukt,it)))
        lista_buttonow[it].grid(column=2,row=it+2)
    else:
        koszyk_produkty[it].configure(text=lista.lista_przedmiotow[it])
        koszyk_produkty[it].grid(column=1, row=it)
        lista_buttonow.append(Button(koszyk_scrollable, text='x', command=partial(UsunProdukt, it)))
        lista_buttonow[it].grid(column=2, row=it)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side='left', fill="both", expand=True)
    koszyk_cena.configure(text=str(abs(round(lista.suma,2))) + ' zł')
    koszyk_cena.grid(column=1, row=0)
    print(it)
    it += 1

def UsunProdukt(nr):
    global it
    print(nr)
    lista.suma -= float(lista.przedmiot_cena[nr])
    koszyk_produkty[nr].grid_forget()
    koszyk_produkty[nr].destroy()
    lista_buttonow[nr].grid_forget()
    lista_buttonow[nr].destroy()
    koszyk_produkty.pop(nr)
    lista.lista_przedmiotow.pop(nr)
    lista.przedmiot_cena.pop(nr)
    listaid.pop(nr)
    lista_buttonow.pop(nr)
    print(lista.lista_przedmiotow)
    it -= 1
    for g in range(nr,it):
         koszyk_produkty[g].configure(text=lista.lista_przedmiotow[g])
         lista_buttonow[g].configure(text='x', command=partial(UsunProdukt, g))
    koszyk_cena.configure(text=str(abs(round(lista.suma,2))) + ' zł')


def PobierzProdukty():
    for i in range(1,max_id_produktu):
        temp = Produkty(i)
        target[i].configure(text=temp.nazwa)
        target2[i].grid(column=2, row=i)

def ClearTarget():
    for i in range(1,max_id_produktu):
        target[i].configure(text="")
        target2[i].grid_remove()

def PrzejdzDoZamowienia():
    global it
    it = 0
    zamow.grid_forget()
    contact.grid_forget()
    zlozenie_zamowienia.grid(column=1, row=1)
    wroc_zamowienie.grid(column=2, row=1)
    PobierzProdukty()

def ZlozZamowienie():
    if (len(lista.lista_przedmiotow) > 0):
        zam = Zamowienie(lista.lista_przedmiotow)
        check = messagebox.askquestion(title='Sposób płatności', message='Czy chcesz zapłacić kartą online?')
        if (check == 'yes'):
            db.Platnosci.insert_one({'id_zamowienia': zam.id_zamowienia, 'sposob': 'Karta', 'status': 'Oczekiwanie na zaksięgowanie płatności', 'kwota': round(lista.suma, 2)})
        else:
            db.Platnosci.insert_one({'id_zamowienia': zam.id_zamowienia, 'sposob': 'Gotówka', 'status': 'Zapłacono','kwota': round(lista.suma, 2)})
        for i in range(len(koszyk_produkty)):
            koszyk_produkty[i].configure(text="")
        koszyk_cena.configure(text="")
        lista.lista_przedmiotow = []
        lista.suma = 0
        wiadomosc_o_zamowieniu = 'Pomyślnie złożono zamówienie. Twój numer zamówienia to: ' + str(zam.id_zamowienia)
        messagebox.showinfo(title='Zamówienie', message=wiadomosc_o_zamowieniu)
    else:
        messagebox.showerror(title='Błąd', message='Nie wybrano żadnego produktu')

def PowrotDoGlownej():
    zamow.grid(column=1, row=1)
    contact.grid(column=3, row=1)
    zlozenie_zamowienia.grid_forget()
    wroc_zamowienie.grid_forget()
    for i in range(len(lista.lista_przedmiotow)):
        koszyk_produkty[i].grid_forget()
    for i in range(len(koszyk_produkty)):
        koszyk_produkty[i].configure(text="")
    koszyk_cena.configure(text="")
    lista.lista_przedmiotow = []
    lista.suma = 0
    scrollbar.pack_forget()
    canvas.pack_forget()
    koszyk_cena.grid_forget()
    ClearTarget()

def Obsluga():
    messagebox.showinfo(title='Informacja', message='Kelner za chwilę podejdzie do stolika.')

okno_glowne = Tk()
okno_glowne.title("eCaterer")
okno_glowne.geometry('768x768')



###REJESTRACJA I LOGOWANIE###
flaga = 0
rejestracja = messagebox.askquestion ('Rejestracja','Czy chcesz się zarejestrować?')
if (rejestracja == 'yes'):
    ask_login = simpledialog.askstring("Rejestracja", "Podaj login", parent=okno_glowne)
    sprawdz_login = db.Dane.find_one({'login': ask_login})
    while (ask_login is None or len(ask_login) <= 5 or sprawdz_login != None):
        if (ask_login is None):
            ask_login = 'a'
        if (len(ask_login) <= 5):
            messagebox.showinfo(title='Rejestracja', message='Login musi składać się co najmniej z 6-ciu znaków')
        if (sprawdz_login != None):
            messagebox.showinfo(title='Rejestracja', message='Login jest już zajęty')
        ask_login = simpledialog.askstring("Rejestracja", "Podaj login", parent=okno_glowne)
        sprawdz_login = db.Dane.find_one({'login': ask_login})
    ask_haslo = simpledialog.askstring("Rejestracja", "Podaj hasło", parent=okno_glowne)
    while (ask_haslo is None or len(ask_haslo) <= 5 ):
        messagebox.showinfo(title='Rejestracja', message='Hasło musi składać się co najmniej z 6-ciu znaków')
        ask_haslo = simpledialog.askstring("Rejestracja", "Podaj hasło", parent=okno_glowne)
    ask_imie = None
    while (ask_imie is None):
        ask_imie = simpledialog.askstring("Rejestracja", "Podaj swoje imię", parent=okno_glowne)
        if (ask_imie is None):
            messagebox.showerror(title='Rejestracja', message='Pole nie może być puste')
    ask_nazwisko = None
    while (ask_nazwisko is None):
        ask_nazwisko = simpledialog.askstring("Rejestracja", "Podaj swoje nazwisko", parent=okno_glowne)
        if (ask_nazwisko is None):
            messagebox.showerror(title='Rejestracja', message='Pole nie może być puste')
    ask_plec = None
    while (ask_plec is None):
        ask_plec = simpledialog.askstring("Rejestracja", "Podaj swoją płeć", parent=okno_glowne)
        if (ask_plec.startswith("M") or ask_plec.startswith("m")):
            ask_plec = "M"
        elif (ask_plec.startswith("K") or ask_plec.startswith("k")):
            ask_plec = "K"
        else:
            messagebox.showerror(title='Rejestracja', message='Proszę wybrać płeć z istniejących opcji: Mężczyzna/Kobieta')
            ask_plec = None
    for x in db.Dane.find({}, {"id_uzytkownika": 1}):
        nowe_id_uz = x['id_uzytkownika'] + 1
    for x in db.Osoby.find({}, {"id_osoby": 1}):
        nowe_id_os = x['id_osoby'] + 1
    for x in db.Klienci.find({}, {"id_klienta": 1}):
        nowe_id_kl = x['id_klienta'] + 1
    db.Dane.insert_one({'id_uzytkownika': nowe_id_uz, 'login': ask_login, 'haslo': ask_haslo, 'typ': 'Klient'})
    db.Osoby.insert_one({'id_osoby': nowe_id_os, 'imie': ask_imie, 'nazwisko': ask_nazwisko, 'plec': ask_plec, 'id_uzytkownika': nowe_id_uz})
    db.Klienci.insert_one({'id_klienta':nowe_id_kl, 'id_osoby': nowe_id_os, 'app': True})
    messagebox.showinfo(title='Rejestracja',message='Rejestracja powiodła się, możesz teraz się zalogować.')
ask_login = simpledialog.askstring("Witaj","Wprowadź login", parent=okno_glowne)
sprawdzamy = db.Dane.find_one({'login': ask_login})
ask_haslo = simpledialog.askstring("Witaj","Wprowadź hasło", parent=okno_glowne)
while(sprawdzamy == None or ask_haslo != sprawdzamy['haslo'] and flaga == 0):
    messagebox.showerror(title="Błąd", message="Nieprawidłowy login lub hasło")
    ask_login = simpledialog.askstring("Witaj", "Wprowadź login", parent=okno_glowne)
    sprawdzamy = db.Dane.find_one({'login': ask_login})
    ask_haslo = simpledialog.askstring("Witaj", "Wprowadź hasło", parent=okno_glowne)
    if (sprawdzamy != None):
        if (ask_haslo == sprawdzamy['haslo']):
            flaga = 1
###KONIEC REJESTRACJI I LOGOWANIA###

ui = Frame(okno_glowne)
powitanie = Frame(okno_glowne)
data = Frame(okno_glowne)
zamowienie = Frame(okno_glowne)
edycja_zamowienia = Frame(okno_glowne)
#koszyk = Frame(okno_glowne)
suma_zam = Frame(okno_glowne)

scrollbar0 = ttk.Frame(okno_glowne)
canvas = Canvas(scrollbar0)
scrollbar = ttk.Scrollbar(scrollbar0,orient='vertical',command=canvas.yview)
koszyk_scrollable = ttk.Frame(canvas)
koszyk_scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0),window=koszyk_scrollable,anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)




powitanie.place(x=0,y=0)
ui.place(relheight=0.1, relwidth=0.4, relx=0.3, rely=0.0)
powitanie.place(relx=0.0,rely=0.0,height=20,width=100)
data.place(relheight=0.4, relwidth=0.4, relx=0.3, rely=0.5)
zamowienie.place(relheight=0.1, relwidth=0.2, relx=0.8, rely=0.0)
scrollbar0.place(relheight=0.4,relwidth=0.3,relx=0.6,rely=0.0)
suma_zam.place(relx=0.9,rely=0.0)
lista = KoszykC()
listaid = []
zamow = Button(ui, text = "Zamów", command=PrzejdzDoZamowienia)
contact = Button(ui, text = "Obsługa", command=Obsluga)
zlozenie_zamowienia = Button(ui, text="Złóż zamówienie", command=ZlozZamowienie)
wroc_zamowienie = Button(ui, text="Wróć", command=PowrotDoGlownej)



if(ask_login!=None):
    imie = Label(powitanie,text='Witaj, '+ ask_login)
else:
    imie = Label(powitanie, text='Witaj')


target = []
target2 = []
lista_buttonow = []
for x in db.Produkty.find({}, {"id_produktu": 1}):
    max_id_produktu = x['id_produktu']
for i in range(max_id_produktu):
    target.append(Label(data,text=""))
    target2.append(Button(data,text="Dodaj do koszyka",command=partial(DodajProdukt,i)))


koszyk_produkty = []
koszyk_cena = Label(suma_zam, text="")





imie.grid(column=1,row=0)
zamow.grid(column=1,row=1)
contact.grid(column=3,row=1)

for i in range(max_id_produktu):
    target[i].grid(column=1,row=i)

okno_glowne.mainloop()
