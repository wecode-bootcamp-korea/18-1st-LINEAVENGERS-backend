import json
from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse, request

from account.models import User
from product.models import Product, Size
from order.models   import Cart, Order
#from account.utils  import token_decorator

class CartView(View):
    #@token_decorator
    def post(self, request):
        
        try:
            data = json.loads(request.body)
        
            #user_id = request.user.id  
            user_id    = data['userId']
            product_id = data['productId']
            size_id    = data['sizeId']
            quantity   = data['quantity']

            if Order.objects.filter(user_id=user_id, order_status=1).exists():
                order = Order.objects.filter(user_id=user_id, order_status=1).last()
            else:
                order = Order.objects.create(
                    order_status_id = 1,
                    user = User.objects.get(id=user_id)
                )
            
            Cart.objects.create(
                quantity = quantity,
                product  = Product.objects.get(id=product_id),
                order    = order,
                size     = Size.objects.get(id=size_id)
            )

            return JsonResponse({'message':'SUCCESS'}, status = 201)            
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)
        except Exception as e:
            print(e)