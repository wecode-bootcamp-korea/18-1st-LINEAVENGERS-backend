import json
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse

from account.models import User
# from account.utils  import token_decorator
from product.models import Product, ProductImage
from mypage.models  import Favorite, Review

# @token_decorator
class FavoriteView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        user    = data['user']
        user    = User.objects.get(id=user)
        product = data['product']
        product = Product.objects.get(id=product)

        if Favorite.objects.filter(user_id=user.id).exists():
            favorite_user = Favorite.objects.get(id=user.id)

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

    def get(self, request, user_id):
        


# @token_decorator
class ReviewView(View):
    def post(self, request):
        data = json.loads(request.body)

        content = data['content']
        rating  = data['rating']
        product = Product.objects.get(id=data['product'])
        user    = User.objects.get(id=data['user'])

        Review.objects.create(content=content, rating=rating, product=product, user=user)
 
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        image = ProductImage.objects.get(product=product)

        product_dict = {
            'name' : product.name,
            'img'  : image.image_url,
        }

        return JsonResponse({'result':product_dict}, status = 200)

# @token_decorator
# class FavoriteView(View):
#     def get(self, request):
#         data = json.loads(request.body)

#         user = data['id']
#         user = User.objects.get(id=user)

#         favorite = Favorite.objects.filter(user_id=user.id)
        
#         result = {}

#         for i in favorite:
#             favorite_dict = {

#             }