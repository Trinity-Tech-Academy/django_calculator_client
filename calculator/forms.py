from django import forms 


class ComputeForm(forms.Form):
    operation = forms.ChoiceField(
        choices=[],                 # populated dynamically from the API 
        label = 'Operation',
    )
    a = forms.FloatField(label='First Operand (a)')
    b = forms.FloatField(
        label='second operand (b)',
        required=False,
        initial=0.0,
        help_text='Leave blank or set to 0 for single-operand operations like sqrt.',
    )
    
    def __init__(self, *args, operations=None, **kwargs):
        super().__init__(*args, **kwargs)
        if operations:
            self.fields['operation'].choices = [
                (op, op) for op in operations
            ]