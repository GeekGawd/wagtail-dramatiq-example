from django.shortcuts import redirect, render

from .models import Job
from .tasks import process_job, do_something
from django.http import JsonResponse
from dramatiq.actor import Actor
from dramatiq.broker import get_broker
from .wagtailbg import background
from django_dramatiq.models import Task

def index(request):
    broker = get_broker()
    do_something.send()
    return JsonResponse(data={"status": "Enqueued Message"})
