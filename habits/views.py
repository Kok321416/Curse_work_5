from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Habit
from .serializers import HabitSerializer, PublicHabitSerializer, PleasantHabitSerializer
from .permissions import IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с привычками пользователя"""
    
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_pleasant', 'is_public']
    
    def get_queryset(self):
        """Возвращает только привычки текущего пользователя"""
        return Habit.objects.filter(user=self.request.user).select_related('related_habit')
    
    @action(detail=False, methods=['get'])
    def pleasant_habits(self, request):
        """Получить список приятных привычек пользователя для выбора в связанных привычках"""
        pleasant_habits = self.get_queryset().filter(is_pleasant=True)
        serializer = PleasantHabitSerializer(pleasant_habits, many=True)
        return Response(serializer.data)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра публичных привычек"""
    
    queryset = Habit.objects.filter(is_public=True).select_related('user')
    serializer_class = PublicHabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']