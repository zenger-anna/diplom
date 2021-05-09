from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# blank - нельзя добавлять новые значения пустыми, null - не может быть пустого значения в БД


class Student(models.Model):
    group = models.CharField(max_length=200, unique=False, blank=False, null=False)
    semester = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')

    def __str__(self):
        return ' '.join([str(self.group), str(self.user.first_name), str(self.user.last_name)])


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')

    def __str__(self):
        return ' - '.join([str(self.user.id), str(self.user.first_name), str(self.user.last_name)])


class Subject(models.Model):
    title = models.CharField(max_length=200, unique=True, blank=False, null=False)
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, blank=False, null=False)
    semester = models.IntegerField()

    def __str__(self):
        return ' - '.join([str(self.title)])


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200, unique=False)
    document = models.FileField(upload_to='docs/')
    doc_type = models.CharField(max_length=7, unique=False)

    def __str__(self):
        return ' - '.join([str(self.user), str(self.title)])
