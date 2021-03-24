import json
import bcrypt
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

    # @token_decorator
    def get(self, request):
        favorites = Favorite.objects.filter(user_id='1', is_favorite=True)
        
        result = [{'name':favorite.product.name, 'price':favorite.product.price, 'image':list(favorite.product.productimage_set.all().values())} for favorite in favorites]
        
        # result = [product = Product.objects.get(id=favorite_product['product'])
        # {'name':product.name, 'price':product.price, 'image':ProductImage.objects.get()} 
        # for favorite_product in favorite_products]
        # for favorite in favorites:
        #     favorite_dict = {
        #         'product' : favorite.product,
        #     }

        #     favotrite_product.append(favorite_dict)
        
        # result = []
        # print('=============================================', favorite_products)

        # for i in favorite_products:
        #     product = Product.objects.get(i['product'])
            
        #     k = {
        #         'name' : product.name,
        #         'price' : product.price,
        #         'image' : ProductImage.objects.get(product=product).image_url,
        #     }

        #     result.append(k)

        return JsonResponse({"result":result}, status = 200)
            
class ReviewView(View):
    # @token_decorator
    def post(self, request):
        data = json.loads(request.body)

        content = data['content']
        rating  = data['rating']
        product = Product.objects.get(id=data['product'])

        Review.objects.create(content=content, rating=rating, product=product, user_id='2')

        return JsonResponse({"message":"SUCCESS"}, status = 200)
