import json
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse

from .models     import User
from my_settings import SECRET_KEY, ALGORITHM

MIN_PASSWORD_LENGTH = 8

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
                return JsonResponse({"message":"INVALID_CHARACTER"}, status = 400)
            
            if User.objects.filter(login_id=login_id).exists():
                return JsonResponse({"message":"USER_NAME_ALREADY_EXITS"}, status = 400)

            if len(password) < MIN_PASSWORD_LENGTH:
                return JsonResponse({"message":"SHORT_PASSWORD"}, status = 400)

            if ('@' not in email) or ('.' not in email):
                return JsonResponse({"message":"INVALID_EMAIL"}, status = 400)

            phone_number = phone_number.replace('-', '')

            password_hashed = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
            
            User.objects.create(
                login_id=login_id,
                password=password_hashed, 
                name=name, phone_number=phone_number, 
                email=email, 
                is_active=True
            )

            return JsonResponse({'message':'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "INVALID_JSON"}, status = 400)

class UserSignIn(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            login_id = data["login_id"]
            password = data["password"]

            user = User.objects.get(login_id=login_id)
            
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                if user.is_active:
                    access_token = jwt.encode({'id':user.id}, SECRET_KEY, ALGORITHM)
                    return JsonResponse({"message":"SUCCESS", 'access_token':access_token}, status = 200)
                else:
                    return JsonResponse({"message":"NONE_CERTIFICATION"}, status = 401)
            else:
                return JsonResponse({"message":"INVALID_USER"}, status = 400)
        
        
        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status = 400)

        except User.MultipleObjectsReturned:
            return JsonResponse({"message":"INVALID_USER"}, status = 400)
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "INVALID_JSON"}, status = 400)