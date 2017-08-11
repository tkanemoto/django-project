# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ordered_model.models import OrderedModel


UPLOAD_FOLDER = 'uploads/%Y-%m-%d/'


class Page(models.Model):
    slug = models.SlugField('slug')
    owner = models.ForeignKey('auth.User', null=True)
    title = models.CharField('title', max_length=100, null=True, help_text='Title text to display')
    subtitle = models.CharField('subtitle', max_length=200, null=True, help_text='Text to display below the title')
    description = models.CharField('description', max_length=400, null=True, blank=True, help_text='Short description for search engines')
    showreel = models.FileField(null=True, blank=True, upload_to=UPLOAD_FOLDER, help_text='The showreel file')
    about = models.TextField('about', max_length=1000, null=True, blank=True, help_text='Text shown in the About section')
    mugshot = models.ImageField(null=True, blank=True, upload_to=UPLOAD_FOLDER, help_text='Your profile picture shown in the About section')
    quote = models.TextField('quote', max_length=1000, null=True, blank=True, help_text='Something profound')
    quote_citation = models.CharField('quote citation', max_length=20, null=True, blank=True, help_text='Some profound person')
    quote_background = models.ImageField(blank=True, null=True, upload_to=UPLOAD_FOLDER)
    clients = models.ManyToManyField('Client', blank=True, help_text='Select the clients you would like to be listed in the Credits section')
    number_of_featured_clients = models.IntegerField('number of featured clients', default=5, help_text='The number of clients to show in the big carousel')
    footer_background = models.ImageField(blank=True, null=True, upload_to=UPLOAD_FOLDER)

    def __unicode__(self):
        return '{} {}'.format(self.title, self.description if self.description is not None else '')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('portfolios-page', kwargs={'slug': self.slug})

    def featured_clients(self):
        return self.clients.all().filter(order__lt=self.number_of_featured_clients)

    def non_featured_clients(self):
        return self.clients.all().filter(order__gte=self.number_of_featured_clients)

    def roles(self):
        return set(self.clients.all().values_list('project__roles__name', flat=True))

    def products(self):
        return set(self.clients.all().values_list('project__roles__product', flat=True))


class EmbeddedContent(OrderedModel):
    content = models.TextField(max_length=1000, help_text='Paste in the embedded content from SoundCloud / YouTube etc.')
    page = models.ForeignKey('Page')
    order_with_respect_to = 'page'

    def __unicode__(self):
        if 'soundcloud.com/player' in self.content:
            return 'SoundCloud track'
        return 'Embedded content'


class Client(OrderedModel):
    name = models.CharField('name', max_length=100, help_text='Name of the client')
    description = models.CharField('description', max_length=200, help_text='Job title or the type of organisation')
    content = models.TextField('content', null=True, blank=True, help_text='Embedded content (video or audio) that best represent your work done for this client')
    background = models.ImageField(null=True, blank=True, upload_to=UPLOAD_FOLDER, help_text='Background image to display in the carousel')
    mugshot = models.ImageField(null=True, blank=True, upload_to=UPLOAD_FOLDER, help_text='Profile picture')
    showreel_url = models.URLField('showreel URL', blank=True, null=True, help_text='The embedded video URL that best represent the work you\'ve done for this client')
    link = models.URLField(null=True, blank=True, help_text='Link to this client\'s website.')

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return '{}'.format(self.name)

    def roles(self):
        return self.project_set.all().values_list('roles__name', flat=True).distinct()

    def products(self):
        return self.project_set.all().values_list('roles__product', flat=True).distinct()


class Role(models.Model):
    name = models.CharField('name', max_length=20)
    product = models.CharField('product', max_length=20)

    def __unicode__(self):
        return '{}'.format(self.name)


class Project(OrderedModel):
    client = models.ForeignKey('Client')
    name = models.CharField('name', max_length=100)
    roles = models.ManyToManyField('Role')
    category = models.CharField('category', max_length=30)
    date = models.CharField('date', max_length=20)
    url = models.URLField(blank=True, null=True, help_text='URL of the embedded video content')
    order_with_respect_to = 'client'

    def __unicode__(self):
        return '{}'.format(self.name)


class Testimonial(OrderedModel):
    author = models.ForeignKey('Client')
    title = models.CharField('title', max_length=200)
    body = models.TextField('body', blank=True)
    page = models.ForeignKey('Page', null=True)
    order_with_respect_to = 'page'

    def __unicode__(self):
        return '{} : {} "{}"'.format(self.author, self.title, self.body)