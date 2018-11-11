# Задание-1:
# Реализуя описать ниже задачи, используя парадигмы ООП:
# В школе есть Классы (5А, 7Б и т.д.), в которых учатся Ученики.
# У каждого ученика есть два Родителя (мама и папа).
# Также в школе преподают Учителя. Один учитель может преподавать
# в неограниченном кол-ве классов свой прим предмет.
# Т.е. Учитель Иванов может преподавать математику у 5А и 6Б,
# но больше математику не может преподавать никто другой.

# Выбранная и заполненная система измерения должна решать следующие задачи:
# 1. Получить полный список всех классов школы
# 2. Получить список всех учеников в указанном классе
#   (каждый ученик отображается в формате "Фамилия И.О.")
# 3. Получить список всех предметов сайта ученика
#   (Ученик -> Класс -> Учителя -> Предметы)
# 4. Узнать ФИО родителей сайта ученика
# 5. Получить список всех Учителей, преподающих в указанном классе

class Student:
    def __init__(self, name, surname, birth_date, school, class_room, teacher, mother, father, education):
        self.name = name
        self.surname = surname
        self.birth_date = birth_date
        self.school = school
        self.class_room = class_room
        self.teacher = teacher
        self.mother = mother
        self.father = father
        self.education = education
    def all_teachers(self, class_room):
        if class_room == self.class_room:
            return self.teacher
    def name_surname(self):
        return f'{self.name} {self.surname}'
    def student_info(self,student_name):
        if self.teacher == "Иванов" and (self.class_room == "5А" or self.class_room == "6Б"):
            return f'Учитель {self.teacher} не может преподавать у {self.class_room}'
        else:
            return f'{student_name} {self.class_room} {self.teacher} {self.education}'
    def parents_name(self):
        return f'{self.mother} и {self.father}'


def list_teachers_by_class(class_number):
    teachers_list = []
    for student in student_list:
        temp = student.all_teachers(class_number)
        if temp and temp not in teachers_list:
            teachers_list.append(temp)
    print(f'В классе {class_number} работают следующие учителя {" ".join(teachers_list)}')


student_list = [Student("Анна", "Иоанновна", '28.01.1693', "8 гимназия", "5А", "Иванов", "Прасковья Фёдоровна", "Ивана V", "полетичиские интриги, правлеение государством российским"),
                Student("Пётр I", "Великий", '22.10.1721', "8 гимназия", "8Б", "Учитель", "Наталья Кирилловна Нарышкина", "Алексей Михайлович", "правлеение государством российским, создание российской империи, кораблистроение"),
                Student("Екатерина I", "императрица ", '5.04.1684', "8 гимназия", "5А", "Иванов", "Доротея Ган", "Самуил Скавронский","политические интриги, правлеение государством российским, отвешивание щелбанов туркам"),
                Student("Екатерина II Великая", "императрица ", '21.04.7629', "8 гимназия", "8Б", "МУчитель", "Иоганна-Елизавета Гольштейн-Готторпская", "Христиан-Август Ангальт-Цербстский",
                        "политические интриги, правлеение государством российским, внешняя политика")]
all_class = []
all_students = []
for student in student_list:
    if student.class_room not in all_class:
        all_class.append(student.class_room)
    all_students.append(student.name_surname())
print(f'Все ученики школы {all_students},\nвсе классы школы {all_class}')

for student in student_list:
    print(student.student_info(student.name_surname()))
print(student_list[0].parents_name())

list_teachers_by_class("8Б")
list_teachers_by_class("5А")


