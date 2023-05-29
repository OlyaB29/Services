from rest_framework import serializers
from .models import MyFiles
from .config import TOKEN
import yadisk


class FileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyFiles
        fields = ('id', 'myfile')


class FileGetSerializer(serializers.ModelSerializer):
    myfile=serializers.SerializerMethodField(method_name='get_file_link')

    class Meta:
        model = MyFiles
        fields = "__all__"

    def get_file_link(self, obj):
        y = yadisk.YaDisk(token=TOKEN)
        link=y.get_download_link(str(obj.myfile))
        return link