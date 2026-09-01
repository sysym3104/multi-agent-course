"""TodoListのカテゴリ機能を中心としたテスト"""

import pytest

from todo import DEFAULT_CATEGORY, Todo, TodoList


def test_add_without_category_uses_default():
    """カテゴリ未指定で追加すると既定カテゴリになる"""
    tl = TodoList()
    todo = tl.add("買い物")
    assert todo.category == DEFAULT_CATEGORY


def test_add_with_category():
    """カテゴリを指定して追加できる。前後の空白は除去される"""
    tl = TodoList()
    todo = tl.add("企画書作成", "  仕事  ")
    assert todo.category == "仕事"


def test_add_with_blank_category_uses_default():
    """空白のみのカテゴリを指定すると既定カテゴリになる"""
    tl = TodoList()
    todo = tl.add("メモ", "   ")
    assert todo.category == DEFAULT_CATEGORY


def test_list_filter_by_category():
    """カテゴリ指定でその分類のTodoだけがid順で返る"""
    tl = TodoList()
    tl.add("企画書作成", "仕事")
    tl.add("牛乳を買う", "プライベート")
    tl.add("経費精算", "仕事")

    result = tl.list(category="仕事")
    assert [t.title for t in result] == ["企画書作成", "経費精算"]


def test_list_filter_by_category_and_incomplete():
    """カテゴリ絞り込みと未完了絞り込みはAND条件で適用される"""
    tl = TodoList()
    tl.add("企画書作成", "仕事")
    done = tl.add("経費精算", "仕事")
    tl.add("牛乳を買う", "プライベート")
    tl.complete(done.id)

    result = tl.list(include_completed=False, category="仕事")
    assert [t.title for t in result] == ["企画書作成"]


def test_list_without_category_returns_all():
    """カテゴリ未指定なら全カテゴリが対象になる"""
    tl = TodoList()
    tl.add("a", "仕事")
    tl.add("b", "プライベート")
    assert len(tl.list()) == 2


def test_set_category_updates_existing_todo():
    """既存Todoのカテゴリを変更できる"""
    tl = TodoList()
    todo = tl.add("引っ越し準備", "プライベート")
    updated = tl.set_category(todo.id, "仕事")
    assert updated.category == "仕事"
    assert tl.list(category="仕事")[0].id == todo.id


def test_set_category_with_blank_uses_default():
    """空白のみのカテゴリに変更すると既定カテゴリになる"""
    tl = TodoList()
    todo = tl.add("タスク", "仕事")
    updated = tl.set_category(todo.id, "  ")
    assert updated.category == DEFAULT_CATEGORY


def test_set_category_missing_id_raises_key_error():
    """存在しないIDを指定するとKeyError"""
    tl = TodoList()
    with pytest.raises(KeyError):
        tl.set_category(999, "仕事")


def test_categories_returns_sorted_unique():
    """categories()は重複を除きソートしたリストを返す"""
    tl = TodoList()
    tl.add("a", "仕事")
    tl.add("b", "プライベート")
    tl.add("c", "仕事")
    tl.add("d")
    assert tl.categories() == sorted(["仕事", "プライベート", DEFAULT_CATEGORY])


def test_str_includes_category():
    """__str__の各行にカテゴリが含まれる"""
    tl = TodoList()
    tl.add("企画書作成", "仕事")
    assert "(仕事)" in str(tl)


def test_existing_behavior_not_regressed():
    """既存の追加・完了・削除・件数カウントが従来どおり動く"""
    tl = TodoList()
    a = tl.add("a")
    b = tl.add("b")
    assert len(tl) == 2

    tl.complete(a.id)
    assert tl.list(include_completed=False) == [b]

    tl.delete(b.id)
    assert len(tl) == 1

    with pytest.raises(ValueError):
        tl.add("   ")


def test_todo_dataclass_default_category():
    """Todoデータクラス単体でも既定カテゴリを持つ"""
    todo = Todo(id=1, title="x")
    assert todo.category == DEFAULT_CATEGORY
