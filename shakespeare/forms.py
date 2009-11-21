from formalchemy import forms
from formalchemy import tables

from shakespeare import model

Work = forms.FieldSet(model.Work)
Work.configure(options=[
    Work.notes.textarea(size=(40,25))
    ])
# Material = forms.FieldSet(model.Material)
# Statistic = forms.FieldSet(model.Statistic)

