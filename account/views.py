import json
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse

from .models     import User
from my_settings import SECRET_KEY, ALGORITHM

class UserSignUp(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            login_id     = data['login_id']
            password     = data['password']
            name         = data['name']
            phone_number = data['phone_number']
            email        = data['email']

            if not login_id.isalnum():
                return JsonResponse({"message":"No TUCKSOOMUNJA"}, status = 400)

            if len(password) < 8:
                return JsonResponse({"message":"More than 8 letters PLEASE."}, status = 400)

            if ('@' not in email) or ('.' not in email):
                return JsonResponse({"message":"Put @ and . in email PLEASE."}, status = 400)

            password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode

            User.objects.create(login_id=login_id, password=password, name=name, phone_number=phone_number, email=email)

            return JsonResponse({'message':'SUCESS'}, status = 200)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "json.decoder.JSONDecodeError"}, status = 400)