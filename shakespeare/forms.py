from formalchemy import forms
from formalchemy import tables
import formalchemy.fields

from shakespeare import model
from shakespeare.model.base import JsonType

forms.FieldSet.default_renderers[JsonType] = formalchemy.fields.TextFieldRenderer

Work = forms.FieldSet(model.Work)
Work.configure(options=[
    Work.notes.textarea(size=(40,25))
    ])
# Material = forms.FieldSet(model.Material)
# Statistic = forms.FieldSet(model.Statistic)

