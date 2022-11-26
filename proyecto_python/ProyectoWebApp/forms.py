from django import forms

class TareaJsonForm(forms.Form):
    file = forms.FileField()

    def __init__(self,*args,**kwargs):
        super(TareaJsonForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-sm'
            visible.field.widget.attrs['accept'] = '.json, .txt'