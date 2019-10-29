import random
import django
import os
import argparse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from datacenter.models import Schoolkid, Mark, Chastisement, Subject, Lesson, Commendation
from django.core.exceptions import ObjectDoesNotExist


def fix_marks(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    marks = Mark.objects.filter(schoolkid=child, points__lte=3)
    updated_marks = Mark.objects.filter(schoolkid=child, points__lte=3).update(points=5)


def remove_chastisements(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    chastisements = Chastisement.objects.filter(schoolkid=child)
    chastisements.delete()


def create_commendation(schoolkid, subject, year_of_study, group_letter):
    commendations = ["Молодец!",
                     "Великолепно!",
                     "Гораздо лучше, чем я ожидал!",
                     "Замечательно!",
                     "Здорово!",
                     "Именно этого я давно ждал от тебя!",
                     "Мы с тобой не зря поработали!",
                     "Отлично!",
                     "Потрясающе!",
                     "Очень хороший ответ!",
                     "Прекрасно!",
                     "Прекрасное начало!",
                     "С каждым разом у тебя получается всё лучше!",
                     "Сказано здорово – просто и ясно!",
                     "Так держать!",
                     "Талантливо!",
                     ]
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    subject = Subject.objects.get(title=subject, year_of_study=year_of_study)
    text = random.choice(commendations)
    last_lesson = Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter, subject=subject).order_by("-date").first()
    teacher = last_lesson.teacher
    created = last_lesson.date
    Commendation.objects.create(text=text, created=created, schoolkid=child, subject=subject, teacher=teacher)


def get_parser():
    parser = argparse.ArgumentParser(
    description='Скрипт предназначен для изменения плохих оценок на хорошие, удаления замечаний и создания похвалы')
    parser.add_argument('schoolkid', help='Фамилия и имя ученика')
    parser.add_argument('subject', help='Учебный предмет')
    parser.add_argument('year_of_study', help='Год обучения')
    parser.add_argument('group_letter', help='Литера класса')
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    schoolkid = args.schoolkid
    subject = args.subject
    year_of_study = args.year_of_study
    group_letter = args.group_letter
    try:
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid, subject, year_of_study, group_letter)
    except ObjectDoesNotExist:
        print(f"Ученик {schoolkid} не найден")


