import json
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse

from account.models import User
from product.models import Product
from mypage.models  import Favorite, Review
from order.models   import Order

# @decorator
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

        return JsonResponse({'message':'SUCCESS'}, status = 200)

class ReviewCreate(View):
    def post(self, request):
        data = json.loads(request.body)

        content = data['content']
        rating  = data['rating']
        oder    = data['order']
        order   = Order.objects.get(id=order)

        Review.objects.create(content=content, rating=rating, order=order)