import os
import subprocess
from django.http import HttpResponse
from django.template import loader
from django.views.generic import FormView
from .forms import IndexForm

class IndexView(FormView):
    template_name = 'kpcweb/index.html'
    success_url = '/'
    form_class = IndexForm

    def __init__(self, *args, **kwargs):
        self.result = None
        return super(IndexView, self).__init__()

    def form_valid(self, form):
        context = self.get_context_data()
        context['result'] = result = {}
        f = form.cleaned_data['file']
        fname = f.name
        print(fname)
        result['po'] = pocontent = f.read().decode('UTF-8')

        # run ko-po-check
        os.system('rm -rf data')
        os.mkdir('data')

        open('data/' + fname, 'w').write(pocontent)
        cmd = ('env PYTHONPATH=external/ko-po-check python3 ' +
            'external/ko-po-check/scripts/ko-po-check ' +
            'data/' + fname)

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        errors = p.stdout.read().decode('UTF-8')
        exitcode = p.wait()
        os.remove('data/' + fname)
        os.rmdir('data')

        if exitcode == 0:
            resultstr = '성공'
        else:
            resultstr = '실패'

        result['result'] = resultstr
        result['errors'] = errors
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if self.result is not None:
            kwargs['result'] = self.result
        return super(IndexView, self).get_context_data(**kwargs)
