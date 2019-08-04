import random
from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Subject
from datacenter.models import Commendation


COMMENDATION_EXAMPLES = '''1. Молодец!
2. Отлично!
3. Хорошо!
4. Гораздо лучше, чем я ожидал!
5. Ты меня приятно удивил!
6. Великолепно!
7. Прекрасно!
8. Ты меня очень обрадовал!
9. Именно этого я давно ждал от тебя!
10. Сказано здорово – просто и ясно!
11. Ты, как всегда, точен!
12. Очень хороший ответ!
13. Талантливо!
14. Ты сегодня прыгнул выше головы!
15. Я поражен!
16. Уже существенно лучше!
17. Потрясающе!
18. Замечательно!
19. Прекрасное начало!
20. Так держать!
21. Ты на верном пути!
22. Здорово!
23. Это как раз то, что нужно!
24. Я тобой горжусь!
25. С каждым разом у тебя получается всё лучше!
26. Мы с тобой не зря поработали!
27. Я вижу, как ты стараешься!
28. Ты растешь над собой!
29. Ты многое сделал, я это вижу!
30. Теперь у тебя точно все получится!'''


def get_schoolkid(name):
    """The function gets schoolkid by name (FIO).

    The name of schoolkid can be not full. If database contain one 
    record with incoming name, function return schoolkid. Otherwise the message
    to be more accurate will be and function return None    

    :param name: name of schoolkid 
    :type: str
    :return: give schoolkid 
    :rtype: Schoolkid

    """
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.MultipleObjectsReturned as multiple_schoolkid_err:
        print("Multiple schoolkids are returned. Please, make your search more accurate")
        return
    except Schoolkid.DoesNotExist as no_schoolkid_err:
        print("No one schoolkid is returned. Please, make your search more accurate")
        return
    print("Got schoolkid:", schoolkid)
    return schoolkid


def fix_marks(schoolkid):
    """The function fix bad marks to excellent for schoolkid.

    Print the number of fixed marks after execution

    :param schoolkid: schoolkid object  
    :type: Schoolkid

    """
    marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    mark_count = marks.count()
    marks.update(points=5)
    print("Fixed {0} marks".format(mark_count))


def remove_chastisements(schoolkid):
    """The function remove chastisements for schoolkid.

    Print the number of removed chastisements after execution

    :param schoolkid: schoolkid object  
    :type: Schoolkid

    """
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisement_count = chastisements.count()
    chastisements.delete()
    print("Removed {0} chastisements".format(chastisement_count))


def _get_random_commendation():
    """This private function give random commendation.

    Commendations gets from COMMENDATION_EXAMPLES, which is string constant.
    COMMENDATION_EXAMPLES parse and serialize to list. After that it gets 
    uniform random number from interval [0,count_of_commendations - 1]
    and return commendation from list with index equaled random number.   

    :return: commendation  
    :rtype: str

    """
    commendation_examples = [commendation_example.split('. ')[1]
                             for commendation_example in COMMENDATION_EXAMPLES.split('\n')]
    random_number = random.randint(0, len(commendation_examples)-1)
    return commendation_examples[random_number]


def add_commendation(schoolkid, subject_title):
    """The function add commendation for schoolkid.

    In first step it gets random commendation by using internal function
    In second step it search lessons by schoolkid grooup letter, year of study 
    and subject title. If no lessons find it print about to be more accurate 
    and return. Otherwise it add commendation and print that everything is OK .   

    :param schoolkid: schoolkid, whome added commendation  
    :type: Schoolkid
    :param subject_title: title of subject for which added commendation 
    :type: Str

    """
    commendation_text = _get_random_commendation()
    lessons = Lesson.objects.filter(group_letter=schoolkid.group_letter,
                                    year_of_study=schoolkid.year_of_study,
                                    subject__title=subject_title)
    if (not lessons):
        print("No such subject or lesson for schoolkid. Please check subject title or timetable")
        return
    lesson = lessons.order_by('-date')[0]
    Commendation.objects.create(text=commendation_text, created=lesson.date,
                                schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)
    print("Added commedation '{0}' on {1}".format(
        commendation_text, lesson.date))

# #Examples
# child = get_schoolkid("Фролов Иван")
# fix_marks(child)
# remove_chastisements(child)
# add_commendation(child, "Музыка")
