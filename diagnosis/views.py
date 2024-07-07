from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from diagnosis.models import DiagnosisPicture
from diagnosis.serializers import DiagnosisPictureSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from users.authentication import JSONWebTokenAuthentication
from diagnosis.model import predict

class DiagnosisPictureView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    parser_classes = [FormParser, MultiPartParser]
    
    def post(self, request):
        data = dict(request.data)
        data['picture'] = data['picture'][0]
        data['user'] = request.user.id
        print(data)
        serializer = DiagnosisPictureSerializer(data=data)
        if serializer.is_valid():
            isinstance = serializer.save()
            prediction = predict(isinstance.picture.path)
            sorted_list = sorted(prediction.items(), key=lambda x: x[1], reverse=True)
            return Response(data=sorted_list, status=200)
        print(serializer.errors)
        return Response(data=serializer.errors, status=500)