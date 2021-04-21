from django.contrib import admin
from .models import PostLike, Post


class PostLikeAdmin(admin.TabularInline):
    model = PostLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Class for registering posts in the admin panel"""
    inlines = (PostLikeAdmin,)
    list_display = ('__str__', 'author')
    search_fields = ('__str__', 'author__username',)
    list_display_links = ('__str__', 'author')


admin.site.register(PostLike)
