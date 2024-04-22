from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
# from rest_framework import viewsets
from .forms import CustomRegistrationForm, CreateChatroomForm
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.contrib.auth.models import User

Resource = apps.get_model('studygroup','Resource')
Chatroom = apps.get_model('studygroup','Chatroom')
ChatroomMember = apps.get_model('studygroup','ChatroomMember')
Message= apps.get_model('studygroup','Message')
Course= apps.get_model('studygroup','Course')
Subject= apps.get_model('studygroup','Subject')
UserProfile= apps.get_model('studygroup','UserProfile')
def index(request):
    return render(request,'studygroup/index.html')

@login_required
def profile(request,user_id):
    
    user_profile= User.objects.get(pk=user_id)
    user= UserProfile.objects.get(user=user_profile)
    # user = get_object_or_404('UserProfile',user=user_profile)
    return render(request, 'studygroup/profile.html', {
        'userprofile':user_profile,
        'user':user
    })
    
def login_view(request):
    if request.method=="POST":
        username= request.POST["username"]
        password= request.POST["password"]
        user= authenticate(request,username=username, password=password)
        if user is not None:
          
           login(request,user)
            
        else:
            return render("registration/login.html", {
                "message":"Invalid Credentials"
            })
    return render(request,"registration/login.html")

def register(request):
    if request.method =='POST':
        form =CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # username= form.cleaned_data.get('username')
            # messages.success(request, f" Your account has been successfully created! You are now able to log in as {username}" )
            return redirect('studygroup:login')
    else:
        form = CustomRegistrationForm()

    return render(request,'register.html',{'form':form})

@login_required
def dashboard(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None

    # user_profile= request.user.userprofile
    subjects= Subject.objects.all()
    
    return render(request, 'studygroup/dashboard.html',{
        'user_profile':user_profile,
        'subjects':subjects
        
    })

@login_required    
def get_courses(request, subject_id):
    courses = Course.objects.filter(subject_id=subject_id).values('id', 'name')
    return JsonResponse(list(courses), safe=False)

@login_required
def course_detail(request, subject_id, course_id):
    subject = get_object_or_404(Subject, id=subject_id)
    course = get_object_or_404(Course, id= course_id, subject=subject)
    existing_chatrooms = Chatroom.objects.filter(course=course)
    user_profile= UserProfile.objects.get(user=request.user)
    user_chatrooms = Chatroom.objects.filter(members__userprofile = user_profile)
    user_existing_chatrooms= existing_chatrooms.filter(members__userprofile=user_profile)
    

    
    return render(request, 'studygroup/course_detail.html',{
        'course':course,
        'user_existing_chatrooms':user_existing_chatrooms,
        'user_chatrooms':user_chatrooms,
        'subject_id':subject_id,
        'existing_chatrooms':existing_chatrooms,
        
        
        
    })
    
@login_required
def create_chatroom(request,subject_id, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CreateChatroomForm(request.POST)
        if form.is_valid():
            chatroom = form.save(commit=False)  # Don't save yet
            chatroom.course = course
            chatroom.created_by = request.user
            chatroom.save()

            ChatroomMember.objects.create(user=request.user, chatroom=chatroom)

            return redirect('studygroup:course_detail', subject_id=subject_id, course_id=course_id)
    else:
        form = CreateChatroomForm()

    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'studygroup/create_chatroom.html', context)

@login_required
def join_chatroom(request, chatroom_id):
    chatroom = get_object_or_404(Chatroom, pk=chatroom_id)
    user=request.user # Assuming UserProfile model

    
    # if chatroom.members.filter(userprofile=user).exists():
    #     messages.warning(request, 'You are already a member of this chatroom.')
    #     return redirect('studygroup:course_detail', subject_id=chatroom.course.subject.id, course_id=chatroom.course.id)

    
    ChatroomMember.objects.create(chatroom=chatroom, user=user)
    messages.success(request, 'You have successfully joined the chatroom!')

    return redirect('studygroup:chatroom_view', chatroom_id=chatroom.id)

# @login_required
# def join_request(request,chatroom_id):
#     chatroom = get_object_or_404(Chatroom, id = chatroom_id)
#     user= request.user
    
#     if request.method == 'POST':
        

@login_required
def chatroom_view(request, chatroom_id):
    chatroom=Chatroom.objects.get(id=chatroom_id)
    subject_id = chatroom.course.subject.id
    course_id=chatroom.course.id
    # chatroom_members = ChatroomMember.objects.filter(chatroom=chatroom)
    members = chatroom.members.all()
    # user_ids = [member.user.id for member in members]
    messages=Message.objects.filter(chatroom = chatroom)
    
    if request.method=='POST':
        content = request.POST['message']
        user= request.user
        Message.objects.create(chatroom=chatroom, user=user, content=content)
        return redirect('studygroup:chatroom_view',chatroom_id=chatroom_id)
    
    return render(request,'chatroom.html',{
        'chatroom':chatroom,
        'messages':messages,
        'subject_id':subject_id,
        'course_id':course_id,
        'members':members,
        # 'user_ids':user_ids
        
    })
    

    
@login_required
def chatroom_resources(request, chatroom_id):
    chatroom = get_object_or_404(Chatroom, pk=chatroom_id)
    resources = Resource.objects.filter(chatroom=chatroom)

    if request.method == 'POST':
        resource_type = request.POST.get('resource_type')
        description = request.POST.get('description', '')

        if resource_type == 'IMAGE':
            resource_file = request.FILES.get('resource_file')
            if not resource_file:
                messages.error(request, 'Please select an image file to upload.')
                return redirect('studygroup:chatroom_resources', chatroom_id=chatroom.id)
            resources = Resource.objects.create(
                chatroom=chatroom,
                user=request.user,
                type=resource_type,
                description=description,
                image=resource_file,
            )
        elif resource_type == 'VIDEO':
            resource_url = request.POST.get('resource_url')
            if not resource_url:
                messages.error(request, 'Please enter a video URL.')
                return redirect('studygroup:chatroom_resources', chatroom_id=chatroom.id)
            resources = Resource.objects.create(
                chatroom=chatroom,
                user=request.user,
                type=resource_type,
                description=description,
                video_url=resource_url,
            )
        else:  # resource_type == 'LINK'
            resource_link = request.POST.get('resource_link')
            if not resource_link:
                messages.error(request, 'Please enter a link.')
                return redirect('studygroup:chatroom_resources', chatroom_id=chatroom.id)
            resources = Resource.objects.create(
                chatroom=chatroom,
                user=request.user,
                type=resource_type,
                description=description,
                link=resource_link,
            )
        messages.success(request, 'Resource uploaded successfully!')
        return redirect('studygroup:chatroom_resources', chatroom_id=chatroom.id)

    return render(request, 'studygroup/chatroom_resources.html', {
        'chatroom': chatroom,
        'resources': resources,
        'chatroom_id':chatroom_id
    })

def logout_view(request):
    logout(request)
    return redirect('studygroup:index')
