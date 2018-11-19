from django.contrib import admin
from django.urls import path
from Record import views
app_name = 'Record'
urlpatterns = [
    path('', views.index,name='index'),
    path('login/',views.login,name='login'),
    path('record/',views.record,name='record'),
    path('register/', views.register,name='register'),
    path('logout/', views.logout,name='logout'),
    path('createhome/',views.createhome,name='createhome'),
    path('homelist/<int:id>/', views.Homeinfo, name='Homeinfo'),
    path('myhome/',views.MyHome,name='myhome'),
    path('myexpense/<int:exp_id>/',views.ChangeExpense,name='changeexpense'),
    path('myexpense_list/',views.MyExpense,name='myexpense'),
    path('DeleteExpense/<int:del_id>/',views.DeleteExpense,name='delete')
]
