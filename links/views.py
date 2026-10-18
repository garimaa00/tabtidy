from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SavedLinkForm
from .models import SavedLink


def register(request):
    if request.user.is_authenticated:
        return redirect('link_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your TabTidy account is ready!')
            return redirect('link_list')
    else:
        form = UserCreationForm()

    return render(request, 'links/register.html', {'form': form})

@login_required
def link_list(request):
    all_links = SavedLink.objects.filter(owner=request.user)
    links = all_links

    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')

    if query:
        links = links.filter(
            Q(title__icontains=query)
            | Q(url__icontains=query)
            | Q(note__icontains=query)
        )

    if category:
        links = links.filter(category=category)

    if status == 'visited':
        links = links.filter(is_visited=True)
    elif status == 'pending':
        links = links.filter(is_visited=False)


    total_links = all_links.count()
    visited_links = all_links.filter(is_visited=True).count()
    pending_links = total_links - visited_links

    progress_percent = (
        round((visited_links / total_links) * 100)
        if total_links > 0 else 0
    )

    context = {
        'links': links,
        'query': query,
        'selected_category': category,
        'selected_status': status,
        'categories': SavedLink.CATEGORY_CHOICES,
        'total_links': total_links,
        'visited_links': visited_links,
        'pending_links': pending_links,
        'progress_percent': progress_percent,
    }

    return render(request, 'links/link_list.html', context)

@login_required
def link_create(request):
    if request.method == 'POST':
        form = SavedLinkForm(request.POST)

        if form.is_valid():
            link= form.save(commit=False)
            link.owner = request.user
            link.save()
            messages.success(request, 'Link saved successfully!')
            return redirect('link_list')
    else:
        form = SavedLinkForm()

    return render(request, 'links/link_form.html', {
        'form': form,
        'page_title': 'Save a new link',
    })

@login_required
def link_update(request, pk):
    link = get_object_or_404(SavedLink, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = SavedLinkForm(request.POST, instance=link)

        if form.is_valid():
            form.save()
            messages.success(request, 'Link updated successfully!')
            return redirect('link_list')
    else:
        form = SavedLinkForm(instance=link)

    return render(request, 'links/link_form.html', {
        'form': form,
        'page_title': 'Edit saved link',
    })

@login_required
def link_toggle_visited(request, pk):
    link = get_object_or_404(SavedLink, pk=pk, owner=request.user)

    if request.method == 'POST':
        link.is_visited = not link.is_visited
        link.save(update_fields=['is_visited'])
        messages.success(request, 'Link status updated!')

    return redirect('link_list')


@login_required
def link_delete(request, pk):
    link = get_object_or_404(SavedLink, pk=pk, owner=request.user)

    if request.method == 'POST':
        link.delete()
        messages.success(request, 'Link deleted successfully!')
        return redirect('link_list')

    return render(request, 'links/link_confirm_delete.html', {
        'link': link,
    })

