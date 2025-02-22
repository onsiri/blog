from django.shortcuts import render, redirect
from .models import Post, Product, Transaction
from django.core.paginator import Paginator
from django.views.generic import ListView,DetailView, CreateView, TemplateView
import matplotlib.pyplot as plt
import pandas as pd
from django.http import HttpResponse
from django.db.models import Count
from io import BytesIO
import base64
from .form import ExcelUploadForm



class BlogListView(ListView):
    model = Post
    template_name = "home.html"

class BlogDetailView(DetailView):  # new
    model = Post
    template_name = "post_detail.html"

class BlogCreateView(CreateView):  # new
    model = Post
    template_name = "post_new.html"
    fields = ["title", "author", "body"]


class AboutPageView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):  # new
        context = super().get_context_data(**kwargs)
        context["contact_address"] = "123 Main Street"
        context["phone_number"] = "555-555-5555"
        return context

class ProductPageView(TemplateView):
    def get_product_view(request):
        items = Product.objects.all()
        return render(request, 'base.html', {'items': items})


def upload_file(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_csv(excel_file)

            for _, row in df.iterrows():
                Transaction.objects.create(
                    UserId=row['UserId'],
                    TransactionId=row['TransactionId'],
                    TransactionTime=row['TransactionTime'],
                    ItemCode=row['ItemCode'],
                    ItemDescription=row['ItemDescription'],
                    NumberOfItemsPurchased=row['NumberOfItemsPurchased'],
                    CostPerItem=row['CostPerItem'],
                    Country=row['Country']
                )
            return redirect('upload_file')  # Redirect to the same page or another page
    else:
        form = ExcelUploadForm()

    return render(request, 'upload.html', {'form': form})

def transaction_list(request):
    model = Post
    items = Transaction.objects.all()  # This should be a QuerySet
    paginator = Paginator(items, 20)  # Show 20 items per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'product_detail.html', {'page_obj': page_obj})


def dashboard(request):
    # Fetch data from the database
    transactions = Transaction.objects.values('ItemDescription').annotate(user_count=Count('UserId')).order_by(
        'ItemDescription')

    # Convert queryset to pandas DataFrame
    df = pd.DataFrame(list(transactions))

    # Create pie chart
    plt.figure(figsize=(10, 7))
    plt.pie(df['user_count'], labels=df['ItemDescription'], autopct='%1.1f%%')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save plot to a bytes buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode image to base64
    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Close the plot
    plt.close()

    # Pass the base64 string to the template
    context = {'chart': graphic}

    return render(request, 'dashboard.html', context)