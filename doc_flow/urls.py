from django.urls import path
from .views import *

app_name = 'doc_flow'
urlpatterns = [
    path('', log_in, name='log_in'),
    path('log_in/', log_in, name='log_in'),
    path('about/', view_about, name='about'),
    path('file_download/<int:document_id>/', view_file_download, name='file_download'),
    path('my_docs/', view_my_documents, name='my_docs'),
    path('student_docs_for_teacher/', view_student_docs_for_teacher, name='student_docs_for_teacher'),
    path('student_subjects/', view_student_subjects, name='student_subjects'),
    path('add_doc/', AddDoc.as_view(), name='add_doc')
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
