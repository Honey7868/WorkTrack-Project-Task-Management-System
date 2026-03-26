from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from .models import Project, Task, Comment, TimeLog
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer, TimeLogSerializer

@login_required
def dashboard(request):
    import datetime
    from .models import User, Project, Task, Comment

    if request.user.role == 'ADMIN':
        from django.contrib.auth.models import Group
        context = {
            'total_projects': Project.objects.count(),
            'active_tasks': Task.objects.exclude(status='COMPLETED').count(),
            'total_employees': User.objects.filter(role='EMPLOYEE').count(),
            'approaching_deadlines': Task.objects.filter(deadline__lte=datetime.date.today() + datetime.timedelta(days=7)).count(),
            'recent_comments': Comment.objects.order_by('-created_at')[:5],
            'teams': Group.objects.prefetch_related('user_set').all()
        }
        return render(request, 'dashboard/admin_dashboard.html', context)
    else:
        from django.contrib.auth.models import Group
        import datetime
        context = {
            'tasks_assigned': Task.objects.filter(assigned_to=request.user).count(),
            'in_progress': Task.objects.filter(assigned_to=request.user, status='IN_PROGRESS').count(),
            'completed': Task.objects.filter(assigned_to=request.user, status='COMPLETED').count(),
            'teams': Group.objects.prefetch_related('user_set').all(),
            'upcoming_tasks': Task.objects.filter(assigned_to=request.user, deadline__gte=datetime.date.today()).exclude(status='COMPLETED').order_by('deadline')[:5]
        }
        return render(request, 'dashboard/employee_dashboard.html', context)

@login_required
def project_list(request):
    from .models import Project
    if request.user.role == 'ADMIN':
        projects = Project.objects.all().order_by('-created_at')
    else:
        projects = Project.objects.filter(tasks__assigned_to=request.user).distinct().order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def kanban_board(request):
    from .models import Task
    if request.user.role == 'ADMIN':
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)
    
    context = {
        'todo_tasks': tasks.filter(status='NOT_STARTED'),
        'in_progress_tasks': tasks.filter(status='IN_PROGRESS'),
        'completed_tasks': tasks.filter(status='COMPLETED'),
        'csrf_token': request.META.get('CSRF_COOKIE', '')
    }
    return render(request, 'tasks/kanban_board.html', context)

@login_required
def my_tasks(request):
    from .models import Task
    tasks = Task.objects.filter(assigned_to=request.user).order_by('deadline')
    return render(request, 'tasks/my_tasks.html', {'tasks': tasks})

@login_required
def employee_list(request):
    from .models import User
    from django.shortcuts import redirect
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    employees = User.objects.all().order_by('-date_joined')
    return render(request, 'management/employee_list.html', {'employees': employees})

@login_required
def employee_delete(request, user_id):
    from .models import User
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    emp = get_object_or_404(User, id=user_id)
    if emp.role != 'ADMIN' and emp != request.user:
        emp.delete()
        messages.success(request, f"Employee {emp.username} deleted successfully.")
    return redirect('employee_list')

@login_required
def task_detail(request, task_id):
    from .models import Task
    from django.shortcuts import get_object_or_404
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def project_detail(request, project_id):
    from .models import Project
    from django.shortcuts import get_object_or_404
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/project_detail.html', {'project': project})

@login_required
def add_comment(request, task_id):
    from .models import Task, Comment
    from django.shortcuts import get_object_or_404, redirect
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(task=task, user=request.user, content=content)
    return redirect('task_detail', task_id=task_id)

@login_required
def upload_attachment(request, task_id):
    from .models import Task, Attachment
    from django.shortcuts import get_object_or_404, redirect
    if request.method == 'POST' and request.FILES.get('file'):
        task = get_object_or_404(Task, id=task_id)
        file = request.FILES['file']
        Attachment.objects.create(task=task, uploaded_by=request.user, file=file)
    return redirect('task_detail', task_id=task_id)

@login_required
def task_mark_complete(request, task_id):
    from .models import Task
    from django.shortcuts import get_object_or_404, redirect
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.status = 'COMPLETED'
        task.save()
    return redirect('task_detail', task_id=task_id)

@login_required
def log_time(request, task_id):
    from .models import Task, TimeLog
    from django.shortcuts import get_object_or_404, redirect
    from django.utils import timezone
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        hours = request.POST.get('hours')
        description = request.POST.get('description', '')
        if hours:
            TimeLog.objects.create(
                task=task, 
                employee=request.user, 
                hours_logged=hours, 
                description=description, 
                date=timezone.now().date()
            )
    return redirect('task_detail', task_id=task_id)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TimeLogViewSet(viewsets.ModelViewSet):
    queryset = TimeLog.objects.all()
    serializer_class = TimeLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)
