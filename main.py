import tkinter as tk
from tkinter.filedialog import *
from main_rotsize import *
from main_collage import *
from os import path
from PIL import ImageTk, Image


def on_exit(cls, l_p_name):
    if l_p_name is not None and l_p_name.split('/')[-1] == MainEffect.backup_dir.split('/')[-1]:
        if messagebox.askokcancel('Закрити програму?', 'Хочете закрити програму?\nУ вас є незбережені фото!'):
            cls.destroy()
            #open('log.txt', 'w').close()
    else:
        if messagebox.askokcancel('Закрити програму?', 'Хочете закрити програму?'):
            cls.destroy()
            #open('log.txt', 'w').close()


def onOpen(cls):
    f_types = [('JPG файли', '*.jpg'), ('PNG файли', '*.png')]
    name = askopenfilename(filetypes=f_types)
    if not (name is None or name == ''):
        file = open('log.txt', 'w')
        file.write(name)
        file.close()
        cls.destroy()
        Main_window().main()


def Read_file():
    if path.exists('log.txt'):
        line_val = ''
        file = open('log.txt', 'r')
        for line in file.readlines():
            line_val += line
        file.close()
        if len(line_val) > 0:
            return line_val
        else:
            return None
    else:
        return None


def save_photo(photo_name):
    if photo_name is not None:
        name = photo_name.split('/')
        image = cv2.imread(photo_name)
        dst = askdirectory()
        if dst[-1] == '/':
            dst += name[-1]
        else:
            dst += '/' + name[-1]
        cv2.imwrite(dst, image)
        messagebox.showinfo('Успіх!', f'Ваше фото було збережено як {name[-1]}.\nЗа шляхом {dst}')
    else:
        messagebox.showinfo('Помилка!', 'Спочатку виберіть фото!')


class Main_window:
    def __init__(self):
        self.root = tk.Tk()
        self.app_size = [1366, 768]

    @staticmethod
    def detect_action(action, img_name, cls):
        if img_name is None:
            messagebox.showinfo('Помилка!', 'Спочатку виберіть фото!')
            # cls.destroy()
            # main()
        else:
            img = cv2.imread(img_name)
            MRS, MF, FD, CL = Main_Rot_size(img), MainEffect(img, cls), \
                              FaceDetection(img), Collage(img)

            if action == 'Розпізнавання обличь':
                FD.Face_detection()

            # визов методів із класу Main_Rot_size
            elif action == 'Зменшити зображення':
                title = 'Зміна розміру зображення!'
                text = 'Введіть % від початковго розміру!'
                InputWindow(title, text, img).resize_image()
            elif action == 'Повернути фото':
                title = 'Повернення зображення!'
                text = 'Введіть кут повороту:'
                InputWindow(title, text, img).resize_image()

            # визов методів із класу MainEffect
            elif action == 'Градація сірого':
                MF.Gray()
            elif action == 'Інверсія білого':
                MF.White()
            elif action == 'Червоний канал':
                MF.Red_chanel()
            elif action == 'Зелений канал':
                MF.Green_chanel()
            elif action == 'Синій канал':
                MF.Blue_chanel()
            elif action == 'Розмити фото':
                MF.Blured_photo()

            elif action == 'Склеїти вертикально':
                CL.Collage_vertical()
            elif action == 'Склеїти горизонтально':
                CL.Collage_horizontal()
            elif action == 'Накласти зображення':
                photo_concl()
            else:
                messagebox.showinfo('Помилка!', 'Немає заданої операції!\nПеревірте код програми!')

    def main(self):
        self.root["bg"] = "white"
        self.root.title('Обробка зображень')
        self.root.resizable(False, False)
        #root.wm_attributes('-topmost', True)
        #self.root.iconbitmap("my_icon.ico")
        self.root.geometry(f'{self.app_size[0]}x{self.app_size[1]}')
        self.root.rowconfigure(0, minsize=800, weight=1)
        self.root.columnconfigure(1, minsize=800, weight=1)

        buttons = ('Розпізнавання обличь', 'Зменшити зображення', 'Повернути фото',
                   'Градація сірого', 'Інверсія білого', 'Розмити фото',
                   'Червоний канал', 'Зелений канал', 'Синій канал',
                   'Склеїти вертикально', 'Склеїти горизонтально', 'Накласти зображення')

        fr_buttons = tk.Frame(self.root, relief=tk.RAISED, bd=4)
        for i in range(len(buttons)):
            button = Button(fr_buttons, text=buttons[i], command=lambda row=i,
                            col=0: self.detect_action(buttons[row], show_photo, self.root),
                            width=25, height=1)
            button.grid(row=i, column=0, padx=5, pady=5, sticky="ew")

        fr_buttons.grid(row=0, column=0, sticky="ns")

        show_photo = Read_file()

        if show_photo is not None:
            photo = ImageTk.PhotoImage(Image.open(show_photo))
            WindowImageShow(show_photo, self.root, self.app_size, photo).ShowImageUI()

        self.root.protocol("WM_DELETE_WINDOW", lambda: on_exit(self.root, show_photo))
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Відкрити", command=lambda: onOpen(self.root))
        fileMenu.add_command(label="Зберегти як...", command=lambda: save_photo(show_photo))
        menubar.add_cascade(label="Файл", menu=fileMenu)

        fileMenu1 = Menu(menubar)
        fileMenu1.add_command(label="Відмінити", command=lambda: onOpen(self.root))
        menubar.add_cascade(label="Розширені", menu=fileMenu1)

        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.mainloop()


class WindowImageShow:
    def __init__(self, photo_name, p_class, window_size, photo):
        self.photo_name = photo_name
        self.p_class = p_class
        self.window_size = window_size
        self.photo = photo

    @staticmethod
    def calculate_params(parameters):
        list_2p = []
        for i in parameters:
            list_2p.append(round(i / 2))
        x = list_2p[0] - list_2p[2]
        y = list_2p[1] - list_2p[3]

        return x, y

    def ShowImageUI(self):
        img1 = cv2.imread(self.photo_name)
        h, w, d = img1.shape
        center_coord = [self.window_size[0] - 230, self.window_size[1], w, h]
        x, y = self.calculate_params(center_coord)

        canvas = Canvas(master=self.p_class)
        canvas.place(x=x + 230, y=y, height=h, width=w)
        canvas.create_image(0, 0, anchor='nw', image=self.photo)


class MainEffect:
    backup_dir = 'redacted_photos/storelogappbackup.jpg'

    def __init__(self, image, cls):
        self.image = image
        self.cls = cls

    def rew_img_file(self):
        file = open('log.txt', 'w')
        file.write(MainEffect.backup_dir)
        file.close()
        self.cls.destroy()
        Main_window().main()

    def Gray(self):
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(MainEffect.backup_dir, gray_image)
        self.rew_img_file()

    def White(self):
        ret, threshold_image = cv2.threshold(self.image, 127, 255, 0)
        cv2.imwrite(MainEffect.backup_dir, threshold_image)
        self.rew_img_file()

    def Blured_photo(self):
        blurred = cv2.GaussianBlur(self.image, (51, 51), 0)
        cv2.imwrite(MainEffect.backup_dir, blurred)
        self.rew_img_file()

    def Red_chanel(self):
        b, g, r = cv2.split(self.image)
        pic = np.zeros(np.shape(self.image), np.uint8)
        pic[:, :, 2] = r
        cv2.imwrite(MainEffect.backup_dir, pic)
        self.rew_img_file()

    def Green_chanel(self):
        b, g, r = cv2.split(self.image)
        pic = np.zeros(np.shape(self.image), np.uint8)
        pic[:, :, 1] = g
        cv2.imwrite(MainEffect.backup_dir, pic)
        self.rew_img_file()

    def Blue_chanel(self):
        b, g, r = cv2.split(self.image)
        pic = np.zeros(np.shape(self.image), np.uint8)
        pic[:, :, 0] = b
        cv2.imwrite(MainEffect.backup_dir, pic)
        self.rew_img_file()


if __name__ == "__main__":
    Main_window().main()