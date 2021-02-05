#!/usr/bin/python

import math
import tkinter
import os
import PIL
from time import time as tm
from PIL import Image, ImageDraw, ImageTk, ImageFilter
from tkinter import ttk
print('Пожалуйста, подождите:\n  Программа запускается...')


VERSION = 'V 0.16.0'

www = 800  # Длина картинки
hhh = 640  # Ширина картинки

mxi = 4
big = 8

mxiop = 4

COL_M = 1
f_0 = 2

zoomc = 1.25

cx = www * 0.5
cy = hhh * 0.5
zoom = 0.75

width = int(www / big // 1)
height = int(hhh / big // 1)

r = 0.7885

zx0 = 0  # r * math.cos (180)
zy0 = 0  # r * math.sin (180)
zx1 = 4
zy1 = 4

fx = 0
fy = 0

progress = None
lpr = None
prg = 0

color1 = '#2222cc'
color2 = '#2288cc'
color3 = '#cc8822'

busy = False


def vopros(xx, yy, ww, hh):
    global zx0, zy0, zx1, zy1, mxi, cx, cy, big, zoom, f_0

    ax = ((xx - ww * 0.5) / zoom + ww * 0.5 - (cx / big)) * 4 / ww
    ay = ((yy - hh * 0.5) / zoom + hh * 0.5 - (cy / big)) * 4 / ww

    z = complex(zx0, zy0)  # complex (ax, ay)
    a = complex(ax, ay)  # complex (zx0, zy0)

    for q in range(min(mxi, mxiop)):
        if z != 0:
            try:
                z = z ** f_0 + a
                #z = complex (abs (z.real), abs (z.imag))
            except BaseException:
                print(z)
        else:
            z = a

        dist = abs(z.real) ** 2 + abs(z.imag) ** 2

        if dist > 4:
            return q
            # return q + (max (4 - dist, 0) / 2)

    return mxi

    '''dist = (abs (z.real) ** 2 + abs (z.imag) ** 2) ** 0.5

    return max (4 - dist, 0) / 2'''


def color(n, m):
    if COL_M == 0:
        q = 1

        s = 1 - n / m

        if s > 0:
            while True:
                f = 1 / (2 ** q)
                if s > f:
                    d = (s - f) / (1 / (2 ** (q - 1)) - f)
                    if q % 2 == 0:
                        a = 1 - d
                    else:
                        a = d
                    break
                q += 1
        else:
            a = 0

        q = round(a * 255)

        return (q, q, q)
    elif COL_M == 1:
        s = (n / m) ** 0.5

        C = 1 / 7
        M1 = 255
        M2 = 192
        M3 = 255

        if s <= C:
            return (M1, int((1 - (s / C)) * 255 // 1),
                    int((1 - (s / C)) * 255 // 1))
        elif s <= 2 * C:
            return (M1, int((s / C - 1) * M2 // 1), 0)
        elif s <= 3 * C:
            return (int((3 - (s / C)) * M1 // 1), M2, 0)
        elif s <= 4 * C:
            return (0, M2, int((s / C - 3) * M3 // 1))
        elif s <= 5 * C:
            return (0, int((5 - (s / C)) * M2 // 1), M3)
        elif s <= 6 * C:
            return (int((s / C - 5) * M1 // 1), 0, M3)
        elif s < 1:
            return (int((7 - (s / C)) * M1 // 1),
                    0, int((7 - (s / C)) * M3 // 1))
        else:
            return (0, 0, 0)


def save_image(image):
    if not ('rendered' in os.listdir('.')):
        os.mkdir('rendered')

    lst = os.listdir('rendered')

    if lst:
        image.save('rendered/' + str(int(int(sorted(lst)
                                             [-1][:4:])) + 1).rjust(4, '0') + '.png', 'PNG')
    else:
        image.save('rendered/0000.png', 'PNG')


def convert(imgg, biggx, biggy, w, h):
    a = imgg.resize((round(w * biggx), round(h * biggy)))
    b = a.filter(ImageFilter.GaussianBlur(radius=1))
    return b


def kartinka():
    global mxi, big, progress, prg, width, height

    imgg = Image.new('RGB', (width, height))
    pix = imgg.load()

    cx1 = cx
    cy1 = cy
    zoom1 = zoom
    busy1 = busy

    y = 0

    ntm = tm()

    colors = [color(q, mxi) for q in range(mxi + 1)]

    while y < int(height // 1):
        for x in range(int(width // 1)):
            pix[x, y] = colors[vopros(x, y, width, height)]

        y += 1

        if (cx1 != cx) or (cy1 != cy) or (zoom1 != zoom) or (busy1 != busy):
            cx1 = cx
            cy1 = cy
            zoom1 = zoom
            busy1 = busy

            mxi = 2 ** mxxi.get()
            big = 2 ** (0 - biig.get())

            width = int(www / big // 1)
            height = int(hhh / big // 1)

            y = 0

            imgg = Image.new('RGB', (width, height))
            pix = imgg.load()

        prg = y / height * 100

        progress['value'] = prg
        q = str(round(progress['value'], 3)).split('.')
        lpr['text'] = 'Генерация изображения...    ' + \
            q[0] + '.' + q[1].ljust(3, '0') + ' %'
        image_window.update()

    return imgg


def modify_img():
    global panel, width, height, zoom, image_window, cx, cy, lab, imgag, progress, lpr, mxi, busy

    busy = not (busy)

    lab['text'] = 'x: ' + str((width * 0.5 - (cx / big)) * 4 / width) + '\ny: ' + str(
        (height * 0.5 - (cy / big)) * 4 / height) + '\n\nzoom: ' + str(zoom) + '\n\nmxiop: ' + str(mxiop)

    if progress is not None:
        return None

    progress = ttk.Progressbar(image_window, length=300, value=0)
    progress.place(x=www + 25, y=hhh - 50)

    lpr = tkinter.Label(bg=color2, text='Генерация изображения...    0 %')
    lpr.place(x=www + 25, y=hhh - 71)

    imgag = kartinka()

    img2 = ImageTk.PhotoImage(convert(imgag, big, big, width, height))

    panel['image'] = img2
    panel.photo = img2

    lpr.destroy()

    progress.destroy()
    progress = None


def set_zoom(event):
    global zoom

    if event.delta > 0:
        zoom *= zoomc ** (event.delta / 120)
    else:
        zoom /= zoomc ** (event.delta / -120)

    modify_img()


def set_center(event):
    global cx, cy

    cx += (event.x - fx) / zoom
    cy += (event.y - fy) / zoom

    modify_img()


def set_flag(event):
    global fx, fy

    if event.num == 1:
        fx = event.x
        fy = event.y


def set_mxi(event):
    global mxi, mxiop, s1

    if progress is None:
        mxi = 2 ** mxxi.get()
        mxiop = mxi

    s1['text'] = str(2 ** mxxi.get())


def set_big(event):
    global big, s2, width, height

    bb = 2 ** (0 - biig.get())

    if progress is None:
        big = bb
        width = int(www / big // 1)
        height = int(hhh / big // 1)

    s2['text'] = str(round(www / bb)) + ' x ' + str(round(hhh / bb))


def paint_color():
    imgg = Image.new('RGB', (256, 1))
    pix = imgg.load()

    for q in range(256):
        pix[q, 0] = color(q, 255)

    return convert(imgg, 1, 30, 256, 1)


def matem(st):
    b1 = ''
    b2 = ''

    d = st[0]

    mod = 0

    n = 1

    for w in range(2, len(st)):
        if mod % 10 == 0:
            if st[w] == '=':
                mod += 1
            else:
                if n == 1:
                    b1 = matem(st[w::])
                    n += 1
                    mod += 2
                else:
                    b2 = matem(st[w::])
                    break
        elif mod % 10 == 1:
            if st[w] == ',':
                b1 = float(b1)
                n += 1
                mod -= 1
            elif st[w] == ')':
                b2 = float(b2)
                break
            else:
                if n == 1:
                    b1 += st[w]
                else:
                    b2 += st[w]
        elif mod == 2:
            if st[w] == ',':
                mod -= 2
            elif st[w] == '(':
                mod += 10
            elif st[w] == ')':
                mod -= 10

            if mod < 0:
                break

    b2 = float(b2)

    if d == '+':
        return b1 + b2
    elif d == '-':
        return b1 - b2
    elif d == '*':
        return b1 * b2
    elif d == '/':
        return b1 / b2
    elif d == '^':
        return b1 ** b2


def video(vid):
    global cx, cy, zoom, f_0, r, zx0, zy0, mxiop

    vidd = vid

    for q in range(len(vidd)):
        bufer = []
        b2 = ''
        mod = 0

        for w in range(len(vidd[q])):
            if mod == 0:
                if vidd[q][w] == '=':
                    mod = 1
                else:
                    bufer.append(matem(vidd[q][w::]))
                    mod = 2
            elif mod == 1:
                if vidd[q][w] == ' ':
                    bufer.append(float(b2))
                    b2 = ''
                    mod = 0
                else:
                    b2 += vidd[q][w]
            elif mod == 2:
                if vidd[q][w] == ' ':
                    mod = 0

        if len(bufer) < 6:
            bufer.append(float(b2))

        vidd[q] = bufer

    progress_v = ttk.Progressbar(image_window, length=300, value=0)
    progress_v.place(x=www + 25, y=hhh - 100)

    lpr_v = tkinter.Label(
        bg=color2, text='Генерация видео...    0 %    ( 0 / ' + str(len(vidd)) + ' )')
    lpr_v.place(x=www + 25, y=hhh - 121)

    for q in range(len(vidd)):
        cx = ((width * 0.5) - (vidd[q][0] * width / 4)) * big
        cy = ((height * 0.5) - (vidd[q][1] * height / 4)) * big
        zoom = vidd[q][2]
        f_0 = vidd[q][3]
        r = vidd[q][4]
        mxiop = int(vidd[q][5])

        zx0 = r * math.cos(180)
        zy0 = r * math.sin(180)

        modify_img()
        save_image(imgag)

        prg_v = (q + 1) / len(vidd) * 100

        progress_v['value'] = prg_v
        qq = str(round(progress_v['value'], 3)).split('.')
        lpr_v['text'] = 'Генерация видео...    ' + qq[0] + '.' + \
            qq[1].ljust(3, '0') + '%    ( ' + str(q + 1) + ' / ' + str(len(vidd)) + ' )'

        image_window.update()

    lpr_v.destroy()
    progress_v.destroy()

    image_window.update()


image_window = tkinter.Tk()
image_window.title('Фрактал Мандельброта    ' + VERSION + '    Vitmalok')
image_window.geometry(str(www + 352) + 'x' + str(hhh + 4))
image_window.resizable(False, False)
image_window['bg'] = color2

mxxi = tkinter.IntVar()
biig = tkinter.IntVar()

imgag = Image.new('RGB', (int(width // 1) * big, int(height // 1) * big))

img = ImageTk.PhotoImage(imgag)

panel = tkinter.Label(image_window, image=img, bg=color1)
panel.place(x=0, y=0)

imama = ImageTk.PhotoImage(paint_color())

colorbar = tkinter.Label(image_window, image=imama, bg=color1)
colorbar.place(x=www + 40, y=330)

scale1 = tkinter.Scale(
    image_window,
    orient=tkinter.HORIZONTAL,
    length=230,
    from_=0,
    to=12,
    bg=color1,
    variable=mxxi,
    activebackground=color1,
    command=set_mxi)
scale1.set(2)
scale1.place(x=www + 40, y=400)

s1 = tkinter.Label(image_window, text=str(mxi), bg=color2)
s1.place(x=www + 280, y=420)

nnn1 = tkinter.Label(
    image_window,
    width=39,
    bg=color2,
    text='Количество итераций:',
    anchor='w')
nnn1.place(x=www + 40, y=400)

scale2 = tkinter.Scale(
    image_window,
    orient=tkinter.HORIZONTAL,
    length=230,
    from_=-4,
    to=2,
    bg=color1,
    variable=biig,
    activebackground=color1,
    command=set_big)
scale2.set(-3)
scale2.place(x=www + 40, y=450)

s2 = tkinter.Label(image_window, text=str(mxi), bg=color2)
s2.place(x=www + 280, y=470)

nnn2 = tkinter.Label(
    image_window,
    width=39,
    bg=color2,
    text='Разрешение:',
    anchor='w')
nnn2.place(x=www + 40, y=450)

lab = tkinter.Label(image_window, bg=color2, text='x: ' +
                    str((width *
                         0.5 -
                         (cx /
                          big)) *
                        4 /
                        width) +
                    '\ny: ' +
                    str((height *
                         0.5 -
                         (cy /
                          big)) *
                        4 /
                        height) +
                    '\n\nzoom: ' +
                    str(zoom), font='Courier 13', just='left')
lab.place(x=www + 40, y=20)

svbt = tkinter.Button(
    image_window,
    text='Сохранить изображение',
    height=2,
    width=38,
    bg=color1,
    activebackground=color1,
    command=lambda: save_image(imgag))
svbt.place(x=www + 40, y=160)

upbt = tkinter.Button(
    image_window,
    text='Обновить изображение',
    height=2,
    width=38,
    bg=color1,
    activebackground=color1,
    command=modify_img)
upbt.place(x=www + 40, y=210)

if 'video.txt' in os.listdir('.'):
    with open('video.txt', 'r') as f:
        zzz = f.readlines()

    for q in range(len(zzz)):
        zzz[q] = zzz[q].strip()

    if zzz[0] == 'True':
        qqq = zzz[1].split(' ; ')

        ver1 = list(map(int, VERSION[2::].split('.')))

        flag = True

        for q in range(len(qqq)):
            eee = qqq[q].split(' ')

            ver2 = list(map(int, eee[1].split('.')))

            if eee[0] == '==':
                if ver1 != ver2:
                    flag = False
                    break
            elif eee[0] == '!=':
                if ver1 == ver2:
                    flag = False
                    break
            elif eee[0] == '>':
                if ver1 == ver2:
                    flag = False
                    break
                f2 = True
                for w in range(min(len(ver1), len(ver2))):
                    if ver1[w] < ver2[w]:
                        flag = False
                        break
                    elif ver1[w] != ver2[w]:
                        f2 = False
                if (len(ver1) < len(ver2)) and f2:
                    flag = False
                    break
            elif eee[0] == '<':
                if ver1 == ver2:
                    flag = False
                    break
                f2 = True
                for w in range(min(len(ver1), len(ver2))):
                    if ver1[w] > ver2[w]:
                        flag = False
                        break
                    elif ver1[w] != ver2[w]:
                        f2 = False
                if (len(ver1) > len(ver2)) and f2:
                    flag = False
                    break
            elif eee[0] == '>=':
                f2 = True
                for w in range(min(len(ver1), len(ver2))):
                    if ver1[w] < ver2[w]:
                        flag = False
                        break
                    elif ver1[w] != ver2[w]:
                        f2 = False
                if (len(ver1) < len(ver2)) and f2:
                    flag = False
                    break
            elif eee[0] == '<=':
                f2 = True
                for w in range(min(len(ver1), len(ver2))):
                    if ver1[w] > ver2[w]:
                        flag = False
                        break
                    elif ver1[w] != ver2[w]:
                        f2 = False
                if (len(ver1) > len(ver2)) and f2:
                    flag = False
                    break

        if flag:
            vibt = tkinter.Button(image_window,
                                  text='Создать видео',
                                  height=2,
                                  width=38,
                                  bg=color3,
                                  activebackground=color3,
                                  command=lambda: video(zzz[3::]))
            vibt.place(x=www + 40, y=260)

            image_window.title(
                'Фрактал Мандельброта    ' +
                VERSION +
                '    Vitmalok    - Режим видео')

panel.bind('<MouseWheel>', set_zoom)
panel.bind('<ButtonRelease-1>', set_center)
panel.bind('<Button-1>', set_flag)

image_window.after(200, modify_img)

image_window.mainloop()
