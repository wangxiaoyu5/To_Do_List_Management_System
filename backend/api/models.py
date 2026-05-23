from django.db import models
from django.conf import settings
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default='#1890ff')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default='#52c41a')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tags'
    )

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name


class Task(TimeStampedModel):
    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM',
        db_index=True
    )
    due_date = models.DateTimeField(null=True, blank=True, db_index=True)
    completed = models.BooleanField(default=False, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    tags = models.ManyToManyField(Tag, through='TaskTag', related_name='tasks')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def mark_completed(self):
        self.completed = True
        self.completed_at = timezone.now()
        self.save()


class TaskTag(TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='task_tags')

    class Meta:
        unique_together = ['task', 'tag']

    def __str__(self):
        return f'{self.task.title} - {self.tag.name}'
