import csv
import random
import math

def tavolsag(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def pontszam_kalkulator(gon_x, gon_y, kar_x, kar_y, eger_x, eger_y):
    lepesek = {
        0: (0, -1), # Fel
        1: (0, 1),  # Le
        2: (-1, 0), # Balra
        3: (1, 0)   # Jobbra
    }

    jatekus_suly = 1.5 # A játékos követése fontosabb
    eger_suly = 0 #1.0  # Az egér elkerülése kevésbé

    legjobb_lepes = -1
    legjobb_pontszam = -float('inf')

    eredeti_tav_jatekos = tavolsag(gon_x, gon_y, kar_x, kar_y)
    eredeti_tav_eger = tavolsag(gon_x, gon_y, eger_x, eger_y)

    #legjobb lpés keresése
    for lepes, (dx, dy) in lepesek.items():
        uj_gon_x, uj_gon_y = gon_x + dx, gon_y + dy

        # Játékos pontszám: A távolság csökkenése a jó
        uj_tav_jatekos = tavolsag(uj_gon_x, uj_gon_y, kar_x, kar_y)
        jatekos_pont = eredeti_tav_jatekos - uj_tav_jatekos

        # Egér pontszám: A távolság növekedése a jó
        uj_tav_eger = tavolsag(uj_gon_x, uj_gon_y, eger_x, eger_y)
        eger_pont = uj_tav_eger - eredeti_tav_eger
        
        # Végső pontszám súlyozással
        vegso_pontszam = (jatekos_pont * jatekus_suly) + (eger_pont * eger_suly)
        
        if vegso_pontszam > legjobb_pontszam:
            legjobb_pontszam = vegso_pontszam
            legjobb_lepes = lepes
    return legjobb_lepes


with open("adatok.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['jatekos_dx', 'jatekos_dy', 'eger_dx', 'eger_dy', 'kimenet'])

    for i in range(10000):
        gon_x, gon_y = random.uniform(-50, 50), random.uniform(-50, 50)
        kar_x, kar_y = random.uniform(-50, 50), random.uniform(-50, 50)
        mouse_x, mouse_y = random.uniform(-50, 50), random.uniform(-50, 50)

        #if gon_x == kar_x and gon_y == kar_y: continue
        #if gon_x == mouse_x and gon_y == mouse_y: continue


        legjobb_lepes = pontszam_kalkulator(gon_x, gon_y, kar_x, kar_y, mouse_x, mouse_y)

        # Adatok mentése
        játékos_dx = kar_x - gon_x
        játékos_dy = kar_y - gon_y
        egér_dx = mouse_x - gon_x
        egér_dy = mouse_y - gon_y
        
        writer.writerow([játékos_dx, játékos_dy, egér_dx, egér_dy, legjobb_lepes])
