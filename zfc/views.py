from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your views here.
import os
import time
from .models import Job
from . import zfc_script
import multiprocessing as mp
import subprocess as sp

# Job control

job_queue = mp.Queue()


def job_work_func(queue):
    while True:
        thejob = queue.get(True)
        job_dir = thejob.job_dir()
        thejob.analysis_status = 'R'
        thejob.save()
        result = sp.run(['bash', 'run_zfc.sh'], cwd=job_dir, stderr=sp.PIPE)
        if result.returncode == 0:
            thejob.analysis_status = 'F'
            thejob.stderr = ''
            thejob.save()
        else:
            thejob.analysis_status = 'E'
            thejob.stderr = result.stderr.decode('utf-8')
            thejob.save()


job_work_pool = mp.Pool(2, job_work_func, (job_queue,))

# View Functions


def home(request):
    return render(request, 'zfc/home.html')


def job(request, job_id):
    # For Post method
    if request.method == 'POST':
        if Job.objects.filter(pk=job_id).exists():
            job_id = job_id + time.strftime("%H%M%S")
        # Make new object
        thejob = Job(
            job_id=job_id,
            analysis_status='P',
            reserve_status='K',
            dir_path=job_id
        )
        thejob.save()
        # Make job dir
        try:
            os.mkdir(thejob.job_dir())
        except FileExistsError:
            pass
        jobfs = FileSystemStorage(location=thejob.job_dir())
        jobfs.save(thejob.file_raw_count, request.FILES['count_file'])
        # Prepare job
        job_args = dict()
        if request.POST['top_n_sgrna'] == '':
            job_args['top_n_sgrna'] = None
        else:
            job_args['top_n_sgrna'] = request.POST['top_n_sgrna']
        if request.POST['top_n_gene'] == '':
            job_args['top_n_gene'] = None
        else:
            job_args['top_n_gene'] = request.POST['top_n_gene']
        jobfs.save(
            'run_zfc.sh',
            zfc_script.make_job_script(
                top_n_sgrna=job_args['top_n_sgrna'],
                top_n_gene=job_args['top_n_gene']
            )
        )

        # Run job
        job_queue.put(thejob)

    # For Get method
    elif request.method == 'GET':
        try:
            thejob = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            raise Http404('Job does not exist.')

    if thejob.analysis_status == 'F':
        return render(
            request, 'zfc/result.html',
            {
                'job_id': thejob.job_id,
                'result_url': '{0}://{1}{2}'.format(
                    request.scheme,
                    request.get_host(),
                    request.get_full_path()
                ),
                'job_status': {
                    'P': 'Pending',
                    'R': 'Running',
                    'F': 'Finished',
                    'E': 'Error',
                }[thejob.analysis_status],
                'file_status': {
                    'K': 'Keeping',
                    'A': 'Archived',
                    'D': 'Deleted',
                }[thejob.reserve_status],
                'image_counts_boxplot': os.path.join(
                    settings.MEDIA_URL,
                    thejob.dir_path,
                    'zfc_counts_boxplot.png'
                ),
                'image_lfc_normcount_scatter': os.path.join(
                    settings.MEDIA_URL,
                    thejob.dir_path,
                    'zfc_lfc_normcount_scatter.png'
                ),
                'image_zlfc_normcount_scatter': os.path.join(
                    settings.MEDIA_URL,
                    thejob.dir_path,
                    'zfc_zlfc_normcount_scatter.png'
                ),
                'image_sgrna_zlfc_rra_scatter': os.path.join(
                    settings.MEDIA_URL,
                    thejob.dir_path,
                    'zfc_sgrna_zlfc_rra_scatter.png'
                ),
                'image_gene_zlfc_rra_scatter': os.path.join(
                    settings.MEDIA_URL,
                    thejob.dir_path,
                    'zfc_gene_zlfc_rra_scatter.png'
                ),
            }
        )
    else:
        return render(
            request, 'zfc/submitted.html',
            {
                'job_id': thejob.job_id,
                'result_url': '{0}://{1}{2}'.format(
                    request.scheme,
                    request.get_host(),
                    request.get_full_path()
                ),
                'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'job_status': {
                    'P': 'Pending',
                    'R': 'Running',
                    'F': 'Finished',
                    'E': 'Error',
                }[thejob.analysis_status],
                'file_status': {
                    'K': 'Keeping',
                    'A': 'Archived',
                    'D': 'Deleted',
                }[thejob.reserve_status],
                'error_message': thejob.stderr
            }
        )


def download(request, job_id):
    try:
        thejob = Job.objects.get(pk=job_id)
        file_path = os.path.join(
            settings.MEDIA_ROOT, thejob.dir_path, thejob.file_out_zip
        )
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = ''.join(
                ['inline; filename=', os.path.basename(file_path)]
            )
            return response
    except Job.DoesNotExist:
        raise Http404('File does not exist.')


def document(request):
    return render(request, 'zfc/document.html')


def about(request):
    return render(request, 'zfc/about.html')
