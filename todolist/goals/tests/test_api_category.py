from rest_framework.test import APITestCase
from django.test import Client
from todolist.core.models import User
from todolist.goals.models import Board, BoardParticipant, GoalCategory


class GoalCategoryApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user_test', password='test', is_superuser=True)
        cls.c = Client()
        cls.response = cls.c.login(username='user_test', password='test')

    def create_board(self):
        board = Board.objects.create(title="test_for_get")
        b_participant = BoardParticipant.objects.create(board=board, user=self.user)
        board.participants.set([b_participant])

        return board

    def create_category(self):
        board = self.create_board()
        category = GoalCategory.objects.create(title="Test_goal_category", board=board, user=self.user)
        return category

    def test_goal_category_create(self):
        board = self.create_board()
        title = "Test_goal_category"

        url = "/goals/goal_category/create"
        # print(url)
        response = self.c.post(url, {"title": title, "board": board.id})
        # print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('title'), title)

    def test_goal_category_list(self):
        category = self.create_category()
        url = "/goals/goal_category/list"
        # print(url)
        response = self.c.get(url)
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], category.id)

    def test_goal_category_delete(self):
        category = self.create_category()

        url = f"/goals/goal_category/{category.id}"
        # print(url)
        response = self.c.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(GoalCategory.objects.get(id=category.id).is_deleted)