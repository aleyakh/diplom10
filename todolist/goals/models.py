from django.db import models
from todolist.core.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)

    class Meta:
        abstract = True


class GoalCategory(BaseModel):
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return f'{self.title} - {self.user.username}'


class Goal(BaseModel):
    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(to=GoalCategory, on_delete=models.CASCADE, related_name='goals')
    due_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='goals')
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(choices=Priority.choices, default=Priority.medium)

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"


class GoalComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор', related_name='comments')
    goal = models.ForeignKey(Goal, verbose_name='Цель', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
