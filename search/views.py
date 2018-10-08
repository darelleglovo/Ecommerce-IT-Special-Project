from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product, Category, Subcategory

# Create your views here.

class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Product.objects.filter(title__icontains=query, active=True)
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super(SearchProductView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        context['prod_count'] = Product.objects.all().count()
        return context