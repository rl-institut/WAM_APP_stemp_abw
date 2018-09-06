from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'stemp_abw/index.html'


def map(request):
    #question = get_object_or_404(Question, pk=question_id)
    return render(request, 'stemp_abw/map.html')
