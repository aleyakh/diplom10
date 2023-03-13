from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from todolist.core.models import User
from todolist.core.serializers import ProfileSerializer
from todolist.goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant

from django.db import transaction


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if self.context['request'].user != value.user:
            raise PermissionDenied
        return value


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise ValidationError('Category not found')
        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise ValidationError('Goal not found')
        if not BoardParticipant.objects.filter(
            board_id=value.category.board_id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user_id=self.context['request'].user.id
        ).exists():
            raise PermissionDenied
        return value

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')


class GoalCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise ValidationError('Goal not found')
        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'goal')


class BoardCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", "is_deleted")
        fields = "__all__"


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices[1:])
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "is_deleted")

    def update(self, instance: Board, validated_data: dict) -> Board:
        with transaction.atomic():
            BoardParticipant.objects.filter(board=instance).exclude(user=self.context['request'].user).delete()
            BoardParticipant.objects.bulk_create([
                BoardParticipant(
                    user=participant['user'],
                    role=participant['role'],
                    board=instance
                )
                for participant in validated_data.pop('participants', [])
            ])

            if title := validated_data.get('title'):
                instance.title = title
                instance.save(update_fields=('title',))

        return instance
