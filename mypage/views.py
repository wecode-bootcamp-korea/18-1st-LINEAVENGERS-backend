import json
import bcrypt
from django.db.models.query_utils import Q
import jwt

from django.views import View
from django.http  import JsonResponse

from account.models import User
from account.utils  import token_decorator
from product.models import Product, ProductImage
from mypage.models  import Favorite, Review

class FavoriteView(View):
    @token_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            product = data['product_id']
            product = Product.objects.get(id=product)

            if Favorite.objects.filter(Q(user=request.user)&Q(product_id=product.id)).exists():
                favorite_user = Favorite.objects.get(Q(user_id=request.user.id)&Q(product_id=product.id))

                if favorite_user.is_favorite:
                    favorite_user.is_favorite = False
                    favorite_user.save()
                    return JsonResponse({'message':'SUCCESS'}, status = 201)

                favorite_user.is_favorite = True
                favorite_user.save()
                return JsonResponse({'message':'SUCCESS'}, status = 201)
            
            Favorite.objects.create(
                is_favorite = True,
                user        = request.user,
                product     = product,
            )
            return JsonResponse({'message':'SUCCESS'}, status = 201)
        except Favorite.DoesNotExist:
            return JsonResponse({'message':'DoesNotExist ERROR'}, status = 400)

    @token_decorator
    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user, is_favorite=True)
        
        result = [{
            'name':favorite.product.name,
            'user_name':favorite.user.name,
            'price':int(favorite.product.price),
            'image':favorite.product.productimage_set.filter(is_thumbnail=True)[0].image_url if favorite.product.productimage_set.filter(is_thumbnail=True) else ""
        } for favorite in favorites]
        
        return JsonResponse({"result":result}, status = 200)