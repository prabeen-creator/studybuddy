from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
   
    bio = models.TextField(blank= True)
    year= models.CharField(max_length= 65)
    major= models.CharField(max_length= 65)
    interests= models.TextField(blank= True)
    
class Subject(models.Model):
    name= models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return str(self.name)
    
class Course(models.Model):
    name= models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    
    def __str__(self):
        return str(self.name)


class Chatroom(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='chatrooms')  # Replace 'Course' with your actual model name
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, through='ChatroomMember', related_name='chatrooms')
    num_resources = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Chatroom: {self.name} (Course: {self.course.name})"


class Message(models.Model):
    content = models.TextField()
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatroom_messages')
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
     return f"Message by {self.user.username} in {self.chatroom.name}: {self.content[:20]}"
 
 
class ChatroomMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_approved= models.BooleanField(default= False)
    
    class Meta:
        unique_together = ('user', 'chatroom')
        
class Resource(models.Model):
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Resource type choices
    TYPE_CHOICES = (
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('LINK', 'Link'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='LINK')

    image = models.ImageField(upload_to='chatroom_resources/images/', blank=True)
    video_url = models.URLField(blank=True)
    link = models.URLField(blank=True)

    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}: {self.get_short_description()}"

    def get_short_description(self):
        if self.type == 'IMAGE':
            return f"Image ({self.image.name})"
        elif self.type == 'VIDEO':
            return f"Video: {self.video_url[:20]}"  # Truncate long URLs
        else:
            return self.link[:20]
        
        
        