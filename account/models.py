from django.db import models
from django.contrib.auth.models import User

    # .with.. other fields and methods ...       
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    yearofstudy = models.CharField(max_length=10)
    usertype = models.CharField(max_length=20)  
    userid = models.CharField(max_length=20, default=0)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    rollno = models.CharField(max_length=20, blank=True, null=True)  # Assuming rollno is a character field
    date = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    photo1 = models.ImageField(upload_to='achievement_photos/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='achievement_photos/', blank=True, null=True) 
    # Add other fields as needed

    def __str__(self):
        return f"{self.user.username} - {self.title}"   
    

class Academic_Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    rollno = models.CharField(max_length=20, blank=True, null=True)  # Assuming rollno is a character field
    title = models.CharField(max_length=255)
    description = models.TextField()
    photo1 = models.ImageField(upload_to='achievement_photos/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='achievement_photos/', blank=True, null=True) 
    # Add other fields as needed

    def __str__(self):
        return f"{self.user.username} - {self.title}"
 

class  Extracurricular_Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    rollno = models.CharField(max_length=20, blank=True, null=True)  # Assuming rollno is a character field   
    date = models.DateField(null=True)
    title = models.CharField(max_length=255)  
    position=models.CharField(max_length=50)
    description = models.TextField()
    photo1 = models.ImageField(upload_to='achievement_photos/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='achievement_photos/', blank=True, null=True) 
    # Add other fields as needed

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class  placement_Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    rollno = models.CharField(max_length=20, blank=True, null=True)  # Assuming rollno is a character field
    title = models.CharField(max_length=255)  
    position=models.CharField(max_length=50)
    description = models.TextField()
    photo1 = models.ImageField(upload_to='achievement_photos/', blank=True, null=True)
   
    # Add other fields as needed

    def __str__(self): 
        return f"{self.user.username} - {self.title}"   

class  workshop_Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    rollno = models.CharField(max_length=20, blank=True, null=True)  # Assuming rollno is a character field
    title = models.CharField(max_length=255) 
    title1 = models.CharField(max_length=255)  
    description = models.TextField() 
    fromdate = models.DateField()
    todate = models.DateField()  
    days=models.CharField(max_length=10)  
    photo1 = models.ImageField(upload_to='achievement_photos/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='achievement_photos/', blank=True, null=True)

    # Add other fields as needed

    def __str__(self):
        return f"{self.user.username} - {self.title}"

