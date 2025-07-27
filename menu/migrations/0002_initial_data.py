from django.db import migrations


def create_menu_hierarchy(apps, schema_editor) -> None:
    Menu = apps.get_model("menu", "Menu")

    def add_children(parent, level: int, max_level: int, prefix: str) -> None:
        if level > max_level:
            return
        for index in range(1, 3):
            name = f"{prefix} {level}-{index}"
            path = f"{parent.path}/{name}" if parent else name
            child = Menu.objects.create(name=name, parent=parent, path=path)
            add_children(child, level + 1, max_level, prefix)

    for root_index in range(1, 6):
        root_name = f"Root {root_index}"
        root = Menu.objects.create(name=root_name, path=root_name)
        add_children(root, 1, 5, f"Item {root_index}")


def remove_menu_hierarchy(apps, schema_editor) -> None:

    Menu = apps.get_model("menu", "Menu")
    Menu.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_menu_hierarchy, remove_menu_hierarchy),
    ]
