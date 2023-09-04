from django.forms.widgets import Input


class ColorInput(Input):
    input_type = "color"
    template_name = "honauth/widgets/colorpicker.html"
