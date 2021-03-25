import jwt
import json
from django.http import JsonResponse

from my_settings    import SECRET_KEY, ALGORITHM
from account.models import User

def token_decorator(func):
    def wrapper(self, request, *arg, **karg):
        try:
            if "Authorization" not in request.headers:
                return JsonResponse({'message':'no authorization'}, status = 400)
        
            token         = request.headers["Authorization"]
            token_decoded = jwt.decode(token, SECRET_KEY, ALGORITHM)

            user            = User.objects.get(id=token_decoded['id'])
            request.user    = user
            request.user_id = user.id

            return func(self, request, *arg, **karg)
            
        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status = 400)

        except User.MultipleObjectsReturned:
            return JsonResponse({"message":"INVALID_USER"}, status = 400)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "INVALID_JSON"}, status = 400)

    return wrapper

def status_decorator(func):
    def wrapper(self, request, *arg, **karg):
        try:            
            token = request.headers.get("Authorization", None)
            if token :
                token_decoded = jwt.decode(token, SECRET_KEY, ALGORITHM)
                user          = User.objects.get(id=token_decoded['id'])
                request.user_id = user.id
            else:
                request.user_id = None

            return func(self, request, *arg, **karg)            
        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status = 400)
        except User.MultipleObjectsReturned:
            return JsonResponse({"message":"INVALID_USER"}, status = 400)        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "INVALID_JSON"}, status = 400)
    return wrapper