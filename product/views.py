from datetime      import datetime

from django.conf.urls import url
from mypage.models import Question, Review, ReviewImage, ReviewRecommand

from django.http                  import JsonResponse, request
from django.views                 import View
from django.db.models.query_utils import Q
from django.db.models             import Count, Avg

from product.models import (
    Category, 
    Menu, 
    Product, 
    ProductImage, ProductSize, Size, Type)
from mypage.models  import Favorite 

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
    #@decorator
    def get(self, request):

        product_list = [
            {
                'productId'    : product.id,
                'thumbnailUrl' : ProductImage.objects.get(Q(product=product)&Q(is_thumbnail='1')).image_url,
                'type'         : product.type,
                'productName'  : product.name,
                'price'        : {
                                "normal" : int(product.price),
                                "sale"   : int(product.discount_rate)
                                },
                'review'       : Review.objects.aggregate(count=Count('id'))["count"],
                'rating'       : Review.objects.aggregate(rating=Avg('rating'))["rating"] if Review.objects.aggregate(rating=Avg('rating'))["rating"] else 0,
                'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                'favorite'     : Favorite.objects.filter(user_id=1,product=product,is_favorite=1).exists(),   #데코레이터가 반영되면 user_id값 변경 .
                'free_shipping': product.is_free_shipping
            } for product in Product.objects.all()[:20]]

        return JsonResponse({'productList':product_list}, status=200)

class ProductDetailView(View):
    #@decorator
    def get(self, request, product_id):

        product = Product.objects.get(id=product_id)

        productDetail = {
                        'productId'    : product.id,
                        'imageUrls'    : [image.image_url for image in ProductImage.objects.filter(product=product)],
                        'type'         : "사이즈",
                        'options'      : [{
                                            "sizeId":size.id,
                                            "name"  :size.name
                                        } for size in Product.objects.get(id=product.id).sizes.all()],
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
                                            "option"    : [{
                                                            "sizeId":size.id,
                                                            "name":size.name
                                                        } for size in Product.objects.get(id=product.id).sizes.all()],
                                            "comment"   : review.content,
                                            "image_url" : ReviewImage.objects.filter(review=review).first().image_url
                                        } for review in Review.objects.filter(product=product)],
                        'review'       : Review.objects.aggregate(count=Count('id'))["count"],
                        'rating'       : round(Review.objects.aggregate(rating=Avg('rating'))["rating"],1),
                        'follower'     : product.follower.all().count(),
                        'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                        'favorite'     : Favorite.objects.filter(user_id=1,product=product).exists(),   #데코레이터가 반영되면 user_id값 변경 .,
                        'free_shipping': product.is_free_shipping
                        }
        
        return JsonResponse({'productDetail':productDetail}, status=200)

class ProductListView(View):
    #@decorator
    def get(self, request):

        menu     = request.GET.get('menu')
        category = request.GET.get('category', None)

        products = Product.objects.filter(Q(category__menu_id=menu) | Q(category_id=category))

        product_list = [{
                        'productId'    : product.id,
                        'thumbnailUrl' : ProductImage.objects.get(Q(product=product.id)&Q(is_thumbnail='1')).image_url,
                        'type'         : Type.objects.get(id=product.type).name,
                        'productName'  : product.name,
                        'price'        : {
                                        "normal" : int(product.price),
                                        "sale"   : int(product.discount_rate)
                                        },
                        'review'       : Review.objects.aggregate(count=Count('id'))["count"],
                        'rating'       : Review.objects.aggregate(rating=Avg('rating'))["rating"] if Review.objects.aggregate(rating=Avg('rating'))["rating"] else 0,
                        'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                        'favorite'     : Favorite.objects.filter(user_id=1,product=product).exists(),   #데코레이터가 반영되면 user_id값 변경 .,
                        'free_shipping': product.is_free_shipping
        } for product in products]
        
        if category:
            current = [{'type' : 'category','title' : Category.objects.get(id=category).name,'count' : len(products)}]
        else:
            current = [{'type' : 'menu', 'title' : Menu.objects.get(id=menu).name, 'count': len(products)}]

        return JsonResponse({'productList':product_list, 'current':current}, status=200)


class ProductReviewView(View):
    #@decorator
    def get(self, request, product_id):

        offset  = int(request.GET.get('offset', 0))
        limit   = int(request.GET.get('limit', 20))
        filter  = request.GET.get('filter', 'RECENT')   #filter : RECENT, LATE, HIGH, LOW
        
        if filter == 'RECENT':
            reviews = Review.objects.filter(product_id=product_id).order_by('create_at')
        elif filter == 'LATE':
            reviews = Review.objects.filter(product_id=product_id).order_by('-create_at')
        elif filter == 'HIGH':
            reviews = Review.objects.filter(product_id=product_id).order_by('-rating')
        elif filter == 'LOW':
            reviews = Review.objects.filter(product_id=product_id).order_by('rating')
        
        #user_id = request.user_id
        user_id = 2 #테스트용.

        review_info = {
                        'avg_rating' : round(reviews.aggregate(rating=Avg('rating'))["rating"],1) if reviews.aggregate(rating=Avg('rating'))["rating"] else 0,
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
        } for review in reviews[offset:limit]]

        return JsonResponse({'review_info':review_info, 'review_list':review_list}, status=200)


class ProductQnaView(View):
    #@decorator
    def get(self, request, product_id):
    
        offset  = int(request.GET.get('offset', 0))
        limit   = int(request.GET.get('limit', 20))
        
        myqna   = request.GET.get('myqna','MYQNA')
        status  = request.GET.get('status','START')   #filter : START, END

        #user_id = request.user_id
        user_id = 2 #테스트용.
        questions = Question.objects.filter(product_id=product_id)

        qna_list = [{
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
                        'a_seller'    : question.answer_set.first().seller if question.answer_set.first() else '',
                        'status'      : question.answer_set.exists()
        } for question in questions[offset:limit]]

        return JsonResponse({'qna_list':qna_list}, status=200)

    #def post(self, request)
