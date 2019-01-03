# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from bs4 import BeautifulSoup
import requests
import re
import string
import binascii
import unidecode


class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nazwa')
    slug = models.CharField(max_length=200, verbose_name='Nazwa uproszcozna', unique=True)

    def save(self, *args, **kwargs):
        self.slug = unidecode.unidecode(self.name).lower().replace(' ', '')

        super(Author, self).save(*args, **kwargs)

class Post(models.Model):
    url = models.TextField(verbose_name='url', unique=True)
    content =  models.TextField(verbose_name='Zawartość artykułu')
    author = models.ForeignKey(Author, verbose_name='Autor')
    crc = models.CharField(max_length=10)
    change = models.BooleanField(default=True, verbose_name='Zmiana')
    words = models.ManyToManyField('Word', through='Occurence')

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        crc = str(binascii.crc32(self.content.encode('utf-8')))
        self.crc = crc
        self.change = 1
        super(Post, self).save(*args, **kwargs)


    def update(self,content):
        crc = str(binascii.crc32(content.encode('utf-8')))
        if crc != self.crc:
            self.crc = crc
            self.content = content
            self.change = 1
            super(Post, self).save()

    def get_words(self):
        content = self.content
        content = re.sub('\s\s+', ' ', content)
        translator = str.maketrans('', '', '!"#$%&()*+,-.:;<=>?@[\]^_`{|}~')  # '.,?":;=>{|}()-!~\%\+\\')
        content = content.translate(translator)
        return content.split()

    def tested(self):
        self.change = 0
        super(Post, self).save()

class Word(models.Model):
    word = models.CharField(max_length=255, verbose_name='Nazwa')

class Occurence(models.Model):
    post = models.ForeignKey('Post')
    word = models.ForeignKey('Word')
    number = models.IntegerField(default=0)

    class Meta:
        ordering = ('number',)

    def up(self):
        self.number += 1
        super(Occurence, self).save()



class Reaper(BeautifulSoup):

    def __init__(self, url):
        result = requests.get(url)
        BeautifulSoup.__init__(self, result.content, 'html.parser')


    def get_first(self):
        title = self.find("h2", {'class': 'post-title'})
        return title.a.get('href')

    def get_next(self):
        next = self.find('li', {'class': 'pull-left'}).find('a')
        if next:
            return next.get('href')
        else:
            return False

    def get_author(self):
        return self.find('span', {'class': 'author-content'}).find('h4').text


    def get_content(self):
        title = self.find('h1', {'class':"post-title"})

        content = title.get_text()
        text = self.find('section', {'class': "post-content"})
        content = content + ' ' + text.get_text()
        content = re.sub('\s\s+', ' ', content)
        return content