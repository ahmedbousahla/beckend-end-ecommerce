from django.shortcuts import render


from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response


from base.models import Product , OrderItem , Order , ShippingAddress 
from base.serializer import ProductSerializer , OrderSerializer

from rest_framework import status
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    orderItems = data['orderItems']
    if orderItems and len (orderItems) == 0:
        return Response ({'detail' : 'no order item'} , status =status.HTTP_400_BAD_REQUEST )

    else :
        # create order
        order = Order.objects.create(
            user = user ,
            paymentMethod = data['paymentMethode'] ,
            taxPrice = data['taxPrice'] ,
            shippingPrice = data ['shippingPrice'] ,
            totalPrice = data ['totalPrice'] ,

        )

        # shipping address
        shipping = ShippingAddress.objects.create(
            order = order , 
            address = data ['shippingAddress']['address'] , 
            city = data ['shippingAddress']['city'] ,
            postalCode = data ['shippingAddress']['postalCode'] ,
            country = data ['shippingAddress']['country'] ,
        )

        # create order items and set order  to orderItem relationship 

        for i in orderItems :
            product = Product.objects.get(_id = i['product'])

            item = OrderItem.objects.create(
                product = product ,
                order = order ,
                name = product.name ,
                qty = i['qty'] ,
                price = i['price'] ,
                image = product.image.url ,
            )

             # update the stock 
            product.countInStock -= item.qty
            product.save()

        serialize = OrderSerializer(order , many = False)
        return Response(serialize.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrder (request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders , many = True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders (request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders , many = True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request ,  pk) :
    user =request.user
    try :
        order = Order.objects.get(_id=pk)

        if user.is_staff or order.user == user :
            serializer = OrderSerializer(order , many = False)
            return Response(serializer.data)
        else :
            Response({'details' : 'not authorized request to view'} , status=status.HTTP_400_BAD_REQUEST )
    except:
        return Response({'detail' : 'does not existe'} , status=status.HTTP_400_BAD_REQUEST  )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid (request , pk) :
    order = Order.objects.get(id = pk)

    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()
    return Response('order paid')