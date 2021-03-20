def token_decorator(func):
    def wrapper(self, request, *arg, **karg):
        try:
            if not request.headers["Authorization"].exists():
                return JsonResponse({'message':'no authorization'}, status = 400)
        
            request.token = request.headers["Authorization"]
            token_decoded = jwt.decode(token, SECRET_KEY, ALGORITHM)
        
            request.user    = User.objects.get(id=token_decoded['id'])
            request.user_id = user['id']

            return func(self, request, *arg, **karg)
            
        except DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status = 400)

        except MultipleObjectsReturned:
            return JsonResponse({"message":"INVALID_USER"}, status = 400)
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "INVALID_JSON"}, status = 400)

    return wrapper