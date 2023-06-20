from django.shortcuts import render, get_object_or_404, redirect
from .models import TodoItem

from django.urls import reverse

from .forms import CommentForm


def todo_list(request):
    todo_items = TodoItem.objects.all().order_by('-created_on')
    return render(request, 'index.html', {"todo_items": todo_items})
    
def todo_detail(request, slug, id):
    todo_item = get_object_or_404(TodoItem, id=id, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.todo = todo_item
            comment.save()

    form = CommentForm()

    comments = todo_item.comments.filter(active=True)

    context = {
        "todo_item": todo_item,
        'form': form,
        'comments': comments
    }

    return render(request, 'todo_detail.html', context)

    #return redirect(reverse('todo_detail', args=[slug, id]), context)

    #return redirect('todo_list')

