import jinja2

from django.templatetags.static import static
from django.urls import reverse
from wagtailmenus.templatetags.menu_tags import main_menu, sub_menu

from jinja2 import Environment

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'main_menu': jinja2.contextfunction(main_menu),
        'sub_menu': jinja2.contextfunction(sub_menu),
    })
    return env
