from django.db import models

#用户信息模型
class Users(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=50)

   # class Meta:
   #    db_table = "polls_users"  # 指定表名

class Jobs(models.Model):
    job_url = models.CharField(max_length=255)
    job_name = models.CharField(max_length=255)
    job_location = models.CharField(max_length=255)
    job_smoney = models.IntegerField()
    job_emoney = models.IntegerField()
    job_cname = models.CharField(max_length=255)
    job_ssuffer = models.IntegerField()
    job_esuffer = models.IntegerField()
    job_educa = models.CharField(max_length=255)
    job_putime = models.CharField(max_length=255)
    job_tags = models.CharField(max_length=255)
    job_info = models.TextField()
    job_type = models.CharField(max_length=255)
    job_address = models.CharField(max_length=255)
    spider = models.CharField(max_length=255)
    crawltime = models.DateField()

    class Meta:
        db_table = "jobs"  # 指定表名
