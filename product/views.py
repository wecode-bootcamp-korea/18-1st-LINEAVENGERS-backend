from datetime import datetime

from django.http                  import JsonResponse, request
from django.views                 import View
from django.db.models.query_utils import Q

from product.models import Category, Menu, Product, ProductImage

class CategoryListView(View):
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
        
        type  = ""
        title = ""
        count = 0

        if getted_category:
            type = "category"
            category = Category.objects.get(id=getted_category) 
            title = category.name
            count = Product.objects.filter(category=category).count()
        else:
            type = "menu"
            menu = Menu.objects.get(id=getted_menu)
            title = menu.name
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
                                    "normal" : int(product.price),
                                    "sale" : int(product.discount_rate)
                                    },
                    'review'       : 10,
                    'rating'       : 5,
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

        if product.is_best and product.is_new:
            type = "TOP"
        elif product.is_best and not product.is_new:
            type = "BEST"
        elif not product.is_best and product.is_new:
            type = "NEW"
        else:
            type = "NORMAL"

        imageList = []
        images = ProductImage.objects.filter(product=product)
        for image in images:
            imageList.append(image.image_url)

        productDetail = {
                        'productId'    : product.id,
                        'imageUrl'     : imageList,
                        'type'         : type,
                        'productName'  : product.name,
                        'price'        : {
                                        "normal" : int(product.price),
                                        "sale" : int(product.discount_rate)
                                        },
                        'review'       : 10,
                        'rating'       : 5,
                        'createDate'   : datetime.strftime(product.create_at, "%Y-%m-%d %H:%M:%S"),
                        'favorite'     : False,
                        'free_shipping': product.is_free_shipping
                        }
        

        return JsonResponse({'productDetail':productDetail}, status=200)
    
class MainCategoryView(View):
    def get(self, request):
        
        menus = Menu.objects.all()
        menuList = []

        for menu in menus:

            categories = Category.objects.filter(menu=menu)
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
                    "menuId"  : menu.id,
                    "menuName": menu.name,
                    "categoryList": categoryList
                }
            ) 
            
        return JsonResponse({'menuList':menuList}, status=200)


class MainProductView(View):
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
                                    "normal" : int(product.price),
                                    "sale" : int(product.discount_rate)
                                    },
                    'review'       : 10,
                    'rating'       : 5,
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

        categories = Category.objects.filter(menu=getted_menu)
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
            type = "category"
            category = Category.objects.get(id=getted_category) 
            title = category.name
            count = Product.objects.filter(category=category).count()
        else:
            type = "menu"
            menu = Menu.objects.get(id=getted_menu)
            title = menu.name
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
