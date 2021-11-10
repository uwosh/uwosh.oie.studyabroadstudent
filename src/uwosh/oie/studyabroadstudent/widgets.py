from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from zope.schema.interfaces import IField
from zope.interface import implementer
from zope.component import adapter
from z3c.form.converter import IntegerDataConverter
from z3c.form.interfaces import ITextWidget
from zope.schema.interfaces import IInt
from zope.component import adapts
from zope.component import provideAdapter
from plone.app.z3cform.widget import DateWidget
from z3c.form.widget import FieldWidget



class SundayStartDateWidget(DateWidget):

    def _base_args(self):
        args = super()._base_args()
        args['pattern_options']['firstDay'] = 0
        return args


class IIntNoFormatWidget(ITextWidget):
    pass


@implementer(IIntNoFormatWidget)
class IntNoFormatWidget(TextWidget):
    id = u'int-no-format-widget'


@adapter(IField, IFormLayer)
@implementer(IFieldWidget)
def IntNoFormatFieldWidget(field, request):
    return FieldWidget(field, IntNoFormatWidget(request))


class NoFormatIntegerDataConverter(IntegerDataConverter):

    # adapts the Widget Definition above
    adapts(IInt, IIntNoFormatWidget)

    def toWidgetValue(self, value):
        return '' if value is self.field.missing_value else str(value)


provideAdapter(NoFormatIntegerDataConverter)
