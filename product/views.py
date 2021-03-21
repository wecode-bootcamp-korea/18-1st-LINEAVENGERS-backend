from datetime      import datetime
from mypage.models import Review

from django.http                  import JsonResponse, request
from django.views                 import View
from django.db.models.query_utils import Q
from django.db.models             import Count, Avg

from product.models import (
    Category, Menu, Product, 
    ProductImage, ProductSize)

class CategoryListView(View):
    def get(self, request):
    
        getted_menu     = request.GET.get('menu')
        getted_category = request.GET.get('category', None)
        
        menus    = Menu.objects.all()
        menuList = []
        for menu in menus:
            menuList.append(
                {
                    "menuId"  : menu.id,
                    "menuName": menu.name 
                }
            )

        categories   = Category.objects.filter(menu=getted_menu)
        categoryList = []
        for category in categories:
            categoryList.append(
                {
                    "categoryId"  : category.id,
                    "categoryName": category.name,
                }
            )
        
        type  = ""
        title = ""
        count = 0

        if getted_category:
            type     = "category"
            category = Category.objects.get(id=getted_category) 
            title    = category.name
            count    = Product.objects.filter(category=category).count()
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

        return JsonResponse({'menuList':menuList, 'categoryList':categoryList, 'current':current}, status=200)

class ProductListView(View):
    def get(self, request):

        products = Product.objects.all()[:20]
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
                                    "normal" : format(int(product.price)),
                                    "sale" : int(product.discount_rate)
                                    },
                    'review'       : Review.objects.aggregate(count=Count('id'))["count"],
                    'rating'       : round(Review.objects.aggregate(rating=Avg('rating'))["rating"],1),
                    'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                    'favorite'     : False,
                    'free_shipping': product.is_free_shipping
                }
            )

        return JsonResponse({'productList':productList}, status=200)

class ProductDetailView(View):
    #@decorator
    def get(self, request, product_id):

        product = Product.objects.get(id=product_id)

        imageList = []
        images = ProductImage.objects.filter(product=product)
        for image in images:
            imageList.append(image.image_url)
        
        sizeList = []
        sizes = Product.objects.get(id=product.id).sizes.all()
        for size in sizes:
            sizeList.append(size.name)
        
        reviewList = []
        reviews = Review.objects.filter(product=product)
        for review in reviews:
            reviewList.append(
                {
                    "user"      : review.user.name,
                    "grade"     : review.rating,
                    "date"      : datetime.strftime(review.create_at, "%Y-%m-%d %H:%M:%S"),
                    "type"      : "사이즈",
                    "option"    : "단품",
                    "comment"   : review.content,
                    "image_url" : ""
                }
            )
        
        productDetail = {
                        'productId'    : product.id,
                        'imageUrls'    : imageList,
                        'type'         : "사이즈",
                        'options'      : sizeList,
                        'name'         : product.name,
                        'price'        : {
                                        "normal" : int(product.price),
                                        "sale" : int(product.discount_rate)
                                        },
                        'reviews'       : reviewList,
                        'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                        'favorite'     : False,
                        'free_shipping': product.is_free_shipping
                        }
        

        return JsonResponse({'productDetail':productDetail}, status=200)
    
class MainCategoryView(View):
    def get(self, request):
        
        menus    = Menu.objects.all()
        menuList = []

        for menu in menus:

            categories   = Category.objects.filter(menu=menu)
            categoryList = []
            for category in categories:
                categoryList.append(
                    {
                        "categoryId"  :category.id,
                        "categoryName":category.name
                    }
                )

            menuList.append(
                {
                    "menuId"      : menu.id,
                    "menuName"    : menu.name,
                    "categoryList": categoryList
                }
            ) 
            
        return JsonResponse({'menuList':menuList}, status=200)


class MainProductView(View):
    def get(self, request):

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
                    'thumbnailUrl' : ProductImage.objects.filter(Q(product=product)&Q(is_thumbnail='1')).image_url,
                    'type'         : type,
                    'productName'  : product.name,
                    'price'        : {
                                    "normal" : int(product.price),
                                    "sale" : int(product.discount_rate)
                                    },
                    'review'       : Review.objects.aggregate(count=Count('id'))["count"],
                    'rating'       : round(Review.objects.aggregate(rating=Avg('rating'))["rating"],1),
                    'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                    'favorite'     : False,
                    'free_shipping': product.is_free_shipping
                }
            )
            if product.id == 20:
                break;

        return JsonResponse({'productList':productList}, status=200)

class CategoryView(View):
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

        categories   = Category.objects.filter(menu=getted_menu)
        categoryList = []
        for category in categories:
            categoryList.append(
                {
                    "categoryId"  : category.id,
                    "categoryName": category.name,
                }
            )
        
        type  = ""
        title = ""
        count = 0

        if getted_category:
            type     = "category"
            category = Category.objects.get(id=getted_category) 
            title    = category.name
            count    = Product.objects.filter(category=category).count()
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

        return JsonResponse({'menuList':menuList, 'categoryList':categoryList, 'current':current}, status=200)

## 상품리스트_2021.03.21
class ProductView(View):
    def get(self, request):

        getted_menu     = request.GET.get('menu')
        getted_category = request.GET.get('category', None)

        #전체메뉴
        menus = Menu.objects.all()
        menuList = []
        for menu in menus:
            menuList.append(
                {
                    "menuId"  : menu.id,
                    "menuName": menu.name 
                }
            )
        
        #카테고리 메뉴
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
                        'favorite'     : False,
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
                
        #현재정보
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
                    'favorite'     : False,
                    'free_shipping': product.is_free_shipping
                }
            )

        return JsonResponse({'menuList':menuList, 'categoryList':categoryList, 'current':current, 'productList':productList}, status=200)


class MainCategoryView(View):
    def get(self, request):
        
        menus    = Menu.objects.all()
        menuList = []

        for menu in menus:
            categories   = Category.objects.filter(menu=menu)
            categoryList = [{
                "categoryId"  :category.id,
                "categoryName":category.name
            } for category in categories]

            menuList.append(
                {
                    "menuId"  : menu.id,
                    "menuName": menu.name,
                    "categoryList": categoryList
                }
            ) 
            
        return JsonResponse({'menuList':menuList}, status=200)

class MainView(View):
    def get(self, request):
        
        menus    = Menu.objects.all()
        menuList = []
        for menu in menus:
            categories   = Category.objects.filter(menu=menu)
            categoryList = [{
                "categoryId"  :category.id,
                "categoryName":category.name
            } for category in categories]
        
            menuList.append(
                {
                    "menuId"  : menu.id,
                    "menuName": menu.name,
                    "categoryList": categoryList
                }
            )

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
                    'thumbnailUrl' : ProductImage.objects.get(Q(product=product)&Q(is_thumbnail='1')).image_url,
                    'type'         : type,
                    'productName'  : product.name,
                    'price'        : {
                                    "normal" : format(int(product.price),','),
                                    "sale" : int(product.discount_rate)
                                    },
                    'review'       : Review.objects.aggregate(count=Count('id'))["count"],
                    'rating'       : round(Review.objects.aggregate(rating=Avg('rating'))["rating"],1),
                    'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                    'favorite'     : False,
                    'free_shipping': product.is_free_shipping
                }
            )
            
        return JsonResponse({'menuList':menuList, 'productList':productList}, status=200)