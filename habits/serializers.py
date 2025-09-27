from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычки"""
    
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Habit
        fields = (
            'id', 'user', 'place', 'time', 'action', 'is_pleasant',
            'related_habit', 'periodicity', 'reward', 'execution_time',
            'is_public', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def validate(self, attrs):
        """Дополнительная валидация на уровне сериализатора"""
        # Исключить одновременный выбор связанной привычки и указания вознаграждения
        if attrs.get('related_habit') and attrs.get('reward'):
            raise serializers.ValidationError(
                "Нельзя одновременно указывать связанную привычку и вознаграждение"
            )
        
        # В связанные привычки могут попадать только привычки с признаком приятной привычки
        related_habit = attrs.get('related_habit')
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError({
                'related_habit': 'В связанные привычки могут попадать только приятные привычки'
            })
        
        # У приятной привычки не может быть вознаграждения или связанной привычки
        if attrs.get('is_pleasant'):
            if attrs.get('reward'):
                raise serializers.ValidationError({
                    'reward': 'У приятной привычки не может быть вознаграждения'
                })
            if attrs.get('related_habit'):
                raise serializers.ValidationError({
                    'related_habit': 'У приятной привычки не может быть связанной привычки'
                })
        
        return attrs
    
    def create(self, validated_data):
        """Создание привычки с привязкой к текущему пользователю"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек (только для чтения)"""
    
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Habit
        fields = (
            'id', 'user', 'place', 'time', 'action', 'periodicity',
            'execution_time', 'created_at'
        )
        read_only_fields = ('id', 'user', 'place', 'time', 'action', 'periodicity', 'execution_time', 'created_at')


class PleasantHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для приятных привычек (для выбора в связанных привычках)"""
    
    class Meta:
        model = Habit
        fields = ('id', 'action')
        read_only_fields = ('id', 'action')
