# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from djblets.datagrid.grids import Column, DataGrid
from matos.models import Matos

class MatosTitreColumn(Column):
    """
    Titre du matos
    """
    def __init__(self, label="Titre",
                 detailed_label="Titre",
                 *args, **kwargs):
        Column.__init__(self, label=label, detailed_label=detailed_label,
                        *kwargs, **kwargs)
        self.sortable = True
        self.shrink = True
        self.link = True
        self.link_func = self.link_to_object
        self.css_class = "linkedcolumn"

    def render_data(self, matos):
        return "%s" % matos.titre

    def link_to_object(self, matos, value):
        return reverse("viewmatos", kwargs={"matos_pk":matos.pk})

class MatosCategorieColumn(Column):
    """
    Categorie du matos
    """
    def __init__(self, label="Type",
                 detailed_label="Type",
                 *args, **kwargs):
        Column.__init__(self, label=label, detailed_label=detailed_label,
                        *kwargs, **kwargs)
        self.sortable = True
        self.shrink = True

    def render_data(self, matos):
        return "%s" % matos.categorie

class MatosPrixColumn(Column):
    """
    Prix du matos
    """
    def __init__(self, label="Prix",
                 detailed_label="Prix",
                 *args, **kwargs):
        Column.__init__(self, label=label, detailed_label=detailed_label,
                        *kwargs, **kwargs)
        self.sortable = True
        self.shrink = True

    def render_data(self, matos):
        return "%s &euro;" % matos.prix_neuf

class MatosDateAchatColumn(Column):
    """
    Prix du matos
    """
    def __init__(self, label="Date d'achat",
                 detailed_label="Date d'achat",
                 *args, **kwargs):
        Column.__init__(self, label=label, detailed_label=detailed_label,
                        *kwargs, **kwargs)
        self.sortable = True
        self.shrink = True

    def render_data(self, matos):
        return "%s" % matos.date_achat

class MatosDataGrid(DataGrid):
    """
    A datagrid that displays a list of matos.
    """
    titre = MatosTitreColumn()
    prix = MatosPrixColumn()
    categorie = MatosCategorieColumn()
    date_achat = MatosDateAchatColumn()

    def __init__(self, request,
                 queryset=Matos.objects.all(),
                 title="Tout le matos"):
        DataGrid.__init__(self, request, queryset, title)
        self.show_disabled = False
        self.default_sort = ["titre"]
        self.default_columns = ["titre", "prix", "date_achat", "categorie"]
