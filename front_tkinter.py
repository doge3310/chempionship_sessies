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

        self.cals = ["absence", "study", "vocation"]
        x1 = 1
        hy = 70

        self.calend_fr = tk.Frame(master, background="grey")
        self.change_fr = tk.Frame(master, background="grey")

        self.absence_text = tk.Label(master, text="absence callendar")
        self.study_text = tk.Label(master, text="study callendar")
        self.vocation_text = tk.Label(master, text="vocation calend")

        self.calend_text = tk.Text(master)
        self.add_calend = tk.Button(master, text="ADD", command=self.add_cal)
        self.del_cal = tk.Button(master, text="DELETE", command=self.delete_cal)

        self.absence_text.place(x=620, y=(x1 - 1) * hy)

        for _, item in enumerate(absence):
            self.it_absence = tk.Button(master,
                                        text=f"{item.name}, {item.date_from}, {item.date_to}",
                                        command=lambda x=item: self.info(x, 0))
            self.it_absence.place(x=620, y=x1 * hy, width=570, height=50)
            x1 += 1

        x1 += 1
        self.study_text.place(x=620, y=(x1 - 1) * hy)

        for _, item in enumerate(study):
            self.it_study = tk.Button(master,
                                      text=f"{item.name}, {item.date_from}, {item.date_to}",
                                      command=lambda x=item: self.info(x, 1))
            self.it_study.place(x=620, y=x1 * hy, width=570, height=50)
            x1 += 1

        x1 += 1
        self.vocation_text.place(x=620, y=(x1 - 1) * hy)

        for _, item in enumerate(vocation):
            self.it_vocation = tk.Button(master,
                                         text=f"{item.name}, {item.date_from}, {item.date_to}",
                                         command=lambda x=item: self.info(x, 2))
            self.it_vocation.place(x=620, y=x1 * hy, width=570, height=50)
            x1 += 1

        self.calend_fr.place(x=610, y=10, width=590, height=780)
        self.change_fr.place(x=10, y=10, width=590, height=780)
        self.calend_text.place(x=15, y=15, width=580, height=700)
        self.add_calend.place(x=15, y=740, width=100, height=30)
        self.del_cal.place(x=130, y=740, width=100, height=30)
        master.geometry("1210x800")

    def info(self, cal, cal_num):
        self.calend_text.delete(1.0, tk.END)
        self.calend_text.insert(1.0, f"{cal.id}\n{cal.name}\n{cal.username}\n{cal.date_from}\n{cal.date_to}\n")
        self.calend_text.insert(tk.END, f"{self.cals[cal_num]}")

    def add_cal(self):
        text = self.calend_text.get(1.0, tk.END)
        fields = [i for i in text.split("\n") if i]

        if fields[-1] == self.cals[0]:
            AbsenceCalend.get_or_create(name=fields[1],
                                        defaults={
                                            "username": fields[2],
                                            "date_from": fields[3],
                                            "date_to": fields[4]
                                        })

        elif fields[-1] == self.cals[1]:
            StudyCalend.get_or_create(name=fields[1],
                                      defaults={
                                          "username": fields[2],
                                          "date_from": fields[3],
                                          "date_to": fields[4]
                                      })

        elif fields[-1] == self.cals[2]:
            VocationCalend.get_or_create(name=fields[1],
                                         defaults={
                                             "username": fields[2],
                                             "date_from": fields[3],
                                             "date_to": fields[4]
                                         })

    def delete_cal(self):
        text = self.calend_text.get(1.0, tk.END)
        fields = [i for i in text.split("\n") if i]

        if fields[-1] == self.cals[0]:
            AbsenceCalend.delete_by_id(fields[0])

        elif fields[-1] == self.cals[1]:
            StudyCalend.delete_by_id(fields[0])

        elif fields[-1] == self.cals[2]:
            VocationCalend.delete_by_id(fields[0])


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1920x1080")
    myapp = Main(root)
    myapp.mainloop()
