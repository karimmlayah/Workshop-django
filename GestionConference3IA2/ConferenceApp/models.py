from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s-]+$',
                message='Le nom doit contenir uniquement des lettres alphabétiques et des epaces .'
            )
        ]
    )
    THEME =[
        ('CS', 'Computer Science'),
        ('AI', 'Artificial Intelligence'),
        ('SE', 'Science & Engineering'),
        ('SSE', 'Social Sciences & Education'),
        ('IT', 'Interdisciplinary Themes'),
    ]
    theme = models.CharField(max_length=255,choices=THEME)
    #theme = models.CharField(max_length=255,choices=['CS', 'AI', 'SE', 'SSE', 'IT'])
    location = models.CharField(max_length=255)
    description = models.TextField(validators=[MinLengthValidator(30,"Minimum 30 characters.")]) 
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True) #juste une seule fois
    updated_at = models.DateTimeField(auto_now=True) #chaque update
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")


class Submission(models.Model):
    Submission_id = models.CharField(max_length=255,primary_key=True,unique=True,editable=False)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keyword = models.TextField()
    paper = models.FileField(
        upload_to='papers/'
    )
    STATUS= [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=50,choices=STATUS, default='submitted')
    submission_date = models.DateTimeField(auto_now_add=True)
    payed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) #juste une seule fois
    updated_at = models.DateTimeField(auto_now=True) #chaque update
    user = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name='submissions')
    conference = models.ForeignKey('Conference', on_delete=models.CASCADE, related_name='submissions')




