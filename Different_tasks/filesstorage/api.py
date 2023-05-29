from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .models import MyFiles
from .serializers import FileCreateSerializer, FileGetSerializer
from .config import TOKEN
import yadisk
import requests


class MyFilesViewSet(viewsets.ModelViewSet):
    queryset = MyFiles.objects.all()
    serializer_class = FileGetSerializer

    def post(self, request):
        serializer = FileCreateSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = request.FILES["myfile"]
            y = yadisk.YaDisk(token=TOKEN)
            y.remove("/test-dir/{}".format(uploaded_file.name), permanently=True)
            # link = y.upload(uploaded_file, "/test-dir/{}".format(uploaded_file.name)).href
            # file_link = requests.get(link, headers={'Authorization': 'OAuth ' + TOKEN}).json()['file']
            y.upload(uploaded_file, "/test-dir/{}".format(uploaded_file.name))
            file_path = "/test-dir/{}".format(uploaded_file.name)
            serializer.save(myfile=file_path)

        return Response(serializer.data)
