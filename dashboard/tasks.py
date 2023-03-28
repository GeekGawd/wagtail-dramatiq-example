import dramatiq, time
from .models import Job
from dashboard import debugger

@dramatiq.actor
def process_job(job_id):
    job = Job.objects.get(pk=job_id)
    job.process()

    job.status = Job.STATUS_DONE
    job.save()

@dramatiq.actor
def do_something():
    debugger.set_trace()
    time.sleep(5)
    print("Hello World")