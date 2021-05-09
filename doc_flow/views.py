import mimetypes
import os

from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import *
from .forms import *
from diplom import settings


class SubjectDocs:
    def __init__(self, subject, documents):
        self.subject = subject
        self.documents = documents


def get_user_type(user):
    if hasattr(user, 'student'):
        user_type = 'student'
    elif hasattr(user, 'teacher'):
        user_type = 'teacher'
    else:
        user_type = None
    return user_type


def log_in(request):

    if 'log_in_but' in request.GET:
        username = request.GET['username']
        password = request.GET['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = redirect('/about/')
            return response
        else:
            return render(request, 'login.html', {'login_error': True})
    if 'log_out_nav_but' in request.GET:
        logout(request)
        return render(request, 'login.html', {'login_error': False})
    return render(request, 'login.html', {'login_error': False})


def view_about(request):
    return render(request, 'about.html', context={'user_type': get_user_type(request.user)})


def view_my_documents(request):
    documents = Document.objects.filter(user=request.user)
    return render(request, 'my_docs.html', context={'documents': documents, 'user_type': get_user_type(request.user)})


def view_student_docs_for_teacher(request):
    subject_docs = []
    subjects = Subject.objects.filter(teacher=request.user.teacher)
    for subject in subjects:
        documents = Document.objects.filter(subject=subject, doc_type='student')
        sub_docs = SubjectDocs(subject, documents)
        subject_docs.append(sub_docs)
    return render(request, 'subject_documents.html', context={'title': 'Документы студентов', 'subject_docs': subject_docs, 'user_type': get_user_type(request.user)})


def view_student_subjects(request):
    subject_docs = []
    subjects = Subject.objects.filter(semester=request.user.student.semester)
    for subject in subjects:
        documents = Document.objects.filter(subject=subject, doc_type='teacher')
        sub_docs = SubjectDocs(subject, documents)
        subject_docs.append(sub_docs)
    return render(request, 'subject_documents.html', context={'title': 'Документы дисциплин', 'subject_docs': subject_docs, 'user_type': get_user_type(request.user)})


def view_file_download(request, document_id):
    path = Document.objects.get(id=document_id).document.path
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


class AddDoc(View):

    def get(self, request):
        form = DocumentForm()
        choices = form.fields['subject'].queryset
        current_user = get_user_type(request.user)
        if current_user == 'student':
            filtered_choices = choices.filter(semester=request.user.student.semester)
        else:
            filtered_choices = choices.filter(teacher=request.user.teacher)
        form.fields['subject'].queryset = filtered_choices
        return render(request, 'add_doc.html', context={'form': form, 'add_doc_error': False, 'user_type': get_user_type(request.user)})

    def post(self, request):
        post_doc = request.POST.copy()
        post_doc.__setitem__('user', request.user.id)
        post_doc.__setitem__('doc_type', get_user_type(request.user))
        bound_form_doc = DocumentForm(post_doc, request.FILES)
        if bound_form_doc.is_valid():
            _ = bound_form_doc.save()
            response = redirect('/add_doc/')
            return response
        return render(request, 'add_doc.html', context={'form': bound_form_doc, 'add_doc_error': True, 'user_type': get_user_type(request.user)})
