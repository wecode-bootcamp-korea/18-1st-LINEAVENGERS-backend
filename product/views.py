import json
from datetime      import datetime

from django.conf.urls       import url
from django.db.models.query import QuerySet
from mypage.models          import Question, Review, ReviewImage, ReviewRecommand
from json.decoder           import JSONDecodeError

from django.http                  import JsonResponse, request
from django.views                 import View
from django.db.models.query_utils import Q
from django.db.models             import Count, Avg

from product.models import (
    Category, 
    Menu, 
    Product, 
    ProductImage, Size, Type)
from mypage.models  import Favorite 
from account.utils  import token_decorator, status_decorator
from order.models   import Cart, Order

class MainCategoryView(View):
    def get(self, request):
        menu_list = [
            {
                "menuId"      : menu.id,
                "menuName"    : menu.name,
                "categoryList": [{
                    "categoryId"  :category.id,
                    "categoryName":category.name
                } for category in Category.objects.filter(menu=menu)]
            } for menu in Menu.objects.all()]
        return JsonResponse({'menuList':menu_list}, status=200)

class MainProductView(View):
    @status_decorator
    def get(self, request):
        try:
            product_list = [
            {
                'productId'    : product.id,
                'thumbnailUrl' : ProductImage.objects.filter(Q(product=product)&Q(is_thumbnail='1')).first().image_url if ProductImage.objects.filter(Q(product=product)&Q(is_thumbnail='1')) else "",
                'type'         : product.type.name,
                'productName'  : product.name,
                'price'        : {
                                "normal" : "{:,}".format(int(product.price)),
                                "sale"   : int(product.discount_rate)
                                },
                'review'       : Review.objects.filter(product_id=product.id).aggregate(count=Count('id'))["count"] if Review.objects.filter(product_id=product.id) else 0,
                'rating'       : Review.objects.filter(product_id=product.id).aggregate(rating=Avg('rating'))["rating"] if Review.objects.filter(product_id=product.id) else 0,
                'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                'favorite'     : Favorite.objects.filter(user_id=1,product=product,is_favorite=1).exists(), 
                'free_shipping': product.is_free_shipping
            } for product in Product.objects.all()[:20]]
        except ProductImage.DoesNotExist:
            return JsonResponse({'message':'thumbnailUrl NOT EXIST'}, status=404)
        except ProductImage.MultipleObjectsReturned:
            return JsonResponse({'message':'thumbnailUrl MULTIPLE RETURNED'}, status=404)
        return JsonResponse({'productList':product_list}, status=200)

class ProductDetailView(View):
    @status_decorator
    def get(self, request, product_id):
        try:
            product       = Product.objects.get(id=product_id)
            productDetail = {
                            'productId'    : product.id,
                            'imageUrls'    : [image.image_url for image in ProductImage.objects.filter(product=product)],
                            'type'         : "사이즈",
                            'options'      : {
                                                "sizeId": Size.objects.get(id=1).id,
                                                "name"  : Size.objects.get(id=1).name
                                            },
                            'name'         : product.name,
                            'price'        : {
                                            "normal" : int(product.price),
                                            "sale"   : int(product.discount_rate)
                                            },
                            'reviews'      : [{
                                                "user"      : review.user.name,
                                                "grade"     : review.rating,
                                                "date"      : datetime.strftime(review.create_at, "%Y-%m-%d %H:%M:%S"),
                                                "type"      : "사이즈",
                                                "option"    : {
                                                                "sizeId": Size.objects.get(id=1).id,
                                                                "name"  : Size.objects.get(id=1).name
                                                            },
                                                "comment"   : review.content,
                                                "image_url" : ReviewImage.objects.filter(review=review).first().image_url
                                            } for review in Review.objects.filter(product=product)],
                            'review'       : Review.objects.filter(product_id=product.id).aggregate(count=Count('id'))["count"] if Review.objects.filter(product_id=product.id) else 0,
                            'rating'       : Review.objects.filter(product_id=product.id).aggregate(rating=Avg('rating'))["rating"] if Review.objects.filter(product_id=product.id) else 0,
                            'follower'     : product.follower.all().count(),
                            'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                            'favorite'     : Favorite.objects.filter(user_id=1,product=product).exists(),
                            'free_shipping': product.is_free_shipping
                            }                
            return JsonResponse({'productDetail':productDetail}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'message':'PRODUCT NOT EXIST'}, status=404)
        except Product.MultipleObjectsReturned:
            return JsonResponse({'message':'PRODUCT MULTIPLE RETURNED'}, status=404)

class ProductListView(View):
    @status_decorator
    def get(self, request):        
        try:
            menu     = request.GET.get('menu')
            category = request.GET.get('category', None)
            user_id  = request.user_id

            products     = Product.objects.filter(Q(category__menu_id=menu) | Q(category_id=category))
            count        = products.count()
            product_list = [{
                            'productId'    : product.id,
                            'thumbnailUrl' : ProductImage.objects.filter(Q(product=product)&Q(is_thumbnail='1')).first().image_url if ProductImage.objects.filter(Q(product=product)&Q(is_thumbnail='1')) else "",
                            'type'         : product.type.name,
                            'productName'  : product.name,
                            'price'        : {
                                            "normal" : int(product.price),
                                            "sale"   : int(product.discount_rate)
                                            },
                            'review'       : Review.objects.filter(product_id=product.id).aggregate(count=Count('id'))["count"] if Review.objects.filter(product_id=product.id) else 0,
                            'rating'       : Review.objects.filter(product_id=product.id).aggregate(rating=Avg('rating'))["rating"] if Review.objects.filter(product_id=product.id) else 0,
                            'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                            'favorite'     : Favorite.objects.filter(user_id=user_id,product=product).exists(),
                            'free_shipping': product.is_free_shipping
            } for product in products]            
            return JsonResponse({'productList':product_list, 'count':count}, status=200)        
        except ProductImage.DoesNotExist:
            return JsonResponse({'message':'thumbnailUrl NOT EXIST'}, status=404)
        except ProductImage.MultipleObjectsReturned:
            return JsonResponse({'message':'thumbnailUrl MULTIPLE RETURNED'}, status=404)
        except Type.DoesNotExist:
            return JsonResponse({'message':'thumbnailUrl NOT EXIST'}, status=404)
        except Type.MultipleObjectsReturned:
            return JsonResponse({'message':'thumbnailUrl MULTIPLE RETURNED'}, status=404)

class ProductReviewView(View):
    @status_decorator
    def get(self, request, product_id):
        try:
            page    = int(request.GET.get('page', 0))
            limit   = int(request.GET.get('limit', 20))
            filter  = request.GET.get('filter', 'RECENT')
            
            if filter == 'RECENT':
                reviews = Review.objects.filter(product_id=product_id).order_by('create_at')
            elif filter == 'LATE':
                reviews = Review.objects.filter(product_id=product_id).order_by('-create_at')
            elif filter == 'HIGH':
                reviews = Review.objects.filter(product_id=product_id).order_by('-rating')
            elif filter == 'LOW':
                reviews = Review.objects.filter(product_id=product_id).order_by('rating')
            
            user_id = request.user_id
            review_info = {
                            'avg_rating'  : round(reviews.aggregate(rating=Avg('rating'))["rating"],1) if reviews.aggregate(rating=Avg('rating'))["rating"] else 0,
                            'total_review': reviews.aggregate(count=Count('id'))["count"]
            }
            review_list = [{
                            'review_id'    : review.id,
                            'content'      : review.content,
                            'rating'       : review.rating,
                            'create_at'    : datetime.strftime(review.create_at, "%Y-%m-%d %H:%M:%S"),
                            'user_id'      : review.user.id,
                            'login_id'     : review.user.login_id,
                            'size_name'    : Size.objects.get(id=1).name,
                            'review_image' : ReviewImage.objects.filter(review_id=review.id).first().image_url,
                            'review_images': [images.image_url for images in ReviewImage.objects.filter(review_id=review.id)],
                            'recommand'    : ReviewRecommand.objects.filter(review_id=review.id).count(),
                            'my_recommand' : Review.objects.get(id=review.id).recommander.filter(id=user_id).exists()
            } for review in reviews[page:limit]]
            return JsonResponse({'review_info':review_info, 'review_list':review_list}, status=200)        
        except Size.DoesNotExist:
            return JsonResponse({'message':'Size NOT EXIST'}, status=404)
        except Size.MultipleObjectsReturned:
            return JsonResponse({'message':'Size MULTIPLE RETURNED'}, status=404)
        except Review.DoesNotExist:
            return JsonResponse({'message':'Review NOT EXIST'}, status=404)
        except Review.MultipleObjectsReturned:
            return JsonResponse({'message':'Review MULTIPLE RETURNED'}, status=404)

class ProductQnaView(View):
    @status_decorator
    def get(self, request, product_id):    
        page      = int(request.GET.get('page', 0))
        limit     = int(request.GET.get('limit', 20))
        questions = Question.objects.filter(product_id=product_id)
        qna_list  = [{
                        'q_id'        : question.id,
                        'q_content'   : question.content,
                        'q_create_at' : datetime.strftime(question.create_at, "%Y-%m-%d %H:%M:%S"),
                        'q_update_at' : datetime.strftime(question.update_at, "%Y-%m-%d %H:%M:%S"),
                        'q_user_id'   : question.user.id,
                        'q_login_id'  : question.user.login_id,
                        'a_id'        : question.answer_set.first().id if question.answer_set.first() else '',
                        'a_content'   : question.answer_set.first().content if question.answer_set.first() else '',
                        'a_create_at' : datetime.strftime(question.answer_set.filter(question_id=question.id).first().create_at, "%Y-%m-%d %H:%M:%S") if question.answer_set.first() else '',
                        'a_update_at' : datetime.strftime(question.answer_set.filter(question_id=question.id).first().update_at, "%Y-%m-%d %H:%M:%S") if question.answer_set.first() else '',
                        'a_seller'    : "판매자" if question.answer_set.first() else '',
                        'status'      : question.answer_set.exists()
        } for question in questions[page:limit]]
        return JsonResponse({'qna_list':qna_list}, status=200)

    @token_decorator
    def post(self, request, product_id):
        try:            
            user_id = request.user_id
            data    = json.loads(request.body)
            content = data['content']

            Question.objects.create(
                content    = content,
                product_id = product_id,
                user_id    = user_id
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)

class MyProductQnaView(View):
    @token_decorator
    def get(self, request, product_id):    
        page      = int(request.GET.get('page', 0))
        limit     = int(request.GET.get('limit', 20))
        user_id   = request.user_id
        questions = Question.objects.filter(Q(product_id=product_id)&Q(user_id=user_id))
        qna_list  = [{
                        'q_id'        : question.id,
                        'q_content'   : question.content,
                        'q_create_at' : datetime.strftime(question.create_at, "%Y-%m-%d %H:%M:%S"),
                        'q_update_at' : datetime.strftime(question.update_at, "%Y-%m-%d %H:%M:%S"),
                        'q_user_id'   : question.user.id,
                        'q_login_id'  : question.user.login_id,
                        'a_id'        : question.answer_set.first().id if question.answer_set.first() else '',
                        'a_content'   : question.answer_set.first().content if question.answer_set.first() else '',
                        'a_create_at' : datetime.strftime(question.answer_set.filter(question_id=question.id).first().create_at, "%Y-%m-%d %H:%M:%S") if question.answer_set.first() else '',
                        'a_update_at' : datetime.strftime(question.answer_set.filter(question_id=question.id).first().update_at, "%Y-%m-%d %H:%M:%S") if question.answer_set.first() else '',
                        'a_seller'    : "판매자" if question.answer_set.first() else '',
                        'status'      : question.answer_set.exists()
        } for question in questions[page:limit]]
        return JsonResponse({'qna_list':qna_list}, status=200)

class QnaDetailView(View):    
    @token_decorator
    def patch(self, request, product_id, question_id):
        try:
            data             = json.loads(request.body)
            content          = data['content']
            question         =  Question.objects.get(id=question_id)
            question.content = content
            question.save()
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
        except Question.DoesNotExist:
            return JsonResponse({'message':'NOT EXIST ERROR'}, status=400)
        except Question.MultipleObjectsReturned:
            return JsonResponse({'message':'MULTIPLE OBJECTS ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)

    @token_decorator
    def delete(self, request, product_id, question_id):
        try:
            question =  Question.objects.get(id=question_id)
            question.delete()
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except Question.DoesNotExist:
            return JsonResponse({'message':'NOT EXIST ERROR'}, status=400)
        except Question.MultipleObjectsReturned:
            return JsonResponse({'message':'MULTIPLE OBJECTS ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)