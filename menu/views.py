from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.views import View

from menu.models import Menu


class MenuView(View):

    def get(self, request: HttpRequest, path: str | None = None) -> HttpResponse:
        items = Menu.objects.all()
        root_menus = [item for item in items if item.parent_id is None]

        context = {
            "active_path": path or "",
            "root_menus": root_menus,
            "menu_items": items,
        }
        return TemplateResponse(request, "tree_page.html", context)