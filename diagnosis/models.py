from django.db import models
from users.models import User
import os
    
class DiagnosisPicture(models.Model):
    def get_upload_to(self, filename):
        return os.path.join('images', 'diagnosis_picture', str(self.user.pk), filename)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_upload_to, default='images/diagnosis_picture/default_question_picture.jpg')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} ({1})'.format(self.user.email, self.creation_date)