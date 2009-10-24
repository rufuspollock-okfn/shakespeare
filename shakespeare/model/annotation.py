import meta

import annotator.model
from annotator.model import Annotation
annotation_table = annotator.model.make_annotation_table(meta.metadata)

annotator.model.map_annotation_object(meta.Session.mapper, annotation_table)

