import json
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse

from product.models import Product
from mypage.models import Favorite

# @decorator
class Favorite(View):
    def post(self, request):
        data = json.loads(request.body)
        
        product = data['product']
        product = Product.objects.get(id=product)

        if Favorite.objects.filter(id=request.user_id).exists():
            favorite_user = Favorite.objects.get(id=request.user_id)

            if favorite_user.is_favorite:
                favorite_user.is_favorite = False
                favorite_user.save()
            
            favorite_user.is_favorite = True
            favorite_user.save()

            return JsonResponse({'message':'SUCCESS'}, status = 200)
        
        Favorite.objects.create(
            is_favorite=True,
            user=request.user,
            product=product,
        )

