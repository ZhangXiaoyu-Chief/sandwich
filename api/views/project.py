from django.shortcuts import render, HttpResponse
from api.libs.base import CoreView
from cmdb.models import BusinessUnit
from django.db.utils import IntegrityError


class Project(CoreView):
    """
    项目接口类
    """

    def get_list(self):
        per_page = self.parameters("per_page")
        if per_page:
            project_objs = self.page_split(BusinessUnit.objects.all())
        else:
            project_objs = BusinessUnit.objects.all()

        project_list = []
        for project_obj in project_objs:
            project_list.append(project_obj.get_info())
        print(project_list)
        self.response_data['data'] = project_list

    def post_create(self):

        try:
            name = self.parameters("name")
            parent = int(self.parameters("parent"))
            memo = self.parameters("memo")
            parent_project = BusinessUnit.objects.filter(id=parent).first()

            if parent_project:
                project_obj = BusinessUnit(name=name, parent_unit=parent_project, memo=memo)
            else:
                project_obj = BusinessUnit(name=name, memo=memo)
            project_obj.save()
            self.response_data['data'] = project_obj.get_info()
        except IntegrityError:
            self.response_data['status'] = False
            self.status_code = 416
        except Exception:
            self.response_data['status'] = False
            self.status_code = 500

    def post_delete(self):
        project_id = self.parameters("project_id")
        try:
            project_obj = BusinessUnit.objects.filter(id=project_id).first()
            project_obj.delete()
        except Exception as e:
            self.response_data['status'] = False
            self.status_code = 500

    def post_change(self):
        try:
            project_id = self.parameters("id")
            name = self.parameters("name")
            parent = int(self.parameters("parent_id"))
            memo = self.parameters("memo")
            project_obj = BusinessUnit.objects.filter(id=project_id).first()
            if project_obj:
                if parent:

                    parent_project = BusinessUnit.objects.filter(id=parent).first()
                    print(parent_project)
                else:
                    parent_project = None

                project_obj.name = name
                project_obj.memo = memo
                project_obj.parent_unit = parent_project
                project_obj.save()
                self.response_data['data'] = project_obj.get_info()
            else:
                self.response_data['status'] = False
                self.status_code = 404
        except IntegrityError:
            self.response_data['status'] = False
            self.status_code = 416
        except Exception:
            self.response_data['status'] = False
            self.status_code = 500
