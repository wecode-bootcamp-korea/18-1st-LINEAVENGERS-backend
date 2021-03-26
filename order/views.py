import json
from json.decoder import JSONDecodeError
from datetime     import datetime

from django.views                 import View
from django.http                  import JsonResponse, request
from django.db                    import transaction
from django.db.models.query_utils import Q

from account.models import User
from product.models import Product, Size, ProductImage
from order.models   import Cart, Order
from account.utils  import token_decorator
from mypage.models  import Review

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
            CART_IN  = 1
            ORDER_IN = 2

            if not Size.objects.filter(id=size_id).exists():
                return JsonResponse({"message": "INVALID_SIZE"}, status = 400)
            if Order.objects.filter(id=order_id, order_status=CART_IN).exists():
                Cart.objects.filter(order_id=order_id, product_id=product_id).delete()
            order = Order.objects.create(
                user            = User.objects.get(id=user_id),
                order_status_id = ORDER_IN,
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
                Order.objects.create(
                    order_status_id = CART_IN,
                    user = User.objects.get(id=user_id)
                )
            order = Order.objects.get(user_id=user_id, order_status=CART_IN)

            cart, created = Cart.objects.get_or_create(
                product  = Product.objects.get(id=product_id),
                order    = order,
                size     = Size.objects.get(id=size_id)
            )
            if created:
                cart.quantity = 0
            cart.quantity += quantity
            cart.save()

            return JsonResponse({'message':'SUCCESS'}, status = 201)                    
        except KeyError:
            return JsonResponse({"message": "KEY ERROR"}, status = 400)
        except Cart.DoesNotExist:
            return JsonResponse({"message": "DoesNotExist ERROR"}, status = 400)
        except Cart.MultipleObjectsReturned:
            return JsonResponse({"message": "MultipleObjectsReturned ERROR"}, status = 400)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)
    
    @token_decorator
    def delete(self, request, product_id):
        try:
            order = Order.objects.get(user=request.user, order_status_id=1)
            Cart.objects.get(order_id=order.id, product_id=product_id).delete()

            return JsonResponse({"message":"SUCCESS"}, status = 201)
            
        except Cart.DoesNotExist:
            return JsonResponse({"message":"NONE_CART"}, status = 400)
        except Cart.MultipleObjectsReturned:
            return JsonResponse({"message":"NONE_CART"}, status = 400)
    
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

    @token_decorator
    def get(self, request):
        
        if not Order.objects.filter(user=request.user, order_status_id=1):
            result = [{}]
            return JsonResponse({'result':result}, status = 200)
        else:
            order = Order.objects.get(user=request.user, order_status_id=1)

        carts = order.cart_set.all()

        result = [{
            'order_id'      :order.id,
            'product_id'    :cart.product.id,
            'name'          :cart.product.name,
            'price'         :int(cart.product.price),
            'image'         :cart.product.productimage_set.filter(is_thumbnail=True)[0].image_url if cart.product.productimage_set.filter(is_thumbnail=True) else "" ,
            'quantity'      :cart.quantity,
            'discount'     :int(cart.product.discount_rate),
            'deliveryprice':3000 if cart.product.is_free_shipping else 0
        } for cart in carts]

        return JsonResponse({'result':result}, status = 200)
        
class ReviewView(View):
    @token_decorator
    def post(self, request):
        data = json.loads(request.body)

        content = data['content']
        rating  = int(data['rating'])
        product = Product.objects.get(id=data['product'])

        Review.objects.create(content=content, rating=rating, product=product, user=request.user)

        return JsonResponse({"message":"SUCCESS"}, status = 201)

    @token_decorator
    def get(self, request):
        user_id      = request.user_id
        product_list = []
        orders       = Order.objects.filter(Q(user_id=user_id) & ~Q(order_status=1))
        for order in orders:
            product_list +=[{
                'order_id'      : order.id,
                'create_at'     : datetime.strftime(order.create_at, "%Y-%m-%d %H:%M:%S"),
                'quantity'      : cart.quantity,
                'size_id'       : cart.size.id,
                'size_name'     : cart.size.name,
                'product_id'    : cart.product.id,
                'product_name'  : cart.product.name,
                'thumbnail_url' : ProductImage.objects.get(Q(product=cart.product.id)&Q(is_thumbnail='1')).image_url,
                'price'         : int(cart.product.price),
                'order_status'  : order.order_status.name
            } for cart in Cart.objects.filter(order_id=order.id)]
            
        return JsonResponse({'product_list':product_list}, status=200)

