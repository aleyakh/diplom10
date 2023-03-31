from django.test import TestCase, Client

from rest_framework.test import APITestCase

from todolist.core.models import User
from todolist.goals.models import Board, GoalCategory, Goal, BoardParticipant, GoalComment


class GoalApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user_test', password='test', is_superuser=True)
        cls.c = Client()
        cls.response = cls.c.login(username='user_test', password='test')

    def create_goal(self):
        board = Board.objects.create(title="test_for_get")
        b_participant = BoardParticipant.objects.create(board=board, user=self.user)
        board.participants.set([b_participant])
        category = GoalCategory.objects.create(title="Test_goal_category", board=board, user=self.user)
        goal = Goal.objects.create(title="Test_goal", category=category, user=self.user)
        return goal

    def create_comment(self):
        goal = self.create_goal()
        comment = GoalComment.objects.create(
            text="comment text",
            goal=goal,
            user=self.user
        )
        return comment

    def test_comment_create(self):
        url = "/goals/goal_comment/create"

        goal = self.create_goal()
        data = {
            "text": "comment text",
            "goal": goal.id,
            "user": self.user
        }
        response = self.c.post(url, data)
        # print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('id'), goal.id)

    def test_comment_list(self):
        comment = self.create_comment()

        url = "/goals/goal_comment/list"
        # print(url)
        response = self.c.get(url)
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get('id'), comment.id)

    def test_comment_get(self):
        comment = self.create_comment()

        url = f"/goals/goal_comment/{comment.id}"
        # print(url)
        response = self.c.get(url)
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), comment.id)

    def test_comment_delete(self):
        comment = self.create_comment()

        url = f"/goals/goal_comment/{comment.id}"
        # print(url)
        response = self.c.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertRaises(GoalComment.DoesNotExist, GoalComment.objects.get)


