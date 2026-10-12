import random
import csv
import os
import imageio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import deque
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generare_labirint(dim):
    return [[[random.choice([0, 1]) for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]


def validare(lab, x, y, z):
    n = len(lab)
    return 0 <= x < n and 0 <= y < n and 0 <= z < n and lab[x][y][z] == 0


def drumuri(lab, x, y, z, end, drum, pas, sol, limita=1000):
    if len(sol) >= limita:
        return
    if (x, y, z) == end:
        sol.append(drum[:])
        return
    directii = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    for dx, dy, dz in directii:
        nx, ny, nz = x + dx, y + dy, z + dz
        if validare(lab, nx, ny, nz) and (nx, ny, nz) not in pas:
            pas.add((nx, ny, nz))
            drum.append((nx, ny, nz))
            drumuri(lab, nx, ny, nz, end, drum, pas, sol, limita)
            drum.pop()
            pas.remove((nx, ny, nz))


def drum_minim(lab, start, end):
    lista = deque([(start, [start])])
    drumuri = []
    nivele = {}
    lungime_min = None

    while lista:
        (x, y, z), drum = lista.popleft()
        lungime = len(drum)

        if lungime_min is not None and lungime > lungime_min:
            continue

        if (x, y, z) == end:
            if lungime_min is None:
                lungime_min = lungime
            if lungime == lungime_min:
                drumuri.append(drum)
            continue

        for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            nx, ny, nz = x + dx, y + dy, z + dz
            next_poz = (nx, ny, nz)

            if validare(lab, nx, ny, nz):
                if next_poz not in nivele or lungime + 1 <= nivele[next_poz]:
                    nivele[next_poz] = lungime + 1
                    lista.append((next_poz, drum + [next_poz]))
    return drumuri


def imagine(lab, drumuri, start, end, img=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for x in range(len(lab)):
        for y in range(len(lab)):
            for z in range(len(lab)):
                if lab[x][y][z] == 1:
                    ax.scatter(x, y, z, c='black', marker='s')

    colors = ['red', 'blue', 'green', 'purple', 'orange']
    for idx, drum in enumerate(drumuri):
        xs, ys, zs = zip(*drum)
        if idx == 0:
            ax.plot(xs, ys, zs, color='gold', linewidth=3, label=f"Best path (len={len(drum)})")
        else:
            ax.plot(xs, ys, zs, color=colors[idx % len(colors)], linewidth=1, label=f"Path {idx + 1} (len={len(drum)})")

    ax.scatter(*start, c='yellow', s=100, label='Start')
    ax.scatter(*end, c='cyan', s=100, label='End')
    ax.legend()

    if img is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img = f"labirint_{timestamp}.png"
    plt.savefig(img)
    plt.close(fig)


def generare_gif(lab, drum, start, end, gif_name="animatie_labirint.gif"):
    images = []
    for i in range(1, len(drum) + 1):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for x in range(len(lab)):
            for y in range(len(lab)):
                for z in range(len(lab)):
                    if lab[x][y][z] == 1:
                        ax.scatter(x, y, z, c='black', marker='s')

        xs, ys, zs = zip(*drum[:i])
        ax.plot(xs, ys, zs, color='gold', linewidth=3)
        ax.scatter(*start, c='yellow', s=100, label='Start')
        ax.scatter(*end, c='cyan', s=100, label='End')
        ax.legend()
        frame_name = f"_frame_{i:03d}.png"
        plt.savefig(frame_name)
        plt.close(fig)
        images.append(imageio.v2.imread(frame_name))

    imageio.mimsave(gif_name, images, duration=0.5, loop=0)
    for img in os.listdir():
        if img.startswith("_frame_") and img.endswith(".png"):
            os.remove(img)
    return gif_name


def html(drumuri, img="None", nume='raport_labirint_scurt.html'):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(nume, 'a') as f:
        f.write(f'<h2>Rulare din {timestamp}</h2>\n')
        if img:
            f.write(f'<p><b>Imagine:</b> <img src="{img}" width="500"></p>\n')
            gif_name = "animatie_labirint.gif"
            f.write(f'<p><b>Animatie:</b> <img src="{gif_name}" width="500"></p>\n')
        if drumuri:
            f.write('<p><b>Solutii gasite (maxim 3 afisate):</b></p>\n')
            for i, drum in enumerate(drumuri[:3]):
                f.write(f'<p>Solutia {i + 1}: {drum}</p>\n')
            if len(drumuri) > 3:
                f.write(f'<p><i>...si alte {len(drumuri) - 3} solutii</i></p>\n')
        f.write('<hr>\n')


def salvare_csv(drumuri, nume='Solutii_Labirint.csv', img=None):
    with open(nume, mode='a', newline='') as file:
        writer = csv.writer(file)
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([f'Data/Ora: {time}'])
        if img:
            writer.writerow([f'Imagine: {img}'])
        for drum in drumuri:
            writer.writerow([drum])
        writer.writerow([])


def pozitii(dim, lab):
    print("\nPozitii libere in labirint:")
    for x in range(dim):
        for y in range(dim):
            for z in range(dim):
                if lab[x][y][z] == 0:
                    print(f"({x}, {y}, {z})", end=' ')
    print('\n')


def main():
    dim = int(input("Introduceti dimensiunea labirintului: "))
    labirint = generare_labirint(dim)
    pozitii(dim, labirint)
    start = tuple(map(int, input("Coordonate start (x y z): ").split()))
    end = tuple(map(int, input("Coordonate final (x y z): ").split()))
    if not (validare(labirint, *start) and validare(labirint, *end)):
        print("Pozitii invalide! Start/End trebuie sa fie in celule libere (0).")
        return

    print("\nCautare pentru cele mai scurte drumuri...")
    drum = drum_minim(labirint, start, end)
    print(f"Numar drumuri scurte gasite: {len(drum)}")
    if not drum:
        print("Nu exista niciun drum intre start si end.")
        return

    print("\nCautare drumuri (maxim 1000)...")
    lista_drumuri = []
    drumuri(labirint, *start, end, [start], set([start]), lista_drumuri)
    print(f"Numar drumuri gasite: {len(lista_drumuri)}")
    salvare_csv(lista_drumuri)

    print("\nSe afiseaza labirintul si drumurile cele mai scurte...")
    imag = f"labirint_{start[0]}_{start[1]}_{start[2]}_to_{end[0]}_{end[1]}_{end[2]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    imagine(labirint, drum, start, end, img=imag)
    generare_gif(labirint, drum[0], start, end)
    salvare_csv(drum, img=imag)
    html(drum, img=imag)


if __name__ == '__main__':
    main()