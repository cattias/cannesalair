from django.forms.widgets import DateInput 
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.forms.util import flatatt

class DatePicker(DateInput):
    def __init__(self, attrs=None):
        super(DateInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        value = force_unicode(value)
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<input%s value="%s"/><div type="text" id="datepicker_%s"></div>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))), final_attrs['id'])
