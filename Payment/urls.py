from django.contrib import admin
from django.urls import path
from Payment import views
app_name = 'Payment'
urlpatterns = [
    path('', views.index,name='index'),
    path('index/', views.index),
    path('page<int:page>/', views.index),
    path('help/',views.help,name='help'),
    path('search/', views.search, name='search'),
    path('accounts/',views.Show_accounts,name='accounts'),
    path('login/',views.login,name='login'),
    path('record/',views.record,name='record'),
    path('register/', views.register,name='register'),
    path('logout/', views.logout,name='logout'),
    path('myexpense/<int:exp_id>/',views.ChangeExpense,name='changeexpense'),
    path('expenses/<int:exp_id>/',views.Show_info,name='expenses_info'),
    path('myexpense_list/',views.MyExpense,name='myexpense'),
    path('DeleteExpense/<int:del_id>/',views.DeleteExpense,name='delete')
]
