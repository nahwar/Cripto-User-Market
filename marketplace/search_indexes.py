import datetime
from haystack import indexes
from .models import Articulo, Categoria

class ArticulosIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    owner = indexes.CharField(model_attr='owner')
    nombre = indexes.CharField(model_attr='nombre')
    imagen = indexes.CharField(model_attr='imagen')
    precio = indexes.CharField(model_attr='precio')
    categoria = indexes.CharField(model_attr='categoria')
    #pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Articulo

    #def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        #return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())