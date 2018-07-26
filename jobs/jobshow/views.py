from django.shortcuts import render
from django.http import HttpResponse
from .models import Jobs
from django.core.paginator import Paginator
# Create your views here.
from django.db.models import Q

def index(request):
	return render(request,'index.html')

def showjobs(request):

	types = request.GET.get('type')
	keyword = request.GET.get('keyword')
	start = request.GET.get('start')
	end = request.GET.get('end')
	# print(start,end)
	if types and start and end:
		if types == 'gongzi':
			db = Jobs.objects.filter(Q(job_smoney__gte=int(start)),Q(job_smoney__lte=int(end))).order_by('job_smoney')
		elif types == 'jingyan':
			db = Jobs.objects.filter(Q(job_ssuffer__gte=int(start)),Q(job_ssuffer__lte=int(end))).order_by('job_ssuffer')
		else:
			db = Jobs.objects.all().order_by('crawltime')
	elif keyword:
		db = Jobs.objects.filter(job_name__contains=keyword)
	else:
		db = Jobs.objects.all().order_by('crawltime')

	paginator = Paginator(db,100)

	p = request.GET.get('p',1)

	db = paginator.page(p)

	context = {'ulist':db}
	return render(request,'showjobs.html',context)




def showjobs_liepin(request):
	types = request.GET.get('type')
	keyword = request.GET.get('keyword')

	start = request.GET.get('start')
	end = request.GET.get('end')
	# print(start,end)
	if types and start and end:
		if types == 'gongzi':
			db = Jobs.objects.filter(Q(job_smoney__gte=int(start)), Q(job_smoney__lte=int(end))).filter(spider='liepin').order_by('job_smoney')
		elif types == 'jingyan':
			db = Jobs.objects.filter(Q(job_ssuffer__gte=int(start)), Q(job_ssuffer__lte=int(end))).filter(spider='liepin').order_by('job_ssuffer')
		else:
			db = Jobs.objects.filter(spider='liepin').order_by('crawltime')
	elif keyword:
		db = Jobs.objects.filter(job_name__contains=keyword)
	else:
		db = Jobs.objects.filter(spider='liepin').order_by('crawltime')


	paginator = Paginator(db, 100)

	p = request.GET.get('p', 1)

	db = paginator.page(p)

	context = {'ulist': db}
	return render(request, 'showjobs.html', context)


def showjobs_qiancheng(request):
	types = request.GET.get('type')
	keyword = request.GET.get('keyword')

	start = request.GET.get('start')
	end = request.GET.get('end')
	# print(start,end)
	if types and start and end:
		if types == 'gongzi':
			db = Jobs.objects.filter(Q(job_smoney__gte=int(start)), Q(job_smoney__lte=int(end))).filter(spider='qiancheng').order_by('job_smoney')
		elif types == 'jingyan':
			db = Jobs.objects.filter(Q(job_ssuffer__gte=int(start)), Q(job_ssuffer__lte=int(end))).filter(spider='qiancheng').order_by('job_ssuffer')
		else:
			db = Jobs.objects.filter(spider='qiancheng').order_by('crawltime')
	elif keyword:
		db = Jobs.objects.filter(job_name__contains=keyword)
	else:
		db = Jobs.objects.filter(spider='qiancheng').order_by('crawltime')


	paginator = Paginator(db, 100)

	p = request.GET.get('p', 1)

	db = paginator.page(p)

	context = {'ulist': db}
	return render(request, 'showjobs.html', context)



def showjobs_zhilian(request):
	types = request.GET.get('type')
	keyword = request.GET.get('keyword')

	start = request.GET.get('start')
	end = request.GET.get('end')
	# print(start,end)
	if types and start and end:
		if types == 'gongzi':
			db = Jobs.objects.filter(Q(job_smoney__gte=int(start)), Q(job_smoney__lte=int(end))).filter(spider='zhilian').order_by('job_smoney')
		elif types == 'jingyan':
			db = Jobs.objects.filter(Q(job_ssuffer__gte=int(start)), Q(job_ssuffer__lte=int(end))).filter(spider='zhilian').order_by('job_ssuffer')
		else:
			db = Jobs.objects.filter(spider='zhilian').order_by('crawltime')
	elif keyword:
		db = Jobs.objects.filter(job_name__contains=keyword)
	else:
		db = Jobs.objects.filter(spider='zhilian').order_by('crawltime')


	paginator = Paginator(db, 100)

	p = request.GET.get('p', 1)

	db = paginator.page(p)

	context = {'ulist': db}
	return render(request, 'showjobs.html', context)
