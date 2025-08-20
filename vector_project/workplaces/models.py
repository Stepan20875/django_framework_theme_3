from django.db import models
from personnel.models import Employee

class Workplace(models.Model):
    group_number = models.IntegerField()
    post_number = models.IntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name='workplaces')

    def __str__(self):
        return f"Group {self.group_number}, Post {self.post_number}"