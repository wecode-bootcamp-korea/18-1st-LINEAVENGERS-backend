import jwt
import json
import bcrypt

from django.views import View
from django.http  import JsonResponse

from .models        import User
from my_settings    import SECRET_KEY, ALGORITHM, EMAIL
from account.utils  import token_decorator
from order.models   import Cart, Order

class CartList(View):                          
    @token_decorator
    def get(self, request):
        order = Order.objects.get(user=request.user, order_status_id=1)

        carts = order.cart_set.all()

        result = [{
            'product_id':cart.product.id,
            'name':cart.product.name,
            'price':int(cart.product.price),
            'image':cart.product.productimage_set.filter(is_thumbnail=True)[0].image_url,
            'quantity':cart.quantity,
            'discount':int(cart.product.discount_rate),
            'deliveryprice':3000 if cart.product.is_free_shipping else 0,
        } for cart in carts]

        return JsonResponse({'result':result}, status = 200)

class CartDetailView(View):
    @token_decorator
    def delete(self, request, product_id):
        try:
            order = Order.objects.get(user=request.user, order_status_id=1)
            Cart.objects.get(order_id=order.id, product_id=product_id).delete()

            return JsonResponse({"message":"SUCCESS"}, status = 200)
        
        except Cart.DoesNotExist:
            return JsonResponse({"message":"NONE_CART"}, status = 400)

        except Cart.MultipleObjectsReturned:
            return JsonResponse({"message":"NONE_CART"}, status = 400)