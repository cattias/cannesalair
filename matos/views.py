from django.shortcuts import render_to_response
from account.decorators import login_required
from matos.datagrids import MatosDataGrid
from matos.models import Matos
from django.template.context import RequestContext

@login_required
def list_matos(request, template_name='matos/matos_list.html'):
    grid = MatosDataGrid(request)
    return grid.render_to_response(template_name)

@login_required
def view_matos(request, matos_pk, template_name='matos/matos_view.html'):
    m = Matos.objects.get(pk=matos_pk)
    return render_to_response(template_name, RequestContext(request, {'matos': m,}))
    