"""Todoリストを管理するモジュール"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import count

# カテゴリ未指定時に使う既定カテゴリ
DEFAULT_CATEGORY = "未分類"


@dataclass
class Todo:
    """1件のTodo項目を表すデータクラス"""

    id: int
    title: str
    completed: bool = False
    category: str = DEFAULT_CATEGORY


class TodoList:
    """Todo項目の追加・一覧表示・完了マーク・削除を行うクラス"""

    def __init__(self) -> None:
        """空のTodoリストを初期化する"""
        self._todos: dict[int, Todo] = {}
        self._id_counter = count(1)

    def add(self, title: str, category: str | None = DEFAULT_CATEGORY) -> Todo:
        """新しいTodoを追加し、追加した項目を返す

        Args:
            title: Todoの内容
            category: 分類カテゴリ。未指定・空文字・空白のみの場合は「未分類」になる

        Returns:
            追加されたTodoオブジェクト

        Raises:
            ValueError: タイトルが空文字または空白のみの場合
        """
        if not title or not title.strip():
            raise ValueError("タイトルを指定してください")

        todo = Todo(
            id=next(self._id_counter),
            title=title.strip(),
            category=self._normalize_category(category),
        )
        self._todos[todo.id] = todo
        return todo

    def list(
        self,
        include_completed: bool = True,
        category: str | None = None,
    ) -> list[Todo]:
        """Todoの一覧を返す

        Args:
            include_completed: Trueの場合は完了済みも含める。Falseの場合は未完了のみ
            category: 指定した場合、そのカテゴリのTodoだけに絞り込む。
                Noneの場合は全カテゴリを対象にする

        Returns:
            id順に並んだTodoのリスト
        """
        todos = sorted(self._todos.values(), key=lambda t: t.id)
        if not include_completed:
            todos = [t for t in todos if not t.completed]
        if category is not None:
            target = self._normalize_category(category)
            todos = [t for t in todos if t.category == target]
        return todos

    def complete(self, todo_id: int) -> Todo:
        """指定したTodoを完了状態にする

        Args:
            todo_id: 完了にするTodoのID

        Returns:
            更新されたTodoオブジェクト

        Raises:
            KeyError: 指定したIDのTodoが存在しない場合
        """
        todo = self._get(todo_id)
        todo.completed = True
        return todo

    def set_category(self, todo_id: int, category: str | None) -> Todo:
        """指定したTodoのカテゴリを変更する

        Args:
            todo_id: 対象のTodoのID
            category: 新しいカテゴリ。空文字・空白のみ・Noneの場合は「未分類」になる

        Returns:
            更新されたTodoオブジェクト

        Raises:
            KeyError: 指定したIDのTodoが存在しない場合
        """
        todo = self._get(todo_id)
        todo.category = self._normalize_category(category)
        return todo

    def categories(self) -> list[str]:
        """登録されているTodoのカテゴリ一覧を返す

        Returns:
            重複を除いてソートしたカテゴリ名のリスト
        """
        return sorted({t.category for t in self._todos.values()})

    def delete(self, todo_id: int) -> Todo:
        """指定したTodoを削除する

        Args:
            todo_id: 削除するTodoのID

        Returns:
            削除されたTodoオブジェクト

        Raises:
            KeyError: 指定したIDのTodoが存在しない場合
        """
        self._get(todo_id)
        return self._todos.pop(todo_id)

    def _get(self, todo_id: int) -> Todo:
        """IDからTodoを取得する内部ヘルパー

        Raises:
            KeyError: 指定したIDのTodoが存在しない場合
        """
        if todo_id not in self._todos:
            raise KeyError(f"ID {todo_id} のTodoは存在しません")
        return self._todos[todo_id]

    @staticmethod
    def _normalize_category(category: str | None) -> str:
        """カテゴリ文字列を正規化する内部ヘルパー

        前後の空白を除去し、空文字・空白のみ・Noneの場合は既定カテゴリを返す
        """
        if category is None:
            return DEFAULT_CATEGORY
        normalized = category.strip()
        return normalized or DEFAULT_CATEGORY

    def __len__(self) -> int:
        """登録されているTodoの件数を返す"""
        return len(self._todos)

    def __str__(self) -> str:
        """Todoリストの中身を人間が読みやすい文字列で返す

        Returns:
            id順に並んだ各Todoを1行ずつ表した文字列。
            リストが空の場合は「(Todoはありません)」を返す
        """
        todos = self.list()
        if not todos:
            return "(Todoはありません)"
        lines = [
            f"[{'✔' if t.completed else ' '}] {t.id}: {t.title} ({t.category})"
            for t in todos
        ]
        return "\n".join(lines)
