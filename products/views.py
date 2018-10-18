from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.apps import apps
from django.shortcuts import render, redirect

from datetime import datetime, timedelta
from .render import Render # changes

from django.contrib import messages


Cart = apps.get_model('carts', 'Cart')

from .models import Product, Category, Subcategory
from orders.models import Order

class ProductFeaturedListView(ListView):
    template_name = "products/list.html"
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductFeaturedDetailView(DetailView):
    template_name = "products/featured-detail.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductListView(ListView):
    #queryset = Product.objects.all()
    template_name = "products/list.html"
    queryset = Product.objects.all()
    # def get_context_data(self, *args, **kwargs):
    #     #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     #     print(context)
    #     #     return context
    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Product.objects.all()
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        context['prod_count'] = Product.objects.all().count()
        return context

def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
            context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
            try:
                cart = Cart.objects.get(id=self.request.session.get("cart_id"))
                items = cart.items.filter(cart=self.request.session.get("cart_id"))
                # items = CartItem.objects.filter(cart=self.request.session.get("cart_id"))
                context['items'] = items

                print(context)
                print("a")
            except:
                pass
            return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhhmm")
        return instance

class ProductDetailView(DetailView):
    #queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
            context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
            print(context)
            return context
    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        print(instance)
        return instance

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)


def product_detail_view(request, pk=None, *args, **kwargs):
    #instance = Product.objects.get(pk=pk)
    #instance = get_object_or_404(Product, pk=pk)
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")
    print(instance)
    # qs = Product.objects.filter(id=pk)
    #
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404("Product doesn't exist")
    context = {
        'object': instance
    }
    #print(context)
    return render(request, "products/detail.html", context)

def list_products_by_category(request, category_slug):
    categories = Category.objects.all()
    products = Product.objects.all()
    subcategories = Subcategory.objects.all()
    prod_count = Product.objects.all().count()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    template = "products/list_by_category.html"
    context = {'categories': categories,
               'products': products,
               'subcategories':subcategories,
               'prod_count': prod_count,
               }
    return render(request, template, context)

def list_products_by_subcategory(request, subcategory_slug):
    categories = Category.objects.all()
    products = Product.objects.all()
    subcategories = Subcategory.objects.all()
    prod_count = Product.objects.all().count()
    if subcategory_slug:
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
        products = products.filter(subcategory=subcategory)
    template = "products/list_by_subcategory.html"
    context = {'categories': categories,
               'products': products,
               'subcategories':subcategories,
               'prod_count': prod_count,
               }
    return render(request, template, context)

def reports_result(request):
    if request.user.is_superuser or request.user.is_staff:
        try:

            download_product_masterlist = request.GET.get('download_product_masterlist')

            if download_product_masterlist:
                master_list = Product.objects.all()
                context = {
                    'master_list': master_list,
                }
                return Render.render('products/products_pdf.html', context)

            date_from = request.GET.get('date_from')
            date_to = request.GET.get('date_to')
            report_type = request.GET.get('report_type')

            print(report_type)

            date_to = date_to.replace("-", " ")

            date_to_formatted = datetime.strptime(date_to, '%Y %m %d')

            date_to_final = date_to_formatted + timedelta(days=1)
            try:
                if report_type == 'unpaid_orders':
                    filtered_objects = Order.objects.filter(timestamp__range=[date_from, date_to_final], status='waiting_for_payment')
                elif report_type == 'shipped_items':
                    filtered_objects = Order.objects.filter(timestamp__range=[date_from, date_to_final], shipping_status='shipped')
                elif report_type == 'not_yet_shipped':
                    filtered_objects = Order.objects.filter(timestamp__range=[date_from, date_to_final], shipping_status='not_shipped')
                elif report_type == 'paid_orders':
                    filtered_objects = Order.objects.filter(timestamp__range=[date_from, date_to_final], status='paid')
                elif report_type == 'canceled_orders':
                    filtered_objects = Order.objects.filter(timestamp__range=[date_from, date_to_final], status='canceled')
                elif report_type == 'all_transactions':
                    filtered_objects = Order.objects.all()
                date_to = date_to.replace(" ", "-")
                context = {
                    'filtered_objects': filtered_objects,
                    'report_type': report_type,
                    'date_from': date_from,
                    'date_to': date_to
                }

                download_report = request.GET.get('download_report')

                if download_report:
                    return Render.render('products/pdf.html', context)
                else:
                    pass
            except:
                context = {
                    'report_type': 'No reports found'
                }

            return render(request, "products/report_result.html", context)
        except Exception as e:
            messages.error(request, 'Please select proper date')
            return redirect('products:reports_page')
    else:
        raise Http404

def reports_page(request):
    if request.user.is_superuser or request.user.is_staff:
        critical_level = Product.objects.filter(inventory__lte=10)
        context = {
            'critical_level': critical_level
        }
        return render(request, "products/reports.html", context)
    else:
        raise Http404