import redis
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from actions.utils import create_action
from common.decorators import ajax_required

from .forms import ImageCreateForm
from .models import Image

r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()

            create_action(request.user, "posted image", new_image)
            messages.success(request, "Image added successfully")
            return redirect(new_image)
    else:
        form = ImageCreateForm()

    ctx = dict(section="images", form=form)
    return render(request, "images/image/create.html", ctx)


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = r.incr(f"image:{image.id}:views")
    r.zincrby("image_ranking", 1, image.id)

    ctx = dict(section="images", image=image, total_views=total_views)
    return render(request, "images/image/detail.html", ctx)


def image_ranking(request):
    ranking = r.zrange("image_ranking", 0, -1, desc=True)[:10]
    ranking_ids = [int(id) for id in ranking]
    most_viewed = list(Image.objects.filter(id__in=ranking_ids))
    most_viewed.sort(key=lambda img: ranking_ids.index(img.id))

    ctx = dict(section="images", most_viewed=most_viewed)
    return render(request, "images/image/ranking.html", ctx)


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 5)
    page = request.GET.get("page")
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        return HttpResponse()

    ctx = dict(section="images", images=images)
    if request.is_ajax():
        return render(request, "images/image/list_ajax.html", ctx)
    return render(request, "images/image/list.html", ctx)
