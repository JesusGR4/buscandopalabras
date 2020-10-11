# -*- coding: utf-8 -*-
from django import template

from article.models import Menu

register = template.Library()


def get_link_attributes(item):
    href = item.link
    if item.is_page():
        href = '/p/{}'.format(item.item.slug)
    if item.is_post():
        href = '/palabra/{}'.format(item.item.slug)

    return {
        'href': href,
        'title': item.title,
        'name': item.name,
    }


def get_links_from_menu(menu):
    return [get_link_attributes(item) for item in menu.items.all()] if menu else []


@register.simple_tag
def header_menu():
    menu = Menu.objects.filter(is_active=True, placement=Menu.HEADER).last()

    return get_links_from_menu(menu)


@register.simple_tag
def footer_menu():
    menu = Menu.objects.filter(is_active=True, placement=Menu.FOOTER).last()

    return get_links_from_menu(menu)
