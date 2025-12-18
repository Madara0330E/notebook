from django.db import models


class Person(models.Model):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    patronymic = models.CharField("Отчество", max_length=100, blank=True, null=True)
    birth_date = models.DateField("Дата рождения")
    gender = models.CharField("Пол", max_length=10)
    workplace = models.CharField("Место работы/учёбы", max_length=200)
    position = models.CharField("Должность", max_length=150)
    notes = models.TextField("Заметки", blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Человек"
        verbose_name_plural = "Люди"


class Contact(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Человек")
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Электронная почта")
    address = models.CharField("Адрес", max_length=255)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)

    def __str__(self):
        return f"{self.phone} — {self.person}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Relationship(models.Model):
    person = models.ForeignKey(Person, related_name="person", on_delete=models.CASCADE, verbose_name="Человек")
    related_person = models.ForeignKey(Person, related_name="related_person", on_delete=models.CASCADE,
                                       verbose_name="Связанный человек")
    relationship_type = models.CharField("Тип отношений", max_length=100)
    note = models.TextField("Примечания", blank=True, null=True)

    def __str__(self):
        return f"{self.person} — {self.relationship_type} — {self.related_person}"

    class Meta:
        verbose_name = "Отношение"
        verbose_name_plural = "Отношения"


class Event(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Человек")
    event_type = models.CharField("Тип события", max_length=100)
    event_date = models.DateField("Дата события")
    reminder_days = models.PositiveSmallIntegerField("Дней до напоминания")

    def __str__(self):
        return f"{self.event_type} — {self.person}"

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"


class GreetingTemplate(models.Model):
    event_type = models.CharField("Тип события", max_length=100)
    template_text = models.TextField("Текст шаблона")

    def __str__(self):
        return self.event_type

    class Meta:
        verbose_name = "Шаблон поздравления"
        verbose_name_plural = "Шаблоны поздравлений"


class Greeting(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Человек")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Событие")
    created_at = models.DateTimeField("Дата генерации", auto_now_add=True)
    greeting_text = models.TextField("Текст поздравления")
    is_sent = models.BooleanField("Отправлено", default=False)
    template = models.ForeignKey(GreetingTemplate, on_delete=models.SET_NULL,
                                 verbose_name="Шаблон", null=True, blank=True)

    def __str__(self):
        return f"Поздравление для {self.person}"

    class Meta:
        verbose_name = "Поздравление"
        verbose_name_plural = "Поздравления"