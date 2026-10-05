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
def antall_skidager(data, aar):
    teller = 0

    for rad in data:
        dato = rad["dato"]
        sno = rad["snodybde"]

        if sno is None:
            continue

        gyldig_periode = (
            (dato.year == aar - 1 and dato.month >= 11)
            or
            (dato.year == aar and dato.month <= 5)
        )

        if gyldig_periode and sno >= 20:
            teller += 1

    return teller
def plantevekst(data, aar):
    total_vekst = 0

    for rad in data:
        dato = rad["dato"]
        temp = rad["middeltemp"]

        if dato.year == aar and temp is not None:

            if temp > 5:
                total_vekst += temp - 5

    return total_vekst
def lengste_torrperiode(data):
    maks_lengde = 0
    start_maks = None
    slutt_maks = None

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
                start_maks = start
                slutt_maks = rad["dato"]

        else:
            lengde = 0

    return maks_lengde, start_maks, slutt_maks
def sommerdager(data, aar):
    sommer = 0
    hoysommer = 0
    tropedager = 0

    for rad in data:
        dato = rad["dato"]
        maks = rad["maks_temp"]

        if dato.year == aar and maks is not None:

            if maks > 20:
                sommer += 1

            if maks > 25:
                hoysommer += 1

            if maks > 30:
                tropedager += 1

    return sommer, hoysommer, tropedager

