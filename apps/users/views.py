from datetime import datetime
from rest_framework.response import Response
from .serializers import UserSerializer, UserRegistroView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import LoginZerializer, LogoutSerializer




# Create your views here.
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        login_serializer = LoginZerializer(data=request.data)
        if login_serializer.is_valid():
            username = login_serializer.validated_data['username']
            
            usuario = User.objects.filter(username=username).first()
            if usuario.is_active:
                token, created = Token.objects.get_or_create(user=usuario)

                data = {
                    'username': usuario.username,
                    'gmail': usuario.gmail,
                    'nombre': usuario.nombre,
                    'token': token.key
                }
                if created:
                    return Response({'user': data}, status=status.HTTP_200_OK)
                else:
                    token_instans = Token.objects.get(key=token)
                    token_instans.delete()
                    token = Token.objects.create(user=usuario)
                    return Response({'messege':'usuario creado exitoso', 'user':data}, status=status.HTTP_200_OK)
            return Response({'error':'el usuario esta inactivo, intentelo en otro momento'}, status=status.HTTP_404_NOT_FOUND)
        else:    
            return Response({'usuario':'no encontrado , intente de nuevo'}, status=status.HTTP_404_NOT_FOUND)


# aqui estoy serrando la secion
class logoutView(APIView):

    '''This is the view to close the section, you just have to send me the user's token by parameters'''

    def post(self, request, *args, **kwargs):
        serializer =  LogoutSerializer(data=request.data) 

        try:
            if serializer.is_valid():
                token_id = serializer.validated_data['token_id']
                token_instans = Token.objects.filter(key=token_id).first()
                if token_instans:
                    token_instans.delete()
                    return Response({'messege':'secion serrada exitosa'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error':'no existen ningun usuario'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':'introdusca el token'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error':'hubo algun tipo de exepcion , intentelo de nuevo'}, status=status.HTTP_400_BAD_REQUEST)


#aqio estoy creando un usuario 
class  Crearusuarioview(APIView):

    '''In this view I create the user and encrypt the password'''
    serializer_class = UserRegistroView
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            repeat_password = serializer.validated_data['repect_password']
            if password != repeat_password:
                return Response({'erro':'usuario creado sastifactoriamente'}, status=status.HTTP_404_NOT_FOUND)

            gmail = serializer.validated_data['gmail']
            nombre = serializer.validated_data['nombre']
            try:
                User.objects.create_user(username, gmail, password, nombre=nombre)
            except:
                return Response({'error':'this gmail exists in the data base'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'exito':'usuario creado sastifactoriamente'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'no introduciste los valores incorrectos'}, status=status.HTTP_400_BAD_REQUEST)