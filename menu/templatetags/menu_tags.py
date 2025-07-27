from typing import Iterable, Optional

from django import template

from menu.models import Menu

register = template.Library()


class TreeNode:

    def __init__(self, menu: Menu) -> None:
        self.menu = menu
        self.children: list["TreeNode"] = []


def build_tree(items: Iterable[Menu]) -> tuple[Optional[TreeNode], dict[int, TreeNode]]:
    nodes = {item.id: TreeNode(item) for item in items}
    root = None
    for item in items:
        node = nodes[item.id]
        if item.parent_id is None:
            root = node
        else:
            nodes[item.parent_id].children.append(node)
    return root, nodes


@register.inclusion_tag("menu/menu.html", takes_context=True)
def draw_menu(context: dict, menu_name: str) -> dict:

    active_path: str = context.get("active_path", "")
    items: list[Menu]
    all_items: Iterable[Menu] | None = context.get("menu_items")

    items = [
        item
        for item in all_items
        if item.name == menu_name or item.path.startswith(f"{menu_name}/")
    ]
    root, nodes = build_tree(items)

    path_map = {item.path: nodes[item.id] for item in items}
    open_paths: set[str] = set()
    active = path_map.get(active_path)
    if active:
        open_paths.add(active.menu.path)
        parent = active.menu.parent_id and nodes.get(active.menu.parent_id)
        while parent:
            open_paths.add(parent.menu.path)
            parent = parent.menu.parent_id and nodes.get(parent.menu.parent_id)
        for child in active.children:
            open_paths.add(child.menu.path)
    elif root and not active_path:
        open_paths.add(root.menu.path)

    return {
        "node": root,
        "open_paths": open_paths,
        "active_path": active_path,
    }