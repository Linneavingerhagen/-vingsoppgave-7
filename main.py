import csv
from datetime import datetime
import matplotlib.pyplot as plt


# -------------------------------------------------
# LESER DATA FRA CSV-FILEN
# -------------------------------------------------

def les_data(filnavn):
    data = []

    with open(filnavn, "r", encoding="utf-8-sig") as fil:
        leser = csv.DictReader(fil, delimiter=";")

        for rad in leser:

            # Hopper over raden med informasjon om datasettet
            if rad["Stasjon"] == "":
                continue

            # Dato
            dato = datetime.strptime(
                rad["Tid(norsk normaltid)"],
                "%d.%m.%Y"
            )

            # Middeltemperatur
            if rad["Middeltemperatur (døgn)"] == "-":
                middeltemp = None
            else:
                middeltemp = float(
                    rad["Middeltemperatur (døgn)"].replace(",", ".")
                )

            # Nedbør
            if rad["Nedbør (døgn)"] == "-":
                nedbor = None
            else:
                nedbor = float(
                    rad["Nedbør (døgn)"].replace(",", ".")
                )

            # Vind
            if rad["Høyeste middelvind (døgn)"] == "-":
                vind = None
            else:
                vind = float(
                    rad["Høyeste middelvind (døgn)"].replace(",", ".")
                )

            # Snødybde
            if rad["Snødybde"] == "-":
                snodybde = None
            else:
                snodybde = float(
                    rad["Snødybde"].replace(",", ".")
                )

            data.append({
                "dato": dato,
                "middeltemp": middeltemp,
                "nedbor": nedbor,
                "vind": vind,
                "snodybde": snodybde
            })

    # Sorterer data etter dato
    data.sort(key=lambda rad: rad["dato"])

    return data


# -------------------------------------------------
# OPPGAVE D - PLOTTING
# -------------------------------------------------

def plott_ar(data, aar):

    datoer = []
    sno = []
    nedbor = []
    temperatur = []
    vind = []

    for rad in data:

        dato = rad["dato"]

        if dato.year == aar:

            datoer.append(dato)
            sno.append(rad["snodybde"])
            nedbor.append(rad["nedbor"])
            temperatur.append(rad["middeltemp"])
            vind.append(rad["vind"])

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(datoer, sno)
    plt.title("Snødybde")
    plt.xlabel("Dato")
    plt.ylabel("Snødybde [cm]")

    plt.subplot(2, 2, 2)
    plt.plot(datoer, nedbor)
    plt.title("Nedbør")
    plt.xlabel("Dato")
    plt.ylabel("Nedbør [mm]")

    plt.subplot(2, 2, 3)
    plt.plot(datoer, temperatur)
    plt.title("Middeltemperatur")
    plt.xlabel("Dato")
    plt.ylabel("Temperatur [°C]")

    plt.subplot(2, 2, 4)
    plt.plot(datoer, vind)
    plt.title("Høyeste middelvind")
    plt.xlabel("Dato")
    plt.ylabel("Vind [m/s]")

    plt.tight_layout()
    plt.show()


# -------------------------------------------------
# OPPGAVE E - ANTALL SKIDAGER
# -------------------------------------------------

def antall_skidager(data, aar):

    teller = 0

    for rad in data:

        dato = rad["dato"]
        sno = rad["snodybde"]

        if sno is None:
            continue

        # Skisesong:
        # november og desember året før
        # januar til mai i det aktuelle året

        gyldig_periode = (
            (dato.year == aar - 1 and dato.month >= 11)
            or
            (dato.year == aar and dato.month <= 5)
        )

        if gyldig_periode and sno >= 20:
            teller += 1

    return teller


# -------------------------------------------------
# OPPGAVE F - PLANTEVEKST
# -------------------------------------------------

def plantevekst(data, aar):

    total_vekst = 0

    for rad in data:

        dato = rad["dato"]
        temp = rad["middeltemp"]

        if dato.year == aar and temp is not None:

            # Planten vokser bare når temperaturen
            # er høyere enn 5 grader

            if temp > 5:
                total_vekst += temp - 5

    return total_vekst


# -------------------------------------------------
# OPPGAVE G - LENGSTE TØRRPERIODE
# -------------------------------------------------

def lengste_torrperiode(data):

    maks_lengde = 0
    start_maks = None
    slutt_maks = None

    lengde = 0
    start = None

    for rad in data:

        nedbor = rad["nedbor"]

        if nedbor == 0:

            # Starter en ny tørrperiode
            if lengde == 0:
                start = rad["dato"]

            lengde += 1

            # Sjekker om dette er den lengste perioden
            if lengde > maks_lengde:

                maks_lengde = lengde
                start_maks = start
                slutt_maks = rad["dato"]

        else:

            # Tørrperioden er avsluttet
            lengde = 0

    return maks_lengde, start_maks, slutt_maks


# -------------------------------------------------
# OPPGAVE H
# -------------------------------------------------

def sommerdager(data, aar):

    print()
    print("Oppgave h kan ikke beregnes korrekt.")
    print("CSV-filen inneholder middeltemperatur,")
    print("men ikke maksimaltemperatur.")
    print("Sommerdager krever maksimaltemperatur.")
    
    return None, None, None


# -------------------------------------------------
# HOVEDPROGRAM
# -------------------------------------------------

# Navnet på CSV-filen
filnavn = "sinnes_2014_2025 2.csv"

# Leser inn data
data = les_data(filnavn)


# Brukeren skriver inn år
aar = int(input("Skriv inn årstall: "))


# -------------------------------------------------
# OPPGAVE D
# -------------------------------------------------

print()
print("OPPGAVE D")
print("Plotter værdata for", aar)

plott_ar(data, aar)


# -------------------------------------------------
# OPPGAVE E
# -------------------------------------------------

skidager = antall_skidager(data, aar)

print()
print("OPPGAVE E")
print("Antall skidager i skisesongen:", skidager)


# -------------------------------------------------
# OPPGAVE F
# -------------------------------------------------

vekst = plantevekst(data, aar)

print()
print("OPPGAVE F")
print("Total plantevekst:", vekst)


# -------------------------------------------------
# OPPGAVE G
# -------------------------------------------------

lengde, startdato, sluttdato = lengste_torrperiode(data)

print()
print("OPPGAVE G")
print("Lengste tørre periode:", lengde, "dager")
print("Startdato:", startdato.strftime("%d.%m.%Y"))
print("Sluttdato:", sluttdato.strftime("%d.%m.%Y"))


# -------------------------------------------------
# OPPGAVE H
# -------------------------------------------------

sommer, hoysommer, trope = sommerdager(data, aar)
