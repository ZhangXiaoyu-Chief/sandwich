from django.shortcuts import render, HttpResponse
from api.libs.base import CoreView
import os
import time
from django.conf import settings

class Upload(CoreView):
    """

    """

    def __get_file_name(self):
        """
        生成时间戳类型的文件名函数，避免文件名重复的问题
        :return:
        """

        return str(time.time()).replace('.', '')

    def __handle_uploaded_file(self, f, filename, path=None, ):
        """
        上传文件函数
        :param f: 文件类型的form对象ImageField
        :param filename: 文件名
        :param path: 路径（相对）
        :return:
        """
        if path is None:
            path = './'
        with open(os.path.join(path, filename), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def post_upload_avatar(self):
        """
        上传图片
        :return: 
        """
        try:
            file_data = self.request.FILES.get('file')
            filename = '%s.%s' % (self.__get_file_name(), file_data.name.split('.')[-1])
            file_str = '%s/%s' % (settings.UPLOADS_PATH['avatar'], filename)
            self.__handle_uploaded_file(file_data, filename,
                                 os.path.join(settings.BASE_DIR, settings.UPLOADS_PATH['avatar']))
            self.response_data['data'] = file_str
        except:
            self.response_data['status'] = False
            self.status_code = 500
