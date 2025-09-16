from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserStatus
from django.utils import timezone
from .models import UserLoginLog
from .models import UserIPLog
import json
from django.http import HttpResponse
import socket
from django.http import HttpResponse
def get_local_ip(request):
    # This gets the actual local IP address of your machine, even on localhost
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return None
def home_view(request):
    return render(request,'home.html')


def register_view(request):
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        password2=request.POST.get('password2')

        if not username or not password or not password2 or not email or not first_name or not last_name:
            messages.error(request,'Please fill all the details')
            return render(request,'register.html')
        
        if password != password2:
            messages.error(request,'Passwords do not match')
            return render(request,'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username taken')
            return render(request,'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email taken')
            return render(request,'register.html')   

        user=User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
        user.save()
        messages.success(request,'User created')
        return redirect('login')
    else:
        return render(request,'register.html')     
        

def login_view(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        # data = json.loads(request.body)
        # local_ip = data.get('public_ip')
        # ip = get_client_ip(request)
        local_ip =  get_local_ip(request) # 👈 This will now have 192.168.x.x
        print(f"Login attempt from IP: {local_ip}")
        now= timezone.now()

        user=authenticate(request,username=username,password=password)
        if user is not None:
            try:
                presence = UserStatus.objects.get(username=username)
            except UserStatus.DoesNotExist:
                messages.error(request, "Access denied: No presence record found.")
                return render(request, 'login.html')
        
            if presence.status == 'in':
                login(request, user)
                email = user.email
                first_name = user.first_name
                last_name = user.last_name
                last_login = user.last_login
                UserLoginLog.objects.create(
                username=username,
                status='in',
                ip_address=local_ip,
                timestamp=now,
                email=email,
                first_name=first_name,
                last_name=last_name,
                last_login=last_login)

                
                return render(request,'login_success.html',{'username':username})

            else:
                messages.error(request, "Access denied: You must be in the office to log in.")
                return render(request, 'login.html')
        

        else:
            messages.error(request,'Invalid credentials')
            return render(request,'login.html')
    else:
        return render(request,'login.html')   


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'username': request.user.username})

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            'activities': [
                'Logged in',
                'Updated profile',
                'Changed password',
            ],
        }
        return Response(data)




from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# @csrf_exempt
# def receive_ip(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             public_ip = data.get('public_ip')
#             print(f"Received IP: {public_ip}")  # Check this in your console
#             if public_ip:
#                 UserIPLog.objects.create(ip_address=public_ip)
#                 return JsonResponse({'status': 'success'})
#             else:
#                 print("No IP found in data")
#                 return JsonResponse({'error': 'No IP provided'}, status=400)
#         except Exception as e:
#             print(f"Error in receive_ip: {e}")
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#     return JsonResponse({'error': 'Invalid request'}, status=400)
