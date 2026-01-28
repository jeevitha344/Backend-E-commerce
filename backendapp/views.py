from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class product_handlerapi(APIView):
    def post(self, request):
        serializer = productserializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
    def get(self,request,productid=None):
        if productid:
            product=product_details.objects.get(id=productid)
            serializer=productserializer(product)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            product=product_details.objects.all()
            serializer=productserializer(product,many=True, context={'request': request})
            return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,productid=None):
        if productid:
            product=product_details.objects.get(id=productid)
            serializer=productserializer(product,data=request.data,partial=True )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
       
            return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,productid=None):
        if productid:
            product=product_details.objects.get(id=productid)
            product.delete()
            return Response({"message":"producted is deleted"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"id is must"},status=status.HTTP_400_BAD_REQUEST)
        


class ProductCategoryAPI(APIView):
    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        category = product_categorytb.objects.all()
        serializer = ProductCategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




# def singnuphandler(self,request):
#     first_name=request.POST.get('firstname')
#     last_name=request.POST.get('lastname')
#     email=request.POST.get('email')
#     username=request.POST.get('username')
#     password=request.POST.get('password')
#     confrimedpassword=request.POST.get('confrimedpassword')
#     if password!=confrimedpassword:
#         return Response

class signupapi(APIView):
    def post(self,request):
        serializer=signupserializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            refresh = RefreshToken.for_user(user)
            access=refresh.access_token
            return Response({
    "access": str(access),
    "refresh": str(refresh),
    "is_superuser": user.is_superuser,
    "is_staff": user.is_staff,
    "username": user.username
}, status=200)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
        

class loginapi(TokenObtainPairView):
    serializer_class = loginserializer # it automaticall return the response to frontend
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

class orderapi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    def post(self,request):
        serializer = Orderserializer(
            data=request.data,
              context={'request': request} 
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
   

    def get(self, request, pk=None):
        user = request.user
        if pk:
            try:
                order_obj = Order.objects.get(id=pk, user=request.user)
                serializer = Orderserializer(order_obj)
                return Response(serializer.data)
            except Order.DoesNotExist:
                return Response({"error": "Order not found"}, status=404)
        
        
        print("user",user)
        if user.is_staff or user.is_superuser:
            total_users = User.objects.count()
            orders = Order.objects.all()
            
            serializer = Orderserializer(orders, many=True)
            return Response({"data":serializer.data,"total_users":total_users})

# class orderproductapi(APIView):
#     def post(self,request):
#         serializer=orderproductserializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors)
        
#     def get(self,request):
        
#             product=orderItems.objects.all()
#             serializer=orderproductserializer(product,many=True, context={'request': request})
#             return Response(serializer.data,status=status.HTTP_200_OK)