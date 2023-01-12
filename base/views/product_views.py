from importlib.resources import contents
'''from math import prod'''
from django.shortcuts import render

from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage

from base.models import Product , Review
from base.serializer import ProductSerializer 

from rest_framework import status


@api_view(["GET"])
def getProducts(request):
    query = request.query_params.get('keyword')
    if query == 'null' :
        query=''

    products = Product.objects.filter(name__icontains=query)

    page = request.query_params.get('page')
    paginator = Paginator(products , 6)
    try :
        products = paginator.page(page)
    except PageNotAnInteger :
        products = paginator.page(1)
    except EmptyPage :
        products = paginator.page(paginator.num_pages)

    if page ==None :
        page = 1

    page = int(page)
    


    serializ=ProductSerializer(products , many=True)    
    return Response({'products' :serializ.data , 'page' : page , 'pages' : paginator.num_pages })



@api_view(["GET"])
def getProduct(request , pk):
    
    # product = Product.objects.filter(_id=pk).select_related('user__review')

    product=Product.objects.get(_id=pk)
    product.user
    serializ=ProductSerializer(product , many=False)
    # print(product)
    return Response(serializ.data)

@api_view(["PUT"])
@permission_classes([IsAdminUser])
def updateProduct (request , pk ):
    data = request.data
    product=Product.objects.get(_id=pk)

    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']

    product.save()

    serializ=ProductSerializer(product , many=False)
    return Response(serializ.data)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def createProduct (request ):
    user = request.user
    product = Product.objects.create(
        user = user ,
        name='simple name' ,
        price = 0 ,
        brand ='simple brand' ,
        countInStock = 0 ,
        category = 'simple category',
        description = ''
     )

    serializer = ProductSerializer(product , many = False)
    return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def deleteProduct (request , pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('product was deleted')

@api_view(["POST"])
def uploadImage (request) :
    data = request.data
    product_id = data['product_id']
    product = Product.objects.get(_id = product_id)
    product.image = request.FILES.get('image')
    product.save()

    return Response('image uploaded')

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createProductReview (request , pk):
    user = request.user
    data = request.data
    product = Product.objects.get(_id=pk)

    alreadyExist = product.review_set.filter(user=user).exists()
    if alreadyExist :
        content = {'detail' : 'product already reviewed' }
        return Response(content , status=status.HTTP_400_BAD_REQUEST )

    elif data['rating'] == 0 :
        content = {'detail' : 'please select rating' }
        return Response(content , status=status.HTTP_400_BAD_REQUEST )

    else :
        review = Review.objects.create(
            user = user ,
            product = product ,
            name = user.first_name ,
            rating = data['rating'] ,
            comment = data['comment'] ,
        )
        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0

        for i in reviews :
            total += i.rating

        product.rating = total/len(reviews)   

        product.save()
        return Response('Review Added')

