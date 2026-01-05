from django.conf import settings
from tasks.views import *
from django.urls import path, include
from django.contrib.auth import views


urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('tasks/', Tasks.as_view(), name="tasks"),
    path('options/', Options.as_view(), name="options"),
    path('options/option-<int:opt_id>/', Catalog_option_tasks.as_view(), name='option'),
    path('tasks/task-<int:cat_id>/', Catalog_tasks.as_view(), name='category'),
    path('tasks/<slug:filter_slug>/', Catalog_tasks_filter.as_view(), name='filter_category'),
    path('themes/', Themes.as_view(), name="themes"),
    path('accounts/register/', RegisterUser.as_view(), name='register'),
    path('accounts/login/', LoginUser.as_view(), name='login'),
    path('accounts/logout/', logout_user, name='logout'),
    path('accounts/password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('task/<int:task_id>/', Task_Object.as_view(), name='task_object'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
