import json
from json.decoder import JSONDecodeError

from django.views                 import View
from django.http                  import JsonResponse, request
from django.db                    import transaction
from django.db.models.query_utils import Q

from account.models import User
from product.models import Product, Size
from order.models   import Cart, Order
from account.utils  import token_decorator

class OrderView(View):
    @token_decorator
    @transaction.atomic
    def post(self, request, product_id):        
        try:
            data     = json.loads(request.body)        
            user_id  = request.user.id
            size_id  = int(data['size_id'])
            quantity = int(data['quantity'])
            order_id = int(data.get('order_id', None))

            if not Size.objects.filter(id=size_id).exists():
                return JsonResponse({"message": "INVALID_SIZE"}, status = 400)
            if Order.objects.filter(id=order_id, order_status=1).exists():
                Cart.objects.filter(order_id=order_id, product_id=product_id).delete()
            order = Order.objects.create(
                user            = User.objects.get(id=user_id),
                order_status_id = 2,
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

class CartView(View):
    @token_decorator
    @transaction.atomic
    def post(self, request, product_id):        
        try:
            data     = json.loads(request.body)        
            user_id  = request.user.id
            size_id  = int(data['size_id'])
            quantity = int(data['quantity'])
            CART_IN  = 1

            if not Size.objects.filter(id=size_id).exists():
                return JsonResponse({"message": "INVALID SIZE"}, status = 400)
            if not Order.objects.filter(user_id=user_id, order_status=CART_IN).exists():
                order = Order.objects.create(
                    order_status_id = CART_IN,
                    user = User.objects.get(id=user_id)
                )
            else:
                order = Order.objects.get(user_id=user_id, order_status=CART_IN)
                            
            Cart.objects.create(
                quantity = quantity,
                product  = Product.objects.get(id=product_id),
                order    = order,
                size     = Size.objects.get(id=size_id)
            )
            return JsonResponse({'message':'SUCCESS'}, status = 201)                    
        except KeyError:
            return JsonResponse({"message": "KEY ERROR"}, status = 400)
        except Cart.DoesNotExist:
            return JsonResponse({"message": "DoesNotExist ERROR"}, status = 400)
        except Cart.MultipleObjectsReturned:
            return JsonResponse({"message": "MultipleObjectsReturned ERROR"}, status = 400)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)

class CartOrderView(View):
    @token_decorator
    def post(self, request):        
        try:
            data     = json.loads(request.body)        
            user_id  = request.user.id
            order_id = int(data['order_id'])
            IN_CART  = 1

            order = Order.objects.get(Q(id=order_id) & Q(user_id=user_id))
            if not order.order_status_id == IN_CART:
                return JsonResponse({"message": "INVALID_STATUS"}, status = 400)
            Order.objects.filter(user_id=user_id, id=order_id).update(order_status_id=2)
            return JsonResponse({'message':'SUCCESS'}, status = 201)                    
        except KeyError:
            return JsonResponse({"message": "KEY ERROR"}, status = 400)
        except Order.DoesNotExist:
            return JsonResponse({"message": "NOT EXIST"}, status = 400)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)