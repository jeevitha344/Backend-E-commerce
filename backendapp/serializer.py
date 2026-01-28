from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class productserializer(serializers.ModelSerializer):
    product_category = serializers.PrimaryKeyRelatedField(
    queryset=product_categorytb.objects.all()
)
    
    class Meta:
        model = product_details
        fields = "__all__"


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = product_categorytb
        fields = "__all__"

class signupserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data): # valiated data -- is from user sent  data  from frontend that   get validate  and store here
        user = User.objects.create_user(
            username=validated_data['username'], # here ve access the validates data vaue using there key 
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class loginserializer(TokenObtainPairSerializer): # it automatically validate the user sent data
    @classmethod
    def get_token(cls,user):
        token=super().get_token(user)
         # Add custom claims
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user info to response
        data['is_superuser'] = self.user.is_superuser
        data['is_staff'] = self.user.is_staff
        
        return data
    
# get_token() → only creates the token (refresh) on backend

# validate() → wraps it together, adds extra info, and sends access + refresh + claims as response.data

# Frontend stores it → uses it in Authorization header for API calls

# Frontend uses access token for protected requests:
# axios.get('/api/orders/', {
#   headers: { Authorization: `Bearer ${localStorage.getItem("access")}` }
# });

# When access expires, frontend uses refresh token to get a new access:
# axios.post('/api/token/refresh/', { refresh: localStorage.getItem("refresh") });

class productserializer(serializers.ModelSerializer):
    class Meta:
        model=product_details
        fields=('id','product_name','product_price','product_image')

class orderproductserializer(serializers.ModelSerializer):
     product=productserializer(read_only=True) #Converts the saved product object into full product details

     product_id = serializers.PrimaryKeyRelatedField(
        queryset=product_details.objects.all(),
        source='product',
        write_only=True
     )
   
   
     class Meta:
        model = OrderItems
        fields = ('id','product','product_id', 'quantity')


class Orderserializer(serializers.ModelSerializer):
   
    items= orderproductserializer(many=True)

    class Meta:
        model = Order
        fields = ('id','name', 'email', 'phone', 'address', 'city', 'zipcode', 'total_price','items')
        # don't include user in fields, we'll set it automatically

    def create(self,validated_data):
        item_data=validated_data.pop('items')
        user=self.context['request'].user
        order_obj=Order.objects.create(user=user,**validated_data)
        for item in item_data:
            OrderItems.objects.create(order=order_obj,product=item['product'],
        quantity=item['quantity'])
        return order_obj
    



    