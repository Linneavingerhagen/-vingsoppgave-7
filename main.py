#hei
print("hei")
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
