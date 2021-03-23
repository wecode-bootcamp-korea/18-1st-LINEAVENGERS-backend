from datetime      import datetime
from mypage.models import Review, ReviewImage

from django.http                  import JsonResponse, request
from django.views                 import View
from django.db.models.query_utils import Q
from django.db.models             import Count, Avg

from product.models import (
    Category, 
    Menu, 
    Product, 
    ProductImage)
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
                'rating'       : round(Review.objects.aggregate(rating=Avg('rating'))["rating"],1),
                'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                'favorite'     : Favorite.objects.filter(user_id=1,product=product,is_favorite=1).exists(),   #데코레이터가 반영되면 user_id값 변경 .
                'free_shipping': product.is_free_shipping
            } for product in Product.objects.all()[:20]]

        return JsonResponse({'productList':product_list}, status=200)

class ProductView(View):
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

class ListView(View):
    #@decorator
    def get(self, request):

        menu     = request.GET.get('menu')
        category = request.GET.get('category', None)

        product_list = []
        products = []

        if category:
            products.append(Product.objects.filter(category=category))
        else:
            categories = Category.objects.filter(menu=menu)
            for category in categories:
                products.append(category)

        product_list = [{
            'productId'    : product.id,
            'thumbnailUrl' : ProductImage.objects.get(Q(product=product.id)&Q(is_thumbnail='1')).image_url,
            'type'         : type,
            'productName'  : product.name,
            'price'        : {
#                            "normal" : int(product.price),
 #                           "sale" : int(product.discount_rate)
                            },
            'review'       : Review.objects.aggregate(count=Count('id'))["count"],
            'rating'       : round(Review.objects.aggregate(rating=Avg('rating'))["rating"],1),
#            'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
            'favorite'     : Favorite.objects.filter(user_id=1,product=product).exists(),   #데코레이터가 반영되면 user_id값 변경 .,
            'free_shipping': product.is_free_shipping
        } for product in products]

        '''
        type       = "menu"
        menu       = Menu.objects.get(id=getted_menu)
        title      = menu.name
        categories = Category.objects.filter(menu=menu)
        for category in categories:
            count += Product.objects.filter(category=category).count()

        if getted_category:
            type     = "category"
            category = Category.objects.get(id=getted_category) 
            title    = category.name
            count    = Product.objects.filter(category=category).count()
            
            products = Product.objects.filter(category=category)
            for product in products:
                if product.is_best and product.is_new:
                    type = "TOP"
                elif product.is_best and not product.is_new:
                    type = "BEST"
                elif not product.is_best and product.is_new:
                    type = "NEW"
                else:
                    type = "NORMAL"    

                product_list.append(
                    {
                        'productId'    : product.id,
                        'thumbnailUrl' : ProductImage.objects.get(Q(product=product.id)&Q(is_thumbnail='1')).image_url,
                        'type'         : type,
                        'productName'  : product.name,
                        'price'        : {
                                        "normal" : int(product.price),
                                        "sale" : int(product.discount_rate)
                                        },
                        'review'       : Review.objects.aggregate(count=Count('id'))["count"],
                        'rating'       : round(Review.objects.aggregate(rating=Avg('rating'))["rating"],1),
                        'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                        'favorite'     : Favorite.objects.filter(user_id=1,product=product).exists(),   #데코레이터가 반영되면 user_id값 변경 .,
                        'free_shipping': product.is_free_shipping
                    }
                )    
        else:
            type       = "menu"
            menu       = Menu.objects.get(id=getted_menu)
            title      = menu.name
            categories = Category.objects.filter(menu=menu)
            for category in categories:
                count += Product.objects.filter(category=category).count()
                
        current = [
            {
                "type" : type,
                "title": title,
                "count": count
            }
        ]

        products    = Product.objects.all()[:20]
        product_list = []
        for product in products:     

            if product.is_best and product.is_new:
                type = "TOP"
            elif product.is_best and not product.is_new:
                type = "BEST"
            elif not product.is_best and product.is_new:
                type = "NEW"
            else:
                type = "NORMAL"    

            product_list.append(
                {
                    'productId'    : product.id,
                    'thumbnailUrl' : ProductImage.objects.get(Q(product=product.id)&Q(is_thumbnail='1')).image_url,
                    'type'         : type,
                    'productName'  : product.name,
                    'price'        : {
                                    "normal" : int(product.price),
                                    "sale" : int(product.discount_rate)
                                    },
                    'review'       : Review.objects.aggregate(count=Count('id'))["count"],
                    'rating'       : round(Review.objects.aggregate(rating=Avg('rating'))["rating"],1),
                    'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                    'favorite'     : Favorite.objects.filter(user_id=1,product=product).exists(),   #데코레이터가 반영되면 user_id값 변경 .,
                    'free_shipping': product.is_free_shipping
                }
            )
        '''

        return JsonResponse({'categoryData':{'menuList':menuList, 'categoryList':categoryList, 'current':current}, 'productList':product_list}, status=200)
        

## 상품리스트_2021.03.21(수정해야함.)
class ProductListView(View):
    #@decorator
    def get(self, request):

        getted_menu     = request.GET.get('menu')
        getted_category = request.GET.get('category', None)

        menus = Menu.objects.all()
        menuList = []
        for menu in menus:
            menuList.append(
                {
                    "menuId"  : menu.id,
                    "menuName": menu.name 
                }
            )
        
        categories = Category.objects.filter(menu=getted_menu)
        categoryList = []
        for category in categories:
            categoryList.append(
                {
                    "categoryId"  : category.id,
                    "categoryName": category.name,
                }
            )
        
        type        = ""
        title       = ""
        count       = 0
        productList = []

        if getted_category:
            type     = "category"
            category = Category.objects.get(id=getted_category) 
            title    = category.name
            count    = Product.objects.filter(category=category).count()
            
            products = Product.objects.filter(category=category)
            for product in products:
                if product.is_best and product.is_new:
                    type = "TOP"
                elif product.is_best and not product.is_new:
                    type = "BEST"
                elif not product.is_best and product.is_new:
                    type = "NEW"
                else:
                    type = "NORMAL"    

                productList.append(
                    {
                        'productId'    : product.id,
                        'thumbnailUrl' : ProductImage.objects.get(Q(product=product.id)&Q(is_thumbnail='1')).image_url,
                        'type'         : type,
                        'productName'  : product.name,
                        'price'        : {
                                        "normal" : int(product.price),
                                        "sale" : int(product.discount_rate)
                                        },
                        'review'       : Review.objects.aggregate(count=Count('id'))["count"],
                        'rating'       : round(Review.objects.aggregate(rating=Avg('rating'))["rating"],1),
                        'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                        'favorite'     : Favorite.objects.filter(user_id=1,product=product).exists(),   #데코레이터가 반영되면 user_id값 변경 .,
                        'free_shipping': product.is_free_shipping
                    }
                )    
        else:
            type       = "menu"
            menu       = Menu.objects.get(id=getted_menu)
            title      = menu.name
            categories = Category.objects.filter(menu=menu)
            for category in categories:
                count += Product.objects.filter(category=category).count()
                
        current = [
            {
                "type" : type,
                "title": title,
                "count": count
            }
        ]

        products    = Product.objects.all()[:20]
        productList = []
        for product in products:     

            if product.is_best and product.is_new:
                type = "TOP"
            elif product.is_best and not product.is_new:
                type = "BEST"
            elif not product.is_best and product.is_new:
                type = "NEW"
            else:
                type = "NORMAL"    

            productList.append(
                {
                    'productId'    : product.id,
                    'thumbnailUrl' : ProductImage.objects.get(Q(product=product.id)&Q(is_thumbnail='1')).image_url,
                    'type'         : type,
                    'productName'  : product.name,
                    'price'        : {
                                    "normal" : int(product.price),
                                    "sale" : int(product.discount_rate)
                                    },
                    'review'       : Review.objects.aggregate(count=Count('id'))["count"],
                    'rating'       : round(Review.objects.aggregate(rating=Avg('rating'))["rating"],1),
                    'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                    'favorite'     : Favorite.objects.filter(user_id=1,product=product).exists(),   #데코레이터가 반영되면 user_id값 변경 .,
                    'free_shipping': product.is_free_shipping
                }
            )

        return JsonResponse({'categoryData':{'menuList':menuList, 'categoryList':categoryList, 'current':current}, 'productList':productList}, status=200)