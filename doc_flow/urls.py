from django.urls import path
from .views import *

app_name = 'doc_flow'
urlpatterns = [
    path('', log_in, name='log_in'),
    path('log_in/', log_in, name='log_in'),
    path('about/', view_about, name='about'),
    path('file_download/<int:document_id>/', view_file_download, name='file_download'),
    path('student_docs/', view_student_documents, name='student_docs'),
    path('teacher_docs/', view_teacher_documents, name='teacher_docs'),
    path('add_doc/', AddDoc.as_view(), name='add_doc')
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
