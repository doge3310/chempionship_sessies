from tkinter import ttk
import tkinter as tk
from db_init import Department, User, Posts, \
    StudyCalend, AbsenceCalend, VocationCalend
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
                                      command=lambda x=jtem: self.dep_button(x))

                if jtem == item:
                    self.but.place(x=w_size * jndex, y=h_size * index)

                else:
                    self.but.place(x=w_size * jndex, y=h_size * index + h_size)

        self.icon_fr.place(x=5, y=5, width=1900, height=200)
        self.empl_list.place(x=910, y=210, width=900, height=800)
        self.structure.place(x=5, y=210, width=900, height=800)

    def dep_button(self, department):
        for widget in self.empl_list.winfo_children():
            widget.destroy()

        for i in User.select():
            if str(i.department) == str(department):
                self.wind_construct(i.__data__)

    def wind_construct(self, dct):
        user_dict = [str(dct[i]) for i in dct]
        dep_name = Department.get(id=user_dict[7]).name
        post_name = Posts.get(id=user_dict[6]).name

        text = f"""{dep_name} - {post_name}
                   {user_dict[1]} {user_dict[2]} {user_dict[3]}
                   {user_dict[10]} {user_dict[13]}
                   {user_dict[-2]}"""

        self.user_button = tk.Button(self.empl_list,
                                     text=text,
                                     font=("Arial", 20),
                                     command=lambda a=user_dict: self.user_window(a))

        self.user_button.pack(anchor="nw")

    def user_window(self, user_data):
        user_window = tk.Toplevel(self.master)
        user_window = UserChange(user_window, user_data)


class UserChange(tk.Frame):
    def __init__(self, master, user):
        super().__init__()
        absence = list(AbsenceCalend.select().where(AbsenceCalend.username == user[0]))
        study = list(StudyCalend.select().where(StudyCalend.username == user[0]))
        vocation = list(VocationCalend.select().where(VocationCalend.username == user[0]))
        x1 = 0.5
        hy = 70

        self.calend_fr = tk.Frame(master, background="grey")
        self.change_fr = tk.Frame(master, background="grey")

        for _, item in enumerate(absence):
            self.it_absence = tk.Button(master,
                                        text=f"{item.name}, {item.date_from}, {item.date_to}",
                                        command=lambda x=item: self.absence_calend(x))
            self.it_absence.place(x=620, y=x1 * hy, width=570, height=50)
            x1 += 1

        for _, item in enumerate(study):
            self.it_study = tk.Button(master,
                                      text=f"{item.name}, {item.date_from}, {item.date_to}",
                                      command=lambda x=item: self.study_calend(x))
            self.it_study.place(x=620, y=x1 * hy, width=570, height=50)
            x1 += 1

        for _, item in enumerate(vocation):
            self.it_vocation = tk.Button(master,
                                         text=f"{item.name}, {item.date_from}, {item.date_to}",
                                         command=lambda x=item: self.vocation_calend(x))
            self.it_vocation.place(x=620, y=x1 * hy, width=570, height=50)
            x1 += 1

        self.calend_fr.place(x=610, y=10, width=590, height=780)
        self.change_fr.place(x=10, y=10, width=590, height=780)
        master.geometry("1210x800")

    def absence_calend(self, cal):
        pass

    def study_calend(self, cal):
        pass

    def vocation_calend(self, cal):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1920x1080")
    myapp = Main(root)
    myapp.mainloop()
