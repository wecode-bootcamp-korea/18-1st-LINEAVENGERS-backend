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
        order = Order.objects.get(user=request.user, order_status_id=1)

        k = order.cart_set.all()

        # for i in k:
        #     my_dict = {'name':i.product.name 

        # result = [{
        #     'name':i.product.name,
        #     'price':i.product.price,
        #     'image':i.product.productimage_set.filter(is_thumbnail=True).image_url,
        #     'quantity':i.quantity,
        #     'size':i.size.name,
        #     'deliveryprice':i.product.
        # } for i in k]

        for i in k:
            if i.product.is_free_shipping:
                deliveryprice:0
            

            

        

        
