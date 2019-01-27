import datetime
from haystack import indexes
from Payment.models import Expense


class PaymentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='pay_user')
    pub_date = indexes.DateTimeField(model_attr='date_time')

    def get_model(self):
        return Expense

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()