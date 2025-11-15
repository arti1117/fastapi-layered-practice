from typing import List

from anonymous_board.entity.anonymous_board import AnonymousBoard
from anonymous_board.repository.anonaymous_board_repository import AnonymousBoardRepository
from config.mysql_config import SessionLocal


class AnonymousBoardRepositoryImpl(AnonymousBoardRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def create(self, title: str, content: str) -> AnonymousBoard:
        db = SessionLocal()

        try:
            board = AnonymousBoard(title=title, content=content)
            db.add(board)
            db.commit()
            db.refresh(board)
            return board

        except:
            db.rollback()
            raise

        finally:
            db.close()


    def list(self) -> List[AnonymousBoard]:
        db = SessionLocal()

        try:
            return db.query(AnonymousBoard).order_by(AnonymousBoard.created_at.desc()).all()

        except:
            raise

        finally:
            db.close()

    def find_by_id(self, id: str) -> AnonymousBoard:
        db = SessionLocal()

        try:
            # return db.query(AnonymousBoard).get(id)
            return (db.query(AnonymousBoard).
                    filter(AnonymousBoard.id == id).first())
        except:
            raise

        finally:
            db.close()

