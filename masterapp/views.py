from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from masterapp.models import Users,Category,Sub_category
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.




class User_Signup(APIView):


    def post(self,request):

        try:
            name=request.data.get('name')
            email=request.data.get('email')
            password=request.data.get('password')
            address=request.data.get('address')

            

            if not email or not name or not address or not password:
                return Response({
                        'status':status.HTTP_400_BAD_REQUEST,
                        'message':'Please enter all the Required filed'
                    },
                    status=400
                )

            if Users.objects.filter(email=email).exists():
                return Response({
                        'status':status.HTTP_400_BAD_REQUEST,
                        'message':'User with this email already exists'
                    },
                    status=400
                )
            
            user=Users.objects.create(
                name=name,
                password=make_password(password),
                email=email,
                address=address
            )

            token, created = Token.objects.get_or_create(user=user)


            return Response(
                {
                    'status':status.HTTP_201_CREATED,
                    'message':'User created',
                    'data':{
                        'name':user.name,
                        'email':user.email,
                        'password':user.password,
                        'address':user.address,
                        'token':token.key,
                    }
                },
                status=400,
            )
        
        except Exception as e:
            print("-----Exp-----",e)
            return Response(
                {"status": 500, "message": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class User_login(APIView):

    def post(self,request):

        try:

            email=request.data.get('email')
            password=request.data.get('password')

            if not email or not password:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Email and password are required'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user=authenticate(email=email,password=password)

            if user is None:
                return Response(
                    {
                        'status': status.HTTP_401_UNAUTHORIZED,
                        'message': 'Invalid email or password'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            token, created = Token.objects.get_or_create(user=user)


            return Response(
                {
                    'status':status.HTTP_200_OK,
                    'message':'Login Succesfully',
                    'data':{
                        'email':user.email,
                        'password':user.password,
                        'token':token.key,

                    }
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("Exception:", e)
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Internal Server Error'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class User_udate_detail(APIView):
 
 authentication_classes = [TokenAuthentication]
 permission_classes = [IsAuthenticated]

 def get(self,request):
    
    
    try:

            id=request.query_params.get('id')

            if not id :
                    return Response(
                        {
                            'status': status.HTTP_404_NOT_FOUND,
                            'message': 'Provide User id to found record',
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
            try:
                    data = Users.objects.get(id=id)
                    return Response(
                        {
                            'status':status.HTTP_200_OK,
                            'message':'User data found',
                            'data':{
                                'name':data.name,
                                'email':data.email,
                                'address':data.address,

                            }
                        },
                        status=status.HTTP_200_OK
                    )
            except Users.DoesNotExist:
                    return Response(
                        {
                            'status': status.HTTP_404_NOT_FOUND,
                            'message': 'User not found',
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
    except Exception as e:
            print("-------Exp-------",e)
            return Response({
                            'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                            'message':'Something went wrong'
                        },
                        status=400
                    )
            


 def post(self,request):
        
        try:
            id=request.query_params.get('id')

            if not id :
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        'message': 'Provide User id to found record',
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            try:
                data = Users.objects.get(id=id)
            except Users.DoesNotExist:

                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        'message': 'User not found',
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # if data.id != request.user.id:
            #     return Response(
            #         {
            #             'status': status.HTTP_403_FORBIDDEN,
            #             'message': 'You are not authorized to update this user',
            #         },
            #         status=status.HTTP_403_FORBIDDEN
            #     )
        
            name=request.data.get('name',data.name)
            email=request.data.get('email',data.email)
            address=request.data.get('address',data.address)

            if not name or not email or not address:
                 return Response({
                            'status':status.HTTP_400_BAD_REQUEST,
                            'message':'Please enter all required filed'
                        },
                        status=400
                    )

            
            if Users.objects.filter(email=data.email).exclude(id=id).exists():
                    return Response({
                            'status':status.HTTP_400_BAD_REQUEST,
                            'message':'User with this email already exists'
                        },
                        status=400
                    )


            data.name = name
            data.email = email
            data.address = address
            data.save()


            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'User data updated successfully',
                    'data': {
                        'name': data.name,
                        'email': data.email,
                        'address': data.address,
                    },
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print("-------Exp-------",e)
            return Response({
                            'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                            'message':'Something went wrong'
                        },
                        status=500
                    )
        




class add_category(APIView):
     
    def post(self,request):
        try:
          
            name=request.data.get('name')
            description=request.data.get('description')
            price=request.data.get('price')


            if not name or not description or not price:
                return Response(
                        {
                            'status':status.HTTP_400_BAD_REQUEST,
                            'message':'Please enter name or description or price'
                        }
                )

            data=Category.objects.create(
                 name=name,
                 description=description,
                 price=price,
                 is_active=True
                )

            data.save()

            return Response(
                {
                    'status':201,
                    'message':'Category added successfuly',
                    'data':{
                        'name':data.name,
                        'description':data.description,
                        'price':data.price,
                    }
                }
            )
        except Exception as e:
            print("---------Exp---------------",e)
            return Response(
                        {
                            'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                            'message':'Something went wrong'
                        }
                )



class add_sub_category(APIView):
 
    def post(self,request):
        try:    

            category_id=request.query_params.get('id')

            if not category_id:
                return Response(
                        {
                            'status':status.HTTP_400_BAD_REQUEST,
                            'message':'Please provide category id'
                        }
                )
            
            try:
                category=Category.objects.get(id=category_id)
                print(f"Category found:-- {category}")
            except Category.DoesNotExist:
                    return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Category not found with this id',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
              
            name=request.data.get('name')
            description=request.data.get('description')
            price=request.data.get('price')
            image = request.FILES.get('image') 

            required_fields = {
                'name': name,
                'description': description,
                'price': price
              
            }

            for i, value in required_fields.items():
                if not value:
                    return Response(
                        {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': f"Please enter {i}",
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            if image:
                if not image.name.endswith(('.jpg', '.png', '.jpeg')):
                    return Response(
                        {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'Invalid image file format. Only jpg, jpeg, and png are allowed.',
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                image = None  # If no image is provided, set it to None
            
            data=Sub_category.objects.create(
                name=name,
                description=description,
                price=price,
                image=image,
                is_active=True,
                category=category

            )
            data.save()
            
            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    'message': 'Subcategory created successfully',
                    'data': {
                        'id': data.id,
                        'name': data.name,
                        'category': data.category.id,
                        'description': data.description,
                        'price': data.price,
                        'image': data.image.url if data.image else None,
                        'is_active': data.is_active,
                        'created_at': data.created_at,
                    },
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print("Exception:------------------:---------", e)
            return Response(
                    {
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'message': 'Internal Server Error',
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
         

            

              

     