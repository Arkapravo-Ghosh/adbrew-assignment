from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..db import db
from .entities import Todo
from .repository import TodoRepository
from .validators import validate_create_payload

TODOS_COLLECTION = "todos"


def _to_representation(todo: Todo) -> dict:
    return {
        "id": todo.id,
        "description": todo.description,
        "created_at": todo.created_at,
    }


class TodoListView(APIView):
    repository = TodoRepository(db[TODOS_COLLECTION])

    def get(self, request):
        todos = self.repository.list_all()
        return Response(
            [_to_representation(todo) for todo in todos],
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        description = validate_create_payload(request.data)
        todo = self.repository.create(description)
        return Response(_to_representation(todo), status=status.HTTP_201_CREATED)

    def delete(self, request):
        self.repository.delete_all()
        return Response(status=status.HTTP_204_NO_CONTENT)
