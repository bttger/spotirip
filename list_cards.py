import soundcard as sc

if __name__ == "__main__":
    cards = sc.all_microphones(include_loopback=True)

    id = 0
    for sc in cards:
        print(id, sc, "\n\t\tSOUNDCARD_ID:", sc.id)
        id += 1
