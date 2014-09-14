from django.forms import widgets 
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.forms.util import flatatt
import datetime
import settings

class LongTextInput(widgets.TextInput):
    def __init__(self, attrs=None):
        super(widgets.TextInput, self).__init__(attrs)
        self.attrs.update({'class': 'input-maxi'})

class MediumTextInput(widgets.TextInput):
    def __init__(self, attrs=None):
        super(widgets.TextInput, self).__init__(attrs)
        self.attrs.update({'class': 'input-medium'})

class MediumTextarea(widgets.Textarea):
    def __init__(self, attrs=None):
        super(widgets.Textarea, self).__init__(attrs)
        self.attrs.update({'class': 'input-medium', 'rows':10,})

class MaxiTextarea(widgets.Textarea):
    def __init__(self, attrs=None):
        super(widgets.Textarea, self).__init__(attrs)
        self.attrs.update({'class': 'input-maxi'})

class TextareaTiny(widgets.Textarea):
    def __init__(self, attrs=None):
        super(widgets.Textarea, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        value = force_unicode(value)
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))))

class CustomDatePicker(widgets.DateTimeInput):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """
    def __init__(self, attrs=None):
        super(widgets.DateTimeInput, self).__init__(attrs)
        self.attrs = self.attrs or {}
        if not self.attrs.get('id'):
            self.attrs.update({'id': 'datepicker'})

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        if not value:
            render = """
            <link rel="stylesheet" type="text/css" href="%(media_url)scss/cupertino/ui.all.css" />
            <div%(attrs)s></div><div id="dateselected_%(div_id)s"></div>
            <script type="text/javascript">
                $("#%(div_id)s").datepicker({
                    dateFormat: 'yy-mm-dd',
                    onSelect: function(date, instance) {
                        $("#dateselected_%(div_id)s").html("<input type='hidden' name='%(name)s' value='"+ date +" 12:00'/>");
                    }
                });
            </script>
            """ % {
                   'media_url': settings.MEDIA_URL,
                   'attrs': flatatt(final_attrs),
                   'div_id': final_attrs['id'],
                   'name': final_attrs['name'],
                  }
        else:
            if isinstance(value, unicode) or isinstance(value, str):
                if value.find(":") > 0:
                    value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")
                else:
                    value = datetime.datetime.strptime(value, "%Y-%m-%d")
            render = """
            <link rel="stylesheet" type="text/css" href="%(media_url)scss/cupertino/ui.all.css" />
            <div%(attrs)s></div><div id="dateselected_%(div_id)s"></div>
            <script type="text/javascript">
                $("#%(div_id)s").datepicker({
                    dateFormat: 'yy-mm-dd',
                    onSelect: function(date, instance) {
                        $("#dateselected_%(div_id)s").html("<input type='hidden' name='%(name)s' value='"+ date +" 12:00'/>");
                    }
                });
                $("#%(div_id)s").datepicker("setDate", new Date(%(year)d,%(monthzerobased)02d,%(day)02d));
                $("#dateselected_%(div_id)s").html("<input type='hidden' name='%(name)s' value='%(year)d-%(month)02d-%(day)02d 12:00'/>");
            </script>
            """ % {
                   'media_url': settings.MEDIA_URL,
                   'attrs': flatatt(final_attrs),
                   'div_id': final_attrs['id'],
                   'name': final_attrs['name'],
                   'year': value.year,
                   'monthzerobased': value.month-1,
                   'month': value.month,
                   'day': value.day,
                  }
        return render
