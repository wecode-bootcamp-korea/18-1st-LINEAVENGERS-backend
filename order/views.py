import jwt
import json
import bcrypt

from django.views import View
from django.http  import JsonResponse

from .models       import User
from my_settings   import SECRET_KEY, ALGORITHM, EMAIL
from account.utils import token_decorator
from order.models  import Cart, Order

class CartList(View):                          
    @token_decorator
    def get(self, request):
        order = Order.objects.get(user=request.user, order_status_id=1)

        carts = order.cart_set.all()

        cart_delivery_3000 = [{
            'name':cart.product.name,
            'price':cart.product.price,
            'image':cart.product.productimage_set.filter(is_thumbnail=True)[0].image_url,
            'quantity':cart.quantity,
            'size':cart.size.name,
            'deliveryprice':3000,
        } for cart in carts if not cart.product.is_free_shipping]

        cart_delivery_0 = [{
            'name':cart.product.name,
            'price':cart.product.price,
            'image':cart.product.productimage_set.filter(is_thumbnail=True)[0].image_url,
            'quantity':cart.quantity,
            'size':cart.size.name,
            'deliveryprice':0,
        } for cart in carts if cart.product.is_free_shipping]

        result = cart_delivery_3000 + cart_delivery_0

        return JsonResponse({'result':result}, status = 200)