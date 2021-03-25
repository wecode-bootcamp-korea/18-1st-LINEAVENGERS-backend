import json
import bcrypt
import jwt
from datetime import datetime

from django.views                 import View
from django.http                  import JsonResponse
from django.db.models.query_utils import Q

from account.models import User
from account.utils  import token_decorator
from product.models import Product, ProductImage
from mypage.models  import Favorite, Review
from order.models   import Order, Cart

class FavoriteView(View):
    @token_decorator
    def post(self, request):
        data = json.loads(request.body)
        
        product = data['product']
        product = Product.objects.get(id=product)

        if Favorite.objects.filter(user=request.user).exists():
            favorite_user = Favorite.objects.get(id=request.user.id)

            if favorite_user.is_favorite:
                favorite_user.is_favorite = False
                favorite_user.save()
                return JsonResponse({'message':'SUCCESS'}, status = 200)

            favorite_user.is_favorite = True
            favorite_user.save()

            return JsonResponse({'message':'SUCCESS'}, status = 200)
        
        Favorite.objects.create(
            is_favorite=True,
            user=user,
            product=product,
        )

        return JsonResponse({'message':'SUCCESS', }, status = 200)

    @token_decorator
    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user, is_favorite=True)
        
        result = [{
            'name':favorite.product.name,
            'user_name':favorite.user.name,
            'price':int(favorite.product.price),
            'image':favorite.product.productimage_set.filter(is_thumbnail=True)[0].image_url
        } for favorite in favorites]
        
        return JsonResponse({"result":result}, status = 200)
        
class ReviewView(View):
    @token_decorator
    def post(self, request):
        data = json.loads(request.body)

        content = data['content']
        rating  = data['rating']
        product = Product.objects.get(id=data['product'])

        Review.objects.create(content=content, rating=rating, product=product, user=request.user)

        return JsonResponse({"message":"SUCCESS"}, status = 200)

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
