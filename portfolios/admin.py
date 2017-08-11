# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ordered_model.admin import OrderedTabularInline, OrderedModelAdmin

from .models import *


class EmbeddedContentInline(OrderedTabularInline):
    model = EmbeddedContent
    fields = ('content', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)


class ProjectInline(OrderedTabularInline):
    model = Project
    fields = ('client', 'name', 'category', 'roles', 'date', 'url', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)


class ClientAdmin(OrderedModelAdmin):
    list_display = ('name', 'description', 'order', 'move_up_down_links')
    inlines = [
        ProjectInline
    ]

    def get_urls(self):
        urls = super(ClientAdmin, self).get_urls()
        for inline in self.inlines:
            if hasattr(inline, 'get_urls'):
                urls = inline.get_urls(self) + urls
        return urls

    def get_queryset(self, request):
        qs = super(ClientAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(page__owner=request.user)


class TestimonialInline(OrderedTabularInline):
    model = Testimonial
    fields = ('author', 'title', 'body', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)


class PageAdmin(admin.ModelAdmin):
    inlines = [
        EmbeddedContentInline,
        TestimonialInline
    ]
    filter_horizontal = ('clients',)

    def get_urls(self):
        urls = super(PageAdmin, self).get_urls()
        for inline in self.inlines:
            if hasattr(inline, 'get_urls'):
                urls = inline.get_urls(self) + urls
        return urls

    def get_queryset(self, request):
        qs = super(PageAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        if request.user.is_superuser:
            return []
        return ['owner']


#admin.site.register(Testimonial)
admin.site.register(Role)
#admin.site.register(Project)
admin.site.register(Client, ClientAdmin)
admin.site.register(Page, PageAdmin)
