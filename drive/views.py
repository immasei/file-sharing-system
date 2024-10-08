from django.http import HttpResponse, JsonResponse
from django.template import loader
import uuid, json
from django.views.decorators.csrf import csrf_exempt

from drive.upload import get_presigned_urls, save_etags
from .models import File

def drive(request):
    template = loader.get_template('index.html')
    context = {
    'ff': File.objects.all().values(),
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def create_upload(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            file_name = payload['file_name']
            content_type = payload['content_type']
            file_size = payload['file_size']

            key = f"{uuid.uuid4()}/{file_name}"

            response = get_presigned_urls(
                key,
                content_type,
                file_size,
            )
      
            return JsonResponse(response, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=404)

    return JsonResponse({'error': ':)'}, status=404)

@csrf_exempt
def complete_upload(request):
	print(12487842)
	if request.method == 'POST':
		try:
			payload = json.loads(request.body)
			print(payload)
			response = save_etags(payload['key'], payload['upload_id'], payload['etags'])
			print(response)
			return JsonResponse(response, status=200)
		except Exception as e:
			return JsonResponse({'error': str(e)}, status=404)

	return JsonResponse({'error': ':)'}, status=404)
