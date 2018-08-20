from rest_framework.generics import ListAPIView
from app1.models import requset_pu
from .serilizers import requestserilizer
from rest_framework.response import Response
from rest_framework import views
class request_api(views.APIView):
    def get(self,request):
        added_var1 = [{"added_var": requset_pu.objects.all().filter(r_user=request.user).count()}]
        final = requestserilizer(added_var1, many=True).data
        return Response(final)




