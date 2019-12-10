from django.db import models
from django.conf import settings
# Create your models here.
import os


class Job(models.Model):
    ANALYSIS_STATUS = [
        ('P', 'Pending'),
        ('R', 'Running'),
        ('F', 'Finished'),
        ('E', 'Error'),
    ]
    RESERVE_STATUS = [
        ('K', 'Keeping'),
        ('A', 'Archived'),
        ('D', 'Deleted'),
    ]
    job_id = models.CharField(max_length=200, primary_key=True)
    submit_date = models.DateTimeField(auto_now_add=True)
    analysis_status = models.CharField(max_length=1, choices=ANALYSIS_STATUS)
    reserve_status = models.CharField(max_length=1, choices=RESERVE_STATUS)
    dir_path = models.CharField(max_length=1000)
    file_raw_count = models.CharField(default='zfc_raw_count.txt', max_length=1000)
    file_sh = models.CharField(default='run_zfc.sh', max_length=1000)
    file_out_zip = models.CharField(default='zfc_out.zip', max_length=1000)
    stderr = models.TextField(max_length=10000)

    def job_dir(self):
        return os.path.join(settings.MEDIA_ROOT, self.dir_path)

    def __str__(self):
        return self.job_id
