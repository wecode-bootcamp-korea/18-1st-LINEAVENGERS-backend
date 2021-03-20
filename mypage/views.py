import json
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse

from product.models import Product
from mypage.models import Favorite

@decorator
class Favorite(View):
def post(self, request):
data = json.loads(request.body)

if Favorite.objects.filter(id=request.user_id).exists():
Favorite.objects.get(id=request.user_id)

