import csv
from datetime import datetime
import matplotlib.pyplot as plt



# Leser inn data fra CSV-fil


def til_float(verdi):
    if verdi == "" or verdi == "-":
        return None

    return float(verdi.replace(",", "."))


def les_fil(filnavn):
    data = []

    with open(filnavn, encoding="utf-8") as fil:
        csv_fil = csv.DictReader(fil, delimiter=";")

        for rad in csv_fil:

            ny_rad = {
                "dato": datetime.strptime(rad["Tid(norsk normaltid)"], "%d.%m.%Y"),
                "middeltemp": til_float(rad["Middeltemperatur"]),
                "maks_temp": til_float(rad["Maksimumstemperatur"]),
                "nedbor": til_float(rad["Nedbør (døgn)"]),
                "vind": til_float(rad["Høyeste middelvind (1 t)"]),
                "snodybde": til_float(rad["Snødybde"])
            }

            data.append(ny_rad)

    return data



# d) Plot værdata for valgt år


def plott_ar(data, aar):

    datoer = []
    sno = []
    nedbor = []
    temperatur = []
    vind = []

    for rad in data:

        if rad["dato"].year == aar:

            datoer.append(rad["dato"])
            sno.append(rad["snodybde"] if rad["snodybde"] is not None else 0)
            nedbor.append(rad["nedbor"] if rad["nedbor"] is not None else 0)
            temperatur.append(rad["middeltemp"])
            vind.append(rad["vind"])

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(datoer, sno)
    plt.title("Snødybde")

    plt.subplot(2, 2, 2)
    plt.plot(datoer, nedbor)
    plt.title("Nedbør")

    plt.subplot(2, 2, 3)
    plt.plot(datoer, temperatur)
    plt.title("Middeltemperatur")

    plt.subplot(2, 2, 4)
    plt.plot(datoer, vind)
    plt.title("Høyeste middelvind")

    plt.tight_layout()
    plt.show()



# e) Antall skidager


def antall_skidager(data, aar):

    teller = 0

    for rad in data:

        dato = rad["dato"]
        sno = rad["snodybde"]

        if sno is None:
            continue

        if (
            (dato.year == aar - 1 and dato.month >= 11)
            or
            (dato.year == aar and dato.month <= 5)
        ):

            if sno >= 20:
                teller += 1

    return teller



# f) Plantevekst


def plantevekst(data, aar):

    vekst = 0

    for rad in data:

        if rad["dato"].year == aar:

            temp = rad["middeltemp"]

            if temp is not None and temp > 5:
                vekst += temp - 5

    return round(vekst, 2)



# g) Lengste tørkeperiode


def lengste_torrperiode(data):

    maks_lengde = 0
    startdato = None
    sluttdato = None

    lengde = 0
    start = None

    for rad in data:

        nedbor = rad["nedbor"]

        if nedbor == 0:

            if lengde == 0:
                start = rad["dato"]

            lengde += 1

            if lengde > maks_lengde:
                maks_lengde = lengde
                startdato = start
                sluttdato = rad["dato"]

        else:
            lengde = 0

    return maks_lengde, startdato, sluttdato

# h) Sommerdager, høysommerdager, tropedager


def sommerdager(data, aar):

    sommer = 0
    hoysommer = 0
    trope = 0

    for rad in data:

        if rad["dato"].year == aar:

            maks = rad["maks_temp"]

            if maks is None:
                continue

            if maks > 20:
                sommer += 1

            if maks > 25:
                hoysommer += 1

            if maks > 30:
                trope += 1

    return sommer, hoysommer, trope




def meny():

    data = les_fil("sinnes_2014_2025_med_makstemperatur.csv")

    while True:

        print("\n----- MENY -----")
        print("1 - Plot værdata")
        print("2 - Antall skidager")
        print("3 - Plantevekst")
        print("4 - Lengste tørkeperiode")
        print("5 - Sommerdager")
        print("0 - Avslutt")

        valg = input("Velg: ")

        if valg == "1":

            aar = int(input("År: "))
            plott_ar(data, aar)

        elif valg == "2":

            aar = int(input("År: "))
            print("Antall skidager:", antall_skidager(data, aar))

        elif valg == "3":

            aar = int(input("År: "))
            print("Plantevekst:", plantevekst(data, aar))

        elif valg == "4":

            lengde, start, slutt = lengste_torrperiode(data)

            print("\nLengste tørkeperiode")
            print("Lengde:", lengde, "dager")
            print("Fra:", start.date())
            print("Til:", slutt.date())

        elif valg == "5":

            aar = int(input("År: ")

            sommer, hoysommer, trope = sommerdager(data, aar)

            print("Sommerdager:", sommer)
            print("Høysommerdager:", hoysommer)
            print("Tropedager:", trope)

        elif valg == "0":

            print("Program avsluttes")
            break

        else:
            print("Ugyldig valg")


meny()
