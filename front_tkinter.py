from tkinter import ttk
import tkinter as tk
from db_init import Department, User, Posts
from PIL import Image, ImageTk


class Main(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.icon_fr = tk.Canvas(background="#89FC43")
        self.icon_fr.create_rectangle(230, 30, 1700, 150, fill="white")
        self.icon_fr.create_text(500, 80, text="Организационная структура", font=("Arial", 30))

        pil_image = Image.open("Logo.png")
        self.tk_image = ImageTk.PhotoImage(pil_image)
        self.icon_fr.create_image(100, 100, image=self.tk_image)

        self.empl_list = tk.Frame(background="grey")
        self.structure = tk.Frame(background="grey")

        w_size = 110
        h_size = 60

        # конструктор структуры
        all_deps = Department.select()
        deps = [i.name for i in all_deps]
        struct = {}

        for i in all_deps:
            dep, und_dep = i.__data__["id"], i.__data__["under_department"]

            try:
                struct[und_dep].append(dep)

            except KeyError:
                struct[und_dep] = [dep]

        # контруктор дерева
        for index, item in enumerate(struct):
            for jndex, jtem in enumerate(struct[item]):
                self.but = ttk.Button(self.structure, text=deps[jtem - 1],
                                      command=lambda x=jtem: self.button(x))

                if jtem == item:
                    self.but.place(x=w_size * jndex, y=h_size * index)

                else:
                    self.but.place(x=w_size * jndex, y=h_size * index + h_size)

        self.icon_fr.place(x=5, y=5, width=1900, height=200)
        self.empl_list.place(x=910, y=210, width=900, height=800)
        self.structure.place(x=5, y=210, width=900, height=800)

    def button(self, department):
        for widget in self.empl_list.winfo_children():
            widget.destroy()

        for i in User.select():
            if str(i.department) == str(department):
                self.wind_construct(i.__data__)

    def wind_construct(self, dct):
        dct = [str(dct[i]) for i in dct]
        dep_name = Department.get(id=dct[7]).name
        post_name = Posts.get(id=dct[6]).name

        text = f"""{dep_name} - {post_name}
                   {dct[1]} {dct[2]} {dct[3]}
                   {dct[10]} {dct[13]}
                   {dct[-2]}"""

        self.user_button = tk.Button(self.empl_list,
                                     text=text,
                                     font=("Arial", 20))

        self.user_button.pack(anchor="nw")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1920x1080")
    myapp = Main(root)
    myapp.mainloop()
