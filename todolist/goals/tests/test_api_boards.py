from rest_framework.test import APITestCase
from django.test import Client
from django.urls import reverse
from todolist.core.models import User
from todolist.goals.models import Board, BoardParticipant


class BoardsApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test', is_superuser=True)
        cls.c = Client()
        cls.response = cls.c.login(username='test_user', password='test')

    def create_board(self):
        board = Board.objects.create(title="test_for_get")
        b_participant = BoardParticipant.objects.create(board=board, user=self.user)
        board.participants.set([b_participant])

        return board

    def test_board_create(self):
        url = "/goals/board/create"
        # print(url)
        title = 'Test_board1'
        response = self.c.post(url, {"title": title})
        # print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('title'), title)

    def test_board_list(self):
        board = self.create_board()

        url = "/goals/board/list"
        # print(url)
        response = self.c.get(url)
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get('id'), board.id)

    def test_board_get(self):
        board = self.create_board()

        url = f"/goals/board/{board.id}"
        # print(url)
        response = self.c.get(url)
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), board.id)

    def test_board_delete(self):
        board = self.create_board()

        url = f"/goals/board/{board.id}"
        # print(url)
        response = self.c.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(Board.objects.get(id=board.id).is_deleted)
