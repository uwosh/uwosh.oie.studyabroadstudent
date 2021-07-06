from plone.app.z3cform.widget import DateWidget


class SundayStartDateWidget(DateWidget):

    def _base_args(self):
        args = super()._base_args()
        args['pattern_options']['firstDay'] = 0
        return args
