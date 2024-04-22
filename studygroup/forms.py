from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.apps import apps
from django.core.exceptions import ValidationError
UserProfile= apps.get_model('studygroup','UserProfile')
Chatroom= apps.get_model('studygroup','Chatroom')


class CustomRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=255)
    email= forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    YEAR_CHOICES = [
        ('Freshman','Freshman'),
        ('Sophomore','Sophomore'),
        ('Junior','Junior'),
        ('Senior','Senior'),
    ]
    
    year = forms.ChoiceField(choices= YEAR_CHOICES)
    major = forms.CharField(max_length=65)

    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2' , 'year', 'major']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username
    
    def save(self, commit=True):
        user = super(CustomRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                
                year=self.cleaned_data['year'],
                major=self.cleaned_data['major']
            )
        return user
    
class CreateChatroomForm(forms.ModelForm): 
    name= forms.CharField(max_length=100, label="Chatroom Name", required= True)
    
    class Meta:
        model=Chatroom
        fields =['name']
        
    def clean_name(self):
        data= self.cleaned_data.get('name')
        course_id= self.cleaned_data.get('course_id')
        if course_id:
            existing_chatrooms = Chatroom.objects.filter(course__id =course_id, name= data)
            if existing_chatrooms.exists():
                raise forms.ValidationError('A chatroom with this name already exists for this course.')
        return data  
    
    def save(self, commit=True):
        chatroom= super(CreateChatroomForm, self).save(commit=False)
        if commit:
            chatroom.save()
        return chatroom 

    