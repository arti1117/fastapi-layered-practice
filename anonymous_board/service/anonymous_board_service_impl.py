from anonymous_board.repository.anonymous_board_repository_impl import AnonymousBoardRepositoryImpl
from anonymous_board.service.anonymous_board_service import AnonymousBoardService


class AnonymousBoardServiceImpl(AnonymousBoardService):
    __instance = None

    def __new__(cls):
        if cls. __instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.anonymous_board_repository = (
                AnonymousBoardRepositoryImpl.getInstance()
            )

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def create(self, title: str, content: str):
        return self.anonymous_board_repository.create(title, content)

    def list(self):
        return self.anonymous_board_repository.list()

    def read(self, board_id: str):
        read_board = self.anonymous_board_repository.find_by_id(board_id)
        if not read_board:
            raise ValueError("ID Not Found")

        return read_board