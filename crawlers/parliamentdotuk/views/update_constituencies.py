from django.http import HttpResponse
from django.views import View

from crawlers.parliamentdotuk.tasks.lda.update_constituencies import update_constituencies
from repository.models import Constituency


VIEW_UPDATE_CONSTITUENCIES = 'update_constituencies_view'


class UpdateConstituenciesView(View):
    def get(self, request):
        if request.user.is_superuser and request.GET.get('update'):
            update_constituencies()

        constituencies = Constituency.objects.all()
        html = f'<div>{len(constituencies)} constituencies:</div>'
        html += '<br/>'.join([x.name for x in constituencies])
        return HttpResponse(html)
