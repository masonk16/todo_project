from django.db import models
from django.contrib.auth.models import User

STATUS = (
    (0,"Not Done"),
    (1,"Done")
)

class TodoItem(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,
                               related_name='todo_items')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    todo = models.ForeignKey(TodoItem, on_delete=models.CASCADE, 
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        
    def __str__(self):
        return f"Comment by {self.name} on {self.todo}"
