from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.ItemListView.as_view(), name='items'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('department/<int:pk>', views.DepartmentDetailView.as_view(), name='department-items'),
    path('myitems/', views.LoanedItemsByUserListView.as_view(), name='my-borrowed-items'),
    path('checkedoutitems/', views.CheckedOutItemsListView.as_view(), name='all-checked-out-items'),
    path('item/create/', views.ItemCreate.as_view(), name='item-create'),
    path('item/<int:pk>/renew/', views.renew_item_librarian, name='renew-item-librarian'),
    path('item/<int:pk>/transaction/', views.TransactionEntry.as_view(), name='librarian-transaction'),
]