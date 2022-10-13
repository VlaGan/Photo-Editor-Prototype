from tkinter import *
from tkinter import messagebox
import cv2


class Main_Rot_size:
    def __init__(self, image):
        self.image = image

    def img_rotation(self, value):
        (h, w, d) = self.image.shape
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, value, 1.0)
        rotated = cv2.warpAffine(self.image, M, (w, h))
        cv2.imshow("Rotation.", rotated)
        cv2.waitKey(0)
        cv2.imwrite("D:\changed_images\_rotated_image.jpg", rotated)

    def img_size(self, value):
        width = int(self.image.shape[1] * value / 100)
        height = int(self.image.shape[0] * value / 100)
        dim = (width, height)
        resized = cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("Changed size.", resized)
        cv2.waitKey(0)
        cv2.imwrite("D:\changed_images\_change_size_image.jpg", resized)

    def Text_on_photo(self):
        location = "D:\changed_images\_text.jpg"
        output = self.image.copy()
        cv2.putText(output, "TEXT", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 2)
        cv2.imshow("Text.", output)
        cv2.waitKey(0)
        cv2.imwrite(location, output)


class InputWindow:
    def __init__(self, title, text, image):
        self.title = title
        self.text = text
        self.image = image

    def resize_image(self):
        def read_input():
            value = text_val.get()
            if value.isnumeric():
                menu_rot.destroy()
                if self.title == 'Повернення зображення!':
                    Main_Rot_size(self.image).img_rotation(int(value))
                elif self.title == 'Зміна розміру зображення!':
                    Main_Rot_size(self.image).img_size(int(value))
            else:
                if len(value) < 1:
                    messagebox.showinfo('Помилка!', 'Ви нічого не ввели!')
                else:
                    messagebox.showinfo('Помилка!', 'Введіть числове значення!')

        menu_rot = Tk()
        menu_rot["bg"] = "black"
        #menu_rot.iconbitmap("my_icon.jpg")
        menu_rot.title(self.title)
        menu_rot.geometry('400x250')
        label_size = Label(menu_rot, text=self.text, bg="black", fg="white",
                           font=("Times New Roman", 14))
        label_size.place(x=20, y=10)
        text_val = Entry(menu_rot, width=15, font=("Times New Roman", 14))
        text_val.place(x=25, y=70)
        btn = Button(menu_rot, text="Ввести", command=read_input,
                     bg="black", fg="white", font=("Times New Roman", 14))
        btn.place(x=225, y=60)
        menu_rot.mainloop()


def photo_concl():
    img = cv2.imread('photo.png')
    h, w = img.shape

    back = cv2.imread('background.jpg', cv2.IMREAD_GRAYSCALE)
    hh, ww = back.shape

    yoff = round((hh - h) / 2)
    xoff = round((ww - w) / 2)

    result = back.copy()
    result[yoff:yoff + h, xoff:xoff + w] = img

    cv2.imshow('CENTERED', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('D:\changed_images\_nakladeno.jpg', result)
