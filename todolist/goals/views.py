from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from todolist.goals.filters import GoalDateFilter
from todolist.goals.models import GoalCategory, Goal, GoalComment, BoardParticipant, Board
from todolist.goals.permissions import BoardPermissions, GoalCategoryPermissions, GoalPermissions, \
    GoalCommentsPermissions
from todolist.goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardSerializer


class BoardCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer

    def perform_create(self, serializer):
        BoardParticipant.objects.create(user=self.request.user, board=serializer.save())


class BoardListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(
            participants__user_id=self.request.user.id,
            is_deleted=False
        )


class BoardView(RetrieveUpdateDestroyAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(is_deleted=False)

    def perform_destroy(self, instance: Board) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted', ))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategoryListView
    permission_classes = [GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted', ))
            instance.goals.update(status=Goal.Status.archived)


class GoalCreateView(CreateAPIView):
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title", 'description']

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user_id=self.request.user.id,
            category__is_deleted=False
        ).exclude(status=Goal.Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return (
            Goal.objects
            .filter(category__board__participants__user_id=self.request.user.id, category__is_deleted=False)
            .exclude(status=Goal.Status.archived)
        )

    def perform_destroy(self, instance:Goal):
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentCreateView(CreateAPIView):
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [GoalCommentsPermissions]


class GoalCommentListView(ListAPIView):
    permission_classes = [GoalCommentsPermissions]
    serializer_class = GoalCommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user_id=self.request.user.id)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalCommentsPermissions]
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        return GoalComment.objects.select_related('user').filter(user_id=self.request.user.id)
