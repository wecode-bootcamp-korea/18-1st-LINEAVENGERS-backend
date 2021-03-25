import jwt
import json
import bcrypt

from django.views                   import View
from django.http                    import JsonResponse
from django.shortcuts               import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http              import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail               import EmailMessage
from django.utils.encoding          import force_text, force_bytes
from django.core.exceptions         import ValidationError

from .models                  import User
from .text                    import message 
from my_settings              import SECRET_KEY, ALGORITHM, EMAIL

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
                return JsonResponse({"message":"INVALID_LOGIN_ID"}, status = 400)

            if len(password) < MIN_PASSWORD_LENGTH:
                return JsonResponse({"message":"SHORT_PASSWORD"}, status = 400)

            if ('@' not in email) or ('.' not in email):
                return JsonResponse({"message":"INVALID_EMAIL"}, status = 400)

            phone_number = phone_number.replace('-', '')

            password_hashed = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
            
            user = User.objects.create(
                login_id=login_id,
                password=password_hashed, 
                name=name, 
                phone_number=phone_number, 
                email=email,
            )

            current_site = get_current_site(request)
            domain       = current_site.domain
            uidb64       = urlsafe_base64_encode(force_bytes(user.id))
            token        = jwt.encode({'user_id':user.id}, SECRET_KEY, ALGORITHM)
            
            message_data = message(domain, uidb64, token)
            mail_title   = '이메일 인증을 완료해 주세요.'
            mail_to      = data['email']

            email = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()

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
                    return JsonResponse({"message":"SUCCESS", 'access_token':access_token, 'name':user.name, 'email':user.email}, status = 200)
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

class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid           = force_text(urlsafe_base64_decode(uidb64))
            user          = User.objects.get(id=uid)
            token_decoded = jwt.decode(token, SECRET_KEY, ALGORITHM)
        
            if token_decoded['user_id'] == user.id:
                user.is_active = True
                user.save()

                return redirect(EMAIL['REDIRECT_PAGE'])
            
            return JsonResponse({'message':'AUTH_FAIL'}, status = 400)

        except ValidationError:
            return JsonResponse({"message":"TYPE_ERROR"}, status = 400)
            
        except KeyError:
            return JsonResponse({"message":"INVALID_KEY"},  status = 400)

class LoginIdExist(View):
    def post(self, request):
        data = json.loads(request.body)

        login_id = data['login_id']
        
        if User.objects.filter(login_id=login_id).exists():

            return JsonResponse({'message':'INVALID_LOGINID'}, status = 400)
        
        return JsonResponse({'message':'SUCCESS'}, status = 200)
