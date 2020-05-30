from haystack import indexes
from .models import Book


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', boost=1.5)
    tags = indexes.CharField(model_attr='tags', boost=1.25)

    def get_model(self):
        return Book