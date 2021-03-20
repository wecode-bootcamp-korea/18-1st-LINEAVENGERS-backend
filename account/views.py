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
                return JsonResponse({"message":"No Special Characters."}, status = 400)
            
            if User.objects.filter(login_id=login_id).exists():
                return JsonResponse({"message":"USER_NAME_ALREADY_EXITS"}, status = 400)

            if len(password) < 8:
                return JsonResponse({"message":"More than 8 letters PLEASE."}, status = 400)

            if ('@' not in email) or ('.' not in email):
                return JsonResponse({"message":"Put @ and . in email PLEASE."}, status = 400)

            phone_number = phone_number.replace('-', '')

            password_hashed = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
            
            User.objects.create(login_id=login_id, password=password_hashed, name=name, phone_number=phone_number, email=email)

            u1 = User.objects.get(login_id=login_id).is_active

            u1 = True

            return JsonResponse({'message':'SUCCESS'}, status = 200)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "json.decoder.JSONDecodeError"}, status = 400)

class UserSignIn(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            login_id = data["login_id"]
            password = data["password"]

            if User.objects.filter(login_id=login_id).exists():
                user_password = User.objects.get(login_id=login_id).password
                user_id       = User.objects.get(login_id=login_id).id
                user_active     = User.objects.get(login_id=login_id).is_active

                if bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8')):
                    if user_active:
                        access_token = jwt.encode({'id':user_id}, SECRET_KEY, ALGORITHM)
                        return JsonResponse({"message":"SUCCESS", 'access_token':access_token}, status = 200)
                    else:
                        return JsonResponse({"message":"please inzoong"}, status = 400)
                else:
                    return JsonResponse({"message":"INVALID_USER"}, status = 401)    
            else:
                return JsonResponse({"message":"INVALID_USER"}, status = 401)
            
        except DoesNotExist:
            return JsonResponse({"message":"djqtek"}, status = 400)

        except MultipleObjectsReturned:
            return JsonResponse({"message":"aksgek"}, status = 400)
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "json.decoder.JSONDecodeError"}, status = 400)