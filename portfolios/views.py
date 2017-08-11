# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import DetailView

from .models import Page


class PageDetail(DetailView):
    model = Page

    def get_template_names(self):
    	ts = super(PageDetail, self).get_template_names()
    	ts += ['portfolios/{}.html'.format(self.object.slug)]
    	return ts


class Home(PageDetail):
    """ Displays the home page. """

    def get_object(self):
        page, _created = Page.objects.get_or_create(slug='home')
        return page
