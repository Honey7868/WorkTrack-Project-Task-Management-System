from rest_framework import serializers
from .models import User, Project, Task, Comment, Attachment, TimeLog, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class ProjectSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class AttachmentSerializer(serializers.ModelSerializer):
    uploader_name = serializers.CharField(source='uploaded_by.username', read_only=True)

    class Meta:
        model = Attachment
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'uploaded_at']

class TimeLogSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.username', read_only=True)

    class Meta:
        model = TimeLog
        fields = '__all__'
        read_only_fields = ['employee']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
