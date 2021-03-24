import jwt
import json
import bcrypt

from django.views import View
from django.http  import JsonResponse

from .models       import User
from my_settings   import SECRET_KEY, ALGORITHM, EMAIL
from account.utils import token_decorator
from order.models  import Cart, Order

class Cart(View):                           # 이름 고쳐야함
    @token_decorator
    def get(self, request):
        # orders = request.user.order_set.filter(order_status=1)
        orders = Order.objects.filter(user=request.user, order_status_id=1)

        order_cart = [order for order in orders]

        for orde in order_cart:
            Cart.objects.filter(order=orde) 
        
