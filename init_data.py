import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teonitetest.settings")
django.setup()

from stats.models import Author, Post, Occurence, Word, Reaper

url='http://teonite.com'


def mainloop(url):

    soup = Reaper(url+'/blog/')

    next_url = soup.get_first()
    while next_url:
        print('url: '+next_url)
        soup = Reaper(url+next_url)
        name = soup.get_author()

        try:
            autorPost = Author.objects.get(name=name)
        except:
            autorPost = Author()
            autorPost.name = name
            autorPost.save()

        content = soup.get_content()


        try:
            post = Post.objects.get(url=next_url)
            post.update(content)
        except:
            post = Post()
            post.url = next_url
            post.author = autorPost
            post.content = content
            post.save()

        next_url = soup.get_next()


def check_words():
    print('start analyse')
    posts = Post.objects.filter(change=True)
    for post in posts:
        occurences = Occurence.objects.filter(post=post).delete()

        words = post.get_words()

        #dodac wyrazy
        for item in words:
            if len(item) <= 255:
                item = item.lower()

                try:
                    word = Word.objects.get(word=item)
                except:
                    word = Word()
                    word.word = item
                    word.save()

                try:
                    occurence = Occurence.objects.get(word=word, post=post)
                except:
                    occurence = Occurence()
                    occurence.post = post
                    occurence.word = word

                occurence.up()

        post.tested()
    print('end analyse')

mainloop(url)
check_words()
