# -*- coding: utf-8 -*-
import re
import string
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, api_view



from django.db.models import Count, Min, Sum, Avg, F
from .models import Author, Post, Occurence, Word, Reaper


def search(request):
    #startTime = datetime.now()
    #mainloop(url)
    #check_words()
    #endTime =datetime.now() - startTime
    return HttpResponse('World statistics')#"Data acquisition: '"+url+"'. Time: "+ str(endTime))

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def word(request,author_slug=''):
    if author_slug:
        words = Post.objects.filter(author__slug=author_slug).values(word=F('words__word')).annotate(sum=Sum('occurence__number')).order_by('-sum')[:10]
    else:
        words = Word.objects.values('word').annotate(sum=Sum('occurence__number')).order_by('-sum')[:10]

    output = {item['word']: item['sum'] for item in words}
    return Response(output)




