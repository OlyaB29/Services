from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .models import MyFiles
from .serializers import FileCreateSerializer, FileGetSerializer
from .config import TOKEN
from .selectel_config import URL, AUTH_TOKEN
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
            y.upload(uploaded_file, "/test-dir/{}".format(uploaded_file.name))
            file_path = "/test-dir/{}".format(uploaded_file.name)
            serializer.save(myfile=file_path)

        return Response(serializer.data)

class SelectelFilesViewSet(viewsets.ModelViewSet):
    queryset = MyFiles.objects.all()
    serializer_class = FileCreateSerializer

    def post(self, request):
        serializer = FileCreateSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = request.FILES["myfile"]
            requests.put(
                URL + "/test-dir/{}".format(uploaded_file.name),
                headers={'X-Auth-Token': AUTH_TOKEN}, files={'file': uploaded_file})

            file_path = "/test-dir/{}".format(uploaded_file.name)
            serializer.save(myfile=file_path)

        return Response(serializer.data)

