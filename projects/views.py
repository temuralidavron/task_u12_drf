from django.db.models import Q
from django.template.context_processors import request
from rest_framework import permissions, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Project, Task
from .permissions import IsProjectOwnerOrMember, OnlyAdmin
from .serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    # permission_classes = (permissions.IsAuthenticated, IsProjectOwnerOrMember)
    permission_classes = [OnlyAdmin,]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        # Agar saqlash paytida qoʻshimcha mantiq kerak boʻlsa,
        # faqat ushbu metodning oʻzini ham override qilish mumkin
        serializer.save(owner=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectOwnerOrMember)

    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.filter(Q(project__owner=user) | Q(project__members=user)).distinct()
        project_id = self.request.query_params.get('project')
        if project_id:
            qs = qs.filter(project_id=project_id)
        status_value = self.request.query_params.get('status')
        if status_value:
            qs = qs.filter(status=status_value)
        return qs
