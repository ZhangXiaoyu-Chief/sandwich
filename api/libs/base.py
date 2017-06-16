from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CoreView(View):
    """
    所有API基类
    """
    def __init__(self, **kwargs):
        super(CoreView, self).__init__(**kwargs)
        self.response_data = {
            'status': True,
            'data': [],
            'info': '',
            'has_next': False,
            'has_previous': False,
            'total_page': 0,
            'per_page': 20
        }

    def parameters(self, key):
        """
        获取POST或者GET中的参数
        :param key: 
        :return: 
        """
        if self.request.method == 'GET':
            return self.request.GET.get(key)
        if self.request.method == 'POST':
            return self.request.POST.get(key)

    def get(self, request, *args, **kwargs):
        """
        收到GET请求后的处理
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        if 'action' not in kwargs:
            self.response_data['status'] = False
            self.response_data['info'] = 'Request action is empty'
            response_obj = JsonResponse(self.response_data)
            response_obj.status_code = 504
            return response_obj

        action = 'get_%s' % kwargs['action'].lower()
        return self.run(action, request)

    def post(self, request, *args, **kwargs):
        """
        收到POST请求后的处理
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        if 'action' not in kwargs:
            self.response_data['status'] = False
            self.response_data['info'] = 'Request action is empty'
            response_obj = JsonResponse(self.response_data)
            response_obj.status_code = 504
            return response_obj

        action = 'post_%s' % kwargs['action'].lower()
        return self.run(action, request)

    def run(self, action, request):
        """
        执行相应的逻辑
        :param action: 
        :param request: 
        :return: 
        """
        self.request = request

        if hasattr(self, action):
            func = getattr(self, action)
            try:
                func()
            except Exception as e:
                self.response_data['info'] = e
                self.response_data['status'] = False
                response_obj = JsonResponse(self.response_data)
                response_obj.status_code = 500
                return response_obj
        else:
            self.response_data['status'] = False
            self.response_data['info'] = 'Request action is invalid'
            response_obj = JsonResponse(self.response_data)
            response_obj.status_code = 501
            return response_obj
        return JsonResponse(self.response_data)

    def page_split(self, objs):
        page = self.parameters('page') if self.parameters('page') else 1
        per_page = None
        try:
            if per_page:
                per_page = int(per_page)
            else:
                per_page = getattr(settings, 'PER_PAGE', 20)
        except ValueError:
            per_page = getattr(settings, 'PER_PAGE', 20)

        paginator = Paginator(objs, per_page=per_page)
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except EmptyPage:
            objs = paginator.page(paginator.num_pages)
        self.response_data['has_previous'] = objs.has_previous()
        self.response_data['has_next'] = objs.has_next()
        self.response_data['total_page'] = paginator.num_pages
        self.response_data['pre_page'] = per_page
        return objs












