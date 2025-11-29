import peewee
from peewee import CharField, AutoField, ForeignKeyField, DateField


db = peewee.SqliteDatabase("database.db")


class Table(peewee.Model):
    class Meta:
        database = db


class Posts(Table):
    id = AutoField()
    name = CharField()


class StudyCalend(Table):
    id = AutoField()
    name = CharField()
    date_from = DateField()
    date_to = DateField()


class AbsenceCalend(Table):
    id = AutoField()
    name = CharField()
    date_from = DateField()
    date_to = DateField()


class VocationCalend(Table):
    id = AutoField()
    name = CharField()
    date_from = DateField()
    date_to = DateField()


class UserData(Table):
    id = AutoField()
    study_calendar = ForeignKeyField(StudyCalend)
    absense_calendar = ForeignKeyField(AbsenceCalend)
    vocation_calendar = ForeignKeyField(VocationCalend)


class Department(Table):
    id = AutoField()
    name = CharField()
    descriprion = CharField()
    head = CharField()
    employ_list = CharField()


class User(Table):
    id = AutoField()
    name = CharField()
    pers_number = CharField()
    phone = CharField()
    birthday = DateField()
    job_title = ForeignKeyField(Posts)
    department = ForeignKeyField(Department)
    supervisor = ForeignKeyField("self")
    helper = ForeignKeyField("self")
    work_phone = CharField()
    employment = ForeignKeyField(UserData)
    email = CharField()
    corp_email = CharField()
    acc_num = CharField()
    cabinet = CharField()
    about = CharField()


class EvenstStatus(Table):
    id = AutoField()
    status_name = CharField()


class Events(Table):
    id = AutoField()
    name = CharField()
    status = ForeignKeyField(EvenstStatus)
    date_from = DateField()
    date_to = DateField()
    managers = ForeignKeyField(User)
    about = CharField()


class MaterialStatus(Table):
    id = AutoField()
    status_name = CharField()


class Material(Table):
    id = AutoField()
    name = CharField()
    change_date = DateField()
    accept_date = DateField()
    status = ForeignKeyField(MaterialStatus)
    mat_type = CharField()
    area = CharField()
    author = ForeignKeyField(User)


class Candidate(Table):
    id = AutoField()
    name = CharField()
    birthday = DateField()
    email = CharField()
    job_want = ForeignKeyField(Posts)


def main():
    pass


def sql_import():
    with open("./WorkingCalendar.mysql.sql", "r", encoding="utf-8") as file:
        file = file.read()
        lst = file.split(";")

        for query in lst:
            db.execute_sql(query)


if __name__ == "__main__":
    db.create_tables([
        Posts,
        Department,
        Events,
        StudyCalend,
        AbsenceCalend,
        VocationCalend,
        UserData,
        User,
        Material
    ])

    main()
    sql_import()
