import json
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse

from account.models import User
# from account.utils  import token_decorator
from product.models import Product
from mypage.models  import Favorite, Review

# @token_decorator
class FavoriteCreate(View):
    def post(self, request):
        data = json.loads(request.body)
        
        user    = data['user']
        user    = User.objects.get(id=user)
        product = data['product']
        product = Product.objects.get(id=product)

        if Favorite.objects.filter(user_id=user.id).exists():
            favorite_user = Favorite.objects.get(id=user.id)

            if favorite_user.is_favorite:
                favorite_user.is_favorite = Falseorder=order
                return JsonResponse({'message':'SUCCESS'}, status = 200)

            favorite_user.is_favorite = True
            favorite_user.save()

            return JsonResponse({'message':'SUCCESS'}, status = 200)
        
        Favorite.objects.create(
            is_favorite=True,
            user=user,
            product=product,
        )

        return JsonResponse({'message':'SUCCESS'}, status = 200)

# @token_decorator
class ReviewCreate(View):
    def post(self, request):
        data = json.loads(request.body)

        content = data['content']
        rating  = data['rating']
        product = Product.objects.get(id=data['product'])
        user    = User.objects.get(id=data['user'])

        Review.objects.create(content=content, rating=rating, product=product, user=user)


