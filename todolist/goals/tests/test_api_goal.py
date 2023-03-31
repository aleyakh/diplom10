from django.test import TestCase, Client

from rest_framework.test import APITestCase

from todolist.core.models import User
from todolist.goals.models import Board, GoalCategory, Goal, BoardParticipant


class GoalApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user_test', password='test', is_superuser=True)
        cls.c = Client()
        cls.response = cls.c.login(username='user_test', password='test')

    def create_category(self):
        board = Board.objects.create(title="test_for_get")
        b_participant = BoardParticipant.objects.create(board=board, user=self.user)
        board.participants.set([b_participant])
        category = GoalCategory.objects.create(title="Test_goal_category", board=board, user=self.user)
        return category

    def create_goal(self):
        category = self.create_category()
        goal = Goal.objects.create(title="Test_goal", category=category, user=self.user)
        return goal

    def test_goal_create(self):
        url = "/goals/goal/create"
        # print(url)

        category = self.create_category()
        data = {
            "title": "test_goal2",
            "category": category.id,
            "user": self.user
        }
        response = self.c.post(url, data)
        # print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('title'), "test_goal2")

    def test_goal_list(self):
        goal = self.create_goal()

        url = "/goals/goal/list"
        # print(url)
        response = self.c.get(url)
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get('id'), goal.id)

    def test_goal_get(self):
        goal = self.create_goal()

        url = f"/goals/goal/{goal.id}"
        # print(url)
        response = self.c.get(url)
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), goal.id)

    def test_goal_delete(self):
        goal = self.create_goal()
        self.assertEqual(goal.status, 1)

        url = f"/goals/goal/{goal.id}"
        # print(url)
        response = self.c.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Goal.objects.get(id=goal.id).status, 4)


