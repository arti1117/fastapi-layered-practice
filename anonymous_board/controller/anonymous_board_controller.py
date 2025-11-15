from http.client import HTTPException
from typing import List

from fastapi import APIRouter

from anonymous_board.controller.request.create_anonymous_board_request import CreateAnonymousBoardRequest
from anonymous_board.controller.response.anonymous_board_response import AnonymousBoardResponse
from anonymous_board.service.anonymous_board_service_impl import AnonymousBoardServiceImpl

anonymous_board_controller =  APIRouter(prefix="/board")
board_service = AnonymousBoardServiceImpl.getInstance()

@anonymous_board_controller.post("/create",
                                 response_model=AnonymousBoardResponse)
def create_anonymous_board(request: CreateAnonymousBoardRequest):
    created_board = board_service.create(request.title, request.content)

    return AnonymousBoardResponse(
        id=created_board.id,
        title=created_board.title,
        content=created_board.content,
        created_at=created_board.created_at
    )

@anonymous_board_controller.get("/list",
                                response_model=List[AnonymousBoardResponse])
def list_anonymous_boards():
    board_list = board_service.list()

    return [
        AnonymousBoardResponse(
            id=anonymous_board.id,
            title=anonymous_board.title,
            content=anonymous_board.content,
            created_at=anonymous_board.created_at.isoformat()
        ) for anonymous_board in board_list
    ]

@anonymous_board_controller.get("/{board_id}",
                                response_model=AnonymousBoardResponse)
def get_anonymous_board(board_id: str):
    try:
        anonymous_board = board_service.read(board_id)

    except ValueError:
        raise HTTPException(status_code=404, detail="Board not found")

    return AnonymousBoardResponse(
        id=anonymous_board.id,
        title=anonymous_board.title,
        content=anonymous_board.content,
        created_at=anonymous_board.created_at.isoformat()
    )