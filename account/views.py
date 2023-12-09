from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login , logout 
from django.contrib.auth.decorators import login_required     
from django.template.loader import get_template  
from django.http import HttpResponse  
from xhtml2pdf import pisa  
from PyPDF2 import PdfWriter ,PdfFileReader, PdfReader # Import PdfWriter instead of PdfFileWriter
from io import BytesIO   
from django.core.mail import send_mail     


from django.shortcuts import get_object_or_404  # Import get_object_or_404 

# Create your views here. 


def login(request):
    if request.method == 'POST':
        username = request.POST['rollno']
        password = request.POST['password']
        # Authenticate user based on username, password,
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard page
        else:
            messages.error(request, 'Invalid username, password, or user type.')
    
    return render(request, 'home.html')   
 


 
def register(request):
    if request.method == 'POST':
        rollno = request.POST['rollno']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        yearofstudy = request.POST['yearofstudy']
        usertype = request.POST['usertype']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']  
        photo= request.FILES.get('photo')
        
        
        # Check if the user already exists
        if User.objects.filter(username=rollno).exists():
            messages.error(request, 'User with this roll number already exists.')
            return redirect('register')  # Redirect to the registration page
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')  
        # Create the User and UserProfile objects
        user = User.objects.create_user(username=rollno, password=password)
        user.email = email
        user.save()
        
        user_profile = UserProfile(user=user, name=name, phone=phone, yearofstudy=yearofstudy, usertype=usertype, email=email,userid=rollno , photo=photo )
        user_profile.save()
        
        messages.success(request, 'Registration successful. You can now login.')
        return redirect('login')  # Redirect to the login page
    
    return render(request, 'register.html')   


def google_login_callback(request):
    # Perform any necessary tasks or checks here, if needed
    # ...

    # Redirect the user to the dashboard
    return redirect('dashboard')


@login_required(login_url='login')  
def dashboard(request):    
    user_profile = request.user.userprofile    
    

    if user_profile.usertype == 'student':
        template_name = 'dashboard.html'
    elif user_profile.usertype == 'staff':
        template_name = 'dashboard_staff.html'
    user_profile = request.user.userprofile

    context = {
        'user_profile': user_profile,
        
    }
   
    return render(request, template_name, context)       


    
@login_required(login_url='login')
def profile(request):  
    user_profile = request.user.userprofile

    context = {
        'user_profile': user_profile,
    }
   
    
    return render(request, 'profile.html', context)           

@login_required(login_url='login')
def profile_staff(request):  
    user_profile = request.user.userprofile

    context = {
        'user_profile': user_profile,
    }
   
    
    return render(request, 'profile_staff.html', context) 



@login_required(login_url='login')
def achievement(request):
    username = request.user.username 
    if request.method == 'POST':
        date = request.POST.get('date')
        title = request.POST.get('title')
        description = request.POST.get('description')
        photo1 = request.FILES.get('photo1')
        photo2 = request.FILES.get('photo2')    


        achievement = Achievement.objects.create(
            user=request.user,  
            rollno = username,
            date=date,
            title=title,
            description=description,
            photo1=photo1,
            photo2=photo2
            # Add other fields as needed
        )   
        admin_info=User.objects.get(is_superuser=True)
        admin_email=admin_info.email
        send_mail(
            'New Achievement added  by  -'+username,
            'the '+ username +'  have added the achievement  '+title+'  . please Login to see full information ',
            'balakumaran6111@gmail.com',
            [admin_email],
            fail_silently=False,
                    )

        return redirect('dashboard')  # Change to the appropriate URL  
    context = {
        'username': username,
    }

    return render(request, 'add_achievement.html',context)       

@login_required(login_url='login')  
def view_achievement(request):  
    username = request.user.username  
    user_profile = request.user.userprofile
    
    detail  =  Achievement.objects.filter(rollno=username)   
    detail1 =  Academic_Achievement.objects.filter(rollno=username)   
    detail2 =  Extracurricular_Achievement.objects.filter(rollno=username)   
    detail3 =  placement_Achievement.objects.filter(rollno=username)   
    detail4 =  workshop_Achievement.objects.filter(rollno=username)   

    context = {
        'detail': detail,
        'detail1': detail1,
        'detail2': detail2,
        'detail3': detail3, 
        'detail4': detail4,      
     
            }
    return render(request, 'view_achievement.html', context)   


@login_required(login_url='login')  
def staff_view_achievement(request,username):  
    
    user_profile = request.user.userprofile

    detail  =  Achievement.objects.filter(rollno=username)   
    detail1 =  Academic_Achievement.objects.filter(rollno=username)   
    detail2 =  Extracurricular_Achievement.objects.filter(rollno=username)   
    detail3 =  placement_Achievement.objects.filter(rollno=username)   
    detail4 =  workshop_Achievement.objects.filter(rollno=username)   

    context = {
        'detail': detail,
        'detail1': detail1,
        'detail2': detail2,
        'detail3': detail3, 
        'detail4': detail4,   
        'user_profile': user_profile,   
     
            }
    return render(request, 'staff_view_achievement.html', context)


def about(request):
    return render(request, 'about.html')  


def about_staff(request):
    return render(request, 'about_staff.html')

def logout_view(request):
    logout(request)
    return redirect('login')    

def student_list(request,year):
    students = UserProfile.objects.filter(usertype='student', yearofstudy = year)
    user_profile = request.user.userprofile

    context= {
        'students': students,
        'user_profile': user_profile,   
}  
    return render(request, 'students_list_staff.html', context)




@login_required(login_url='login')  
def updateData(request, pkid):
    mydata = Achievement.objects.get(id=pkid)
    if request.method == 'POST':
        # Handle form submission for updating achievement data
        mydata.date = request.POST['date']
        mydata.title = request.POST['title']
        mydata.description = request.POST['description']
        
        # Check if new photo files are provided and update accordingly
        if 'photo1' in request.FILES:
            mydata.photo1 = request.FILES['photo1']
        if 'photo2' in request.FILES:
            mydata.photo2 = request.FILES['photo2']
        
        # Save the updated achievement data
        mydata.save()
        
        return redirect('view_achievement')  # Redirect to the achievement view page

    context = {'data': mydata}
    return render(request, 'edit_achievement.html', context)



def deleteData(request, pkid):
    mydata = Achievement.objects.get(id=pkid)
    mydata.delete()
    return redirect('view_achievement')   

@login_required(login_url='login')
def student_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    detail = UserProfile.objects.filter(usertype="student", yearofstudy=user_profile.yearofstudy)
    context = {
        'detail': detail
    } 
    return render(request, 'students_list_staff.html', context)   

def generate_pdf(request, username):
    # Fetch user profile
    user_profile = UserProfile.objects.get(user__username=username)

    # Fetch academic achievements
    academic_achievements = Academic_Achievement.objects.filter(rollno=username)

    # Fetch extracurricular achievements
    extracurricular_achievements = Extracurricular_Achievement.objects.filter(rollno=username)

    # Fetch placement achievements
    placement_achievements = placement_Achievement.objects.filter(rollno=username)

    # Fetch workshop achievements
    workshop_achievements = workshop_Achievement.objects.filter(rollno=username)   

    achievements = Achievement.objects.filter(rollno=username)


    # Prepare context data for the template
    context = {
        'user_profile': user_profile,
        'academic_achievements': academic_achievements,
        'extracurricular_achievements': extracurricular_achievements,
        'placement_achievements': placement_achievements,
        'workshop_achievements': workshop_achievements,   
        'achievements': achievements,
    }   

    # Render the template with context data
    template = get_template('pdf_template.html')
    html = template.render(context)

    # Create a PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{username}_achievements.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('PDF generation error.', content_type='text/plain')

    return response         

def generate_pdf_for_all_students(request, year_of_study):
    # Get a queryset of student userids for the specified year of study
    students = UserProfile.objects.filter(yearofstudy=year_of_study, usertype='student')

    # Create a PDF document that combines all individual PDFs
    pdf_writer = PdfWriter()

    for student in students:
        pdf_response = generate_pdf(request, student.userid)
        pdf_reader = PdfReader(BytesIO(pdf_response.content))  # Use PdfReader

        # Add each page of the PDF to the combined PDF
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

    combined_pdf = HttpResponse(content_type='application/pdf')
    combined_pdf['Content-Disposition'] = f'attachment; filename="{year_of_study}_students_achievements.pdf'

    pdf_writer.write(combined_pdf)

    return combined_pdf


@login_required(login_url='login')
def academic_achievement(request):  
        username = request.user.username
        if request.method == 'POST':
            date = request.POST.get('date')
            title = request.POST.get('achievement_type')
            description = request.POST.get('description')
            photo1 = request.FILES.get('photo1')
            photo2 = request.FILES.get('photo2')    
        
            achievement = Academic_Achievement.objects.create(
                user=request.user,  
                rollno = username,
                title=title,
                description=description,
                photo1=photo1,
                photo2=photo2
                # Add other fields as needed
            )   
            admin_info=User.objects.get(is_superuser=True)
            admin_email=admin_info.email
            send_mail(
                'New Academic Achievement added  by  '+username,
                'the '+ username +'  have added the Academic achievement  '+title+'  . please Login to see full information ',
                'balakumaran6111@gmail.com',
                [admin_email],
                fail_silently=False,
                        )

            
            
            return redirect('dashboard')
             
        

        context={
                'username': username,

            }
        return render(request, 'academic_achievement.html', context)   

@login_required(login_url='login')
def extracurricular_achievement(request):  
        username = request.user.username
        if request.method == 'POST':
            date = request.POST.get('date')
            title = request.POST.get('title') 
            position=request.POST.get('achievement_type')
            description = request.POST.get('description')
            photo1 = request.FILES.get('photo1')
            photo2 = request.FILES.get('photo2')    
        
            achievement = Extracurricular_Achievement.objects.create(
                user=request.user,  
                rollno = username,
                title=title, 
                position=position,
                description=description,
                photo1=photo1,
                photo2=photo2 ,
                date=date
                # Add other fields as needed
            )   
          
            admin_info=User.objects.get(is_superuser=True)
            admin_email=admin_info.email
            send_mail(
                'New Extracurricular Achievement added  by  '+username,
                'the '+ username +'  have added Extracurricular  achievement  '+title+'  . please Login to see full information ',
                'balakumaran6111@gmail.com',
                [admin_email],
                fail_silently=False,
                        )
            return redirect('dashboard')

                
        

        context={
                'username': username,

            }
        return render(request, 'extracurricular_achievement.html', context)   


@login_required(login_url='login')
def placement_achievement(request):  
        username = request.user.username
        if request.method == 'POST':
            date = request.POST.get('date')
            title = request.POST.get('title') 
            position=request.POST.get('achievement_type')
            description = request.POST.get('description')
            photo1 = request.FILES.get('photo1')
               
        
            achievement = placement_Achievement.objects.create(
                user=request.user,  
                rollno = username,
                title=title, 
                position=position,
                description=description,
                photo1=photo1,
             
                # Add other fields as needed
            )     
            admin_info=User.objects.get(is_superuser=True)
            admin_email=admin_info.email
            send_mail(
                'New Placement Achievement added  by  '+username,
                'the '+ username +'  have added the Placement achievement  '+title+'  . please Login to see full information ',
                'balakumaran6111@gmail.com',
                [admin_email],
                fail_silently=False,
                        )
            return redirect('dashboard')
             
        

        context={
                'username': username,

            }
        return render(request, 'placement_achievement.html', context)   


@login_required(login_url='login')
def workshop_achievement(request):  
        username = request.user.username
        if request.method == 'POST':
            
            title = request.POST.get('title')    
            title1 = request.POST.get('title1') 
            description = request.POST.get('description')
            fromdate = request.POST.get('fromdate') 
            todate = request.POST.get('todate') 
            days=request.POST.get('days') 
           
           
            photo1 = request.FILES.get('photo1')
            photo2 = request.FILES.get('photo2')

               
        
            achievement = workshop_Achievement.objects.create(
                user=request.user,  
                rollno = username,
                title=title, 
                title1=title1,  
                fromdate=fromdate,
                todate=todate, 
                days=days, 
                description=description,
                photo1=photo1,
                photo2=photo2,
             
                # Add other fields as needed
            )   
            admin_info=User.objects.get(is_superuser=True)
            admin_email=admin_info.email
            send_mail(
                'New Wokrshop  Achievement added  by  '+username,
                'the '+ username +'  have added the workshop achievement  '+title+'  . please Login to see full information ',
                'balakumaran6111@gmail.com',
                [admin_email],
                fail_silently=False,
                        )
            return redirect('dashboard')
             
        

        context={
                'username': username,

            }
        return render(request, 'workshop_achievement.html', context)   


def deleteWorkshopData(request, pkid):
    mydata = workshop_Achievement.objects.get(id=pkid)
    mydata.delete()
    return redirect('view_achievement')    

def deleteExtracurricularData(request, pkid):
    mydata = Extracurricular_Achievement.objects.get(id=pkid)
    mydata.delete()
    return redirect('view_achievement')     


def deletePlacementData(request, pkid):
    mydata = placement_Achievement.objects.get(id=pkid)
    mydata.delete()
    return redirect('view_achievement')     

def deleteAcademicData(request, pkid):
    mydata = Academic_Achievement.objects.get(id=pkid)
    mydata.delete()
    return redirect('view_achievement')      


@login_required(login_url='login')  
def updateAcademicData(request, pkid):
    mydata = Academic_Achievement.objects.get(id=pkid)
    if request.method == 'POST':
        # Handle form submission for updating achievement data
        
        mydata.title = request.POST['achievement_type']
        mydata.description = request.POST['description']
        
        # Check if new photo files are provided and update accordingly
        if 'photo1' in request.FILES:
            mydata.photo1 = request.FILES['photo1']
        if 'photo2' in request.FILES:
            mydata.photo2 = request.FILES['photo2']
        
        # Save the updated achievement data
        mydata.save()
        
        return redirect('view_achievement')  # Redirect to the achievement view page

    context = {'data': mydata}
    return render(request, 'edit_academic_achievement.html', context)



@login_required(login_url='login')  
def updateExtracurricularData(request, pkid):
    mydata =  Extracurricular_Achievement.objects.get(id=pkid)
    if request.method == 'POST':
        # Handle form submission for updating achievement data
        
        mydata.title = request.POST['position_type']
        mydata.description = request.POST['description']
        
        # Check if new photo files are provided and update accordingly
        if 'photo1' in request.FILES:
            mydata.photo1 = request.FILES['photo1']
        if 'photo2' in request.FILES:
            mydata.photo2 = request.FILES['photo2']
        
        # Save the updated achievement data
        mydata.save()
        
        return redirect('view_achievement')  # Redirect to the achievement view page

    context = {'data': mydata}
    return render(request, 'edit_extracurricular_achievement.html', context)


@login_required(login_url='login')  
def updatePlacementData(request, pkid):
    mydata =   placement_Achievement.objects.get(id=pkid)
    if request.method == 'POST':
        # Handle form submission for updating achievement data
        
        mydata.title = request.POST['title']
        mydata.description = request.POST['description']
        mydata.position=request.POST['achievement_type']
        # Check if new photo files are provided and update accordingly
        if 'photo1' in request.FILES:
            mydata.photo1 = request.FILES['photo1']
        if 'photo2' in request.FILES:
            mydata.photo2 = request.FILES['photo2']
        
        # Save the updated achievement data
        mydata.save()
        
        return redirect('view_achievement')  # Redirect to the achievement view page

    context = {'data': mydata}
    return render(request, 'edit_placement_achievement.html', context)


@login_required(login_url='login')  
def updateworkshopData(request, pkid):
    mydata =workshop_Achievement.objects.get(id=pkid)
    if request.method == 'POST':
        # Handle form submission for updating achievement data
        
        mydata.title = request.POST['title']
        mydata.title1 = request.POST['title1']
        mydata.description = request.POST['description']
        mydata.fromdate = request.POST.get('fromdate') 
        mydata.todate = request.POST.get('todate') 
        mydata.days=request.POST.get('days') 

        # Check if new photo files are provided and update accordingly
        if 'photo1' in request.FILES:
            mydata.photo1 = request.FILES['photo1']
        if 'photo2' in request.FILES:
            mydata.photo2 = request.FILES['photo2']
        
        # Save the updated achievement data
        mydata.save()
        
        return redirect('view_achievement')  # Redirect to the achievement view page

    context = {'data': mydata}
    return render(request, 'edit_workshop_achievement.html', context)
