from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.views import View

from menu.models import Menu


class MenuView(View):

    def get(self, request: HttpRequest, path: str | None = None) -> HttpResponse:

        active_path = path or ""
        if active_path:
            root_segment = active_path.split("/", 1)[0]
            filters = Q(parent__isnull=True) | Q(path__startswith=root_segment)
        else:
            filters = Q(parent__isnull=True) | Q(parent__parent__isnull=True)

        qs = Menu.objects.filter(filters)
        items = [item for item in qs]
        root_menus = [item for item in items if item.parent_id is None]

        context = {
            "active_path": active_path,
            "root_menus": root_menus,
            "menu_items": items,
        }
        return TemplateResponse(request, "tree_page.html", context)