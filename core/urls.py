from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'timelogs', views.TimeLogViewSet)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.project_list, name='project_list'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('kanban/', views.kanban_board, name='kanban'),
    path('my-tasks/', views.my_tasks, name='my_tasks'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/<int:user_id>/delete/', views.employee_delete, name='employee_delete'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/comment/', views.add_comment, name='add_comment'),
    path('task/<int:task_id>/attachment/', views.upload_attachment, name='upload_attachment'),
    path('task/<int:task_id>/complete/', views.task_mark_complete, name='task_mark_complete'),
    path('task/<int:task_id>/log-time/', views.log_time, name='log_time'),
    path('api/', include(router.urls)),
]
