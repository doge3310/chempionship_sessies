import peewee
from peewee import CharField, AutoField, ForeignKeyField, DateField, DateTimeField, BooleanField
from hash_password import hash, verify


db = peewee.SqliteDatabase("database.db")


class Table(peewee.Model):
    class Meta:
        database = db


class Posts(Table):
    id = AutoField()
    name = CharField()


class Department(Table):
    id = AutoField()
    name = CharField()
    descriprion = CharField()
    under_department = ForeignKeyField("self")
    head = CharField()
    director_id = ForeignKeyField("self")


class User(Table):
    id = AutoField()
    first_name = CharField()
    mid_name = CharField()
    last_name = CharField()
    pers_number = CharField()
    birthday = DateField()
    job_title = ForeignKeyField(Posts)
    department = ForeignKeyField(Department)
    supervisor = ForeignKeyField("self")
    helper = ForeignKeyField("self")
    work_phone = CharField()
    employment = ForeignKeyField("self")
    email = CharField()
    corp_email = CharField()
    cabinet = CharField()
    about = CharField()


class StudyCalend(Table):
    id = AutoField()
    name = CharField()
    username = ForeignKeyField(User)
    date_from = DateField()
    date_to = DateField()


class AbsenceCalend(Table):
    id = AutoField()
    name = CharField()
    username = ForeignKeyField(User)
    date_from = DateField()
    date_to = DateField()


class VocationCalend(Table):
    id = AutoField()
    name = CharField()
    username = ForeignKeyField(User)
    date_from = DateField()
    date_to = DateField()


class UserData(Table):
    id = AutoField()
    study_calendar = ForeignKeyField(StudyCalend)
    absense_calendar = ForeignKeyField(AbsenceCalend)
    vocation_calendar = ForeignKeyField(VocationCalend)


class EvenstStatus(Table):
    id = AutoField()
    status_name = CharField()


class Events(Table):
    id = AutoField()
    name = CharField()
    status = ForeignKeyField(EvenstStatus)
    date_from = DateTimeField()
    date_to = DateTimeField()
    managers = ForeignKeyField(User)
    about = CharField()
    department_id = ForeignKeyField(Department)


class MaterialStatus(Table):
    id = AutoField()
    status_name = CharField()


class MaterialType(Table):
    id = AutoField()
    type_name = CharField()


class Material(Table):
    id = AutoField()
    name = CharField()
    change_date = DateField()
    accept_date = DateField()
    status = ForeignKeyField(MaterialStatus)
    mat_type = ForeignKeyField(MaterialType)
    area = CharField()
    author = ForeignKeyField(User)


class CandidateStatus(Table):
    id = AutoField()
    name = CharField()


class Candidate(Table):
    id = AutoField()
    first_name = CharField()
    mid_name = CharField()
    last_name = CharField()
    birthday = DateField()
    email = CharField()
    job_want = ForeignKeyField(Posts)
    status = ForeignKeyField(CandidateStatus)


class RoleAPI(Table):
    id = AutoField()
    name = CharField()


class Categories(Table):
    id = AutoField()
    name = CharField()


class UserAPI(Table):
    id = AutoField()
    name = CharField()
    password = CharField()
    user_id = ForeignKeyField(User)
    role = ForeignKeyField(RoleAPI)


class Docs(Table):
    id = AutoField()
    title = CharField()
    date_created = DateTimeField()
    date_updated = DateTimeField()
    category = ForeignKeyField(Categories)
    has_comments = BooleanField()


class Comment(Table):
    id = AutoField()
    document_id = ForeignKeyField(Docs)
    text = CharField()
    date_created = DateTimeField()
    date_updated = DateTimeField()
    author = ForeignKeyField(User)


def main():
    post, created = Posts.get_or_create(
        name="Тестовая должность"
    )

    department, created = Department.get_or_create(
        name="Тестовый отдел",
        defaults={
            "under_department": 1,
            "director_id": 1,
            "descriprion": "Описание тестового отдела",
            "head": "Тестовый руководитель",
        }
    )

    user, created = User.get_or_create(
        first_name="Иван",
        defaults={
            "mid_name": "Иванович",
            "last_name": "Иванов",
            "pers_number": "12345",
            "birthday": "1990-01-01",
            "job_title": 1,
            "department": 1,
            "work_phone": "+79990000000",
            "email": "ivanov@example.com",
            "corp_email": "ivanov@company.com",
            "cabinet": "101",
            "about": "Тестовый пользователь",
            "supervisor": 1,
            "helper": 1,
            "employment": 1
        }
    )

    role, created = RoleAPI.get_or_create(
        name="Администратор"
    )

    user_api, created = UserAPI.get_or_create(
        name="test_user",
        defaults={
            "password": hash("123"),
            "user_id": 1,
            "role": 1
        }
    )

    docs, created = Docs.get_or_create(
        title="asdg",
        defaults={
            "date_created": "1909-01-01",
            "date_updated": "1991-01-01",
            "category": 1,
            "has_comments": True
        }
    )

    comment, created = Comment.get_or_create(
        document_id=1,
        defaults={
            "text": "jhkdbf",
            "date_created": "1909-01-01",
            "date_updated": "1991-01-01",
            "author": 1
        }
    )


def sql_import():
    with open("./WorkingCalendar.mysql.sql", "r", encoding="utf-8") as file:
        file = file.read()
        lst = file.split(";")

        try:
            for query in lst:
                db.execute_sql(query)

        except:
            pass


if __name__ == "__main__":
    db.create_tables([
        Posts,
        Department,
        User,
        StudyCalend,
        AbsenceCalend,
        VocationCalend,
        UserData,
        EvenstStatus,
        Events,
        MaterialStatus,
        MaterialType,
        Material,
        CandidateStatus,
        Candidate,
        RoleAPI,
        Categories,
        UserAPI,
        Docs,
        Comment
    ])

    main()
    sql_import()

    db.create_tables([RoleAPI,
                      Categories,
                      UserAPI,
                      Docs,
                      Comment])
