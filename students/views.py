from __future__ import absolute_import
import json as simplejson


from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView, CreateView, \
    UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q


from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


from core.utils import json, query, login_required
from .models import Student
from .forms import AdminForm, StudentForm
from .serializers import StudentSerializer


class HomeView(FormView):
    template_name = 'students/homepage.html'
    form_class = AdminForm
    success_url = '/students/dashboard/'

    def form_valid(self, form):
        self.request.session['email'] = form.cleaned_data['email']
        return super(HomeView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'students/dashboard.html'


class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'


class StudentUpdateView(SuccessMessageMixin, UpdateView):
    model = Student
    fields = ('name', 'email', 'state', 'city', 'gender', 'ph_no')
    template_name_suffix = '_update_form'
    # success_message = "The user %(self.object.name)s was edited " + \
    #                   "successfully!"


class StudentDetailView(DetailView):
    model = Student
    fields = ('name', 'email', 'state', 'city', 'gender', 'ph_no')


class StudentCreateView(SuccessMessageMixin, CreateView):
    model = Student
    fields = ('name', 'email', 'state', 'city', 'gender', 'ph_no')
    template_name_suffix = '_create_form'
    # success_message = "The user %(self.object.name)s was created " + \
    #                   "successfully!"


class StudentDeleteView(SuccessMessageMixin, DeleteView):
    model = Student
    template_name_suffix = '_delete_form'
    success_url = '/students/dashboard/'
    # success_message = "The user %(self.object.name)s was deleted " + \
    #                   "successfully!"


class LogoutView(TemplateView):
    template_name = 'students/logout.html'

    def get(self, request, *args, **kwargs):
        self.request.session.flush()
        return super(LogoutView, self).get(request, *args, **kwargs)


@csrf_exempt
def student_action(request, action):
    if action == 'find':
        q = request.GET.get('q', None)
        if q is not None:
            result = Student.objects.filter(
                Q(name__icontains=q))
            total = result.count()
            data = {'total': total, 'rows': json(result)}
        else:
            data = query(Student, request, {})
        return HttpResponse(simplejson.dumps(data))
    if action == 'add':
        form = StudentForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                o = form.save()
                data = {'success': True, 'msg': "The student is saved.", 'obj': json(o), 'isAdd': True}
                return HttpResponse(simplejson.dumps(data))
    if action == 'del':
        if request.method == "POST":
            pk = request.POST['pk']
            Student.objects.get(pk=pk).delete()
            data = {'success': True, 'msg': "The student is deleted.", 'obj': None}
            return HttpResponse(simplejson.dumps(data))
    if action.startswith('edit') > 0:
        if request.method == "POST":
            pk = action.split("/")[-1]
            instance = Student.objects.get(pk=pk)
            form = StudentForm(request.POST or None, instance=instance)
            if request.method == "POST":
                if form.is_valid():
                    o = form.save()
                    data = {'success': True, 'msg': "The student is edited.", 'obj': json(o), 'isAdd': False}
                    return HttpResponse(simplejson.dumps(data))


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'students': reverse('students:student_list', request=request, format=format),
    })


@method_decorator(login_required, name='dispatch')
class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


@method_decorator(login_required, name='dispatch')
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
