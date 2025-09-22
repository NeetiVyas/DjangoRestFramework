from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .authtokens import CustomAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = DefaultRouter()
router.register('employees', views.EmployeeViewset, basename='employees')
urlpatterns = [
    path('students/', views.studentView),
    path('students/<int:pk>/', views.studentDetailView),
    #path('employees/', views.Employees.as_view()),
    #path('employees/<int:pk>', views.EmployeesDetail.as_view()),
    path('', include(router.urls)),
    path('blogs/', views.BlogsView.as_view()),
    path('comments/', views.CommentsView.as_view()),
    path('blogs/<int:pk>/', views.BlogDetailView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
    # path('customers/', views.CustomerView.as_view()),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('gettoken/', obtain_auth_token)
    path('gettoken/', CustomAuthToken.as_view()),
    path('getjwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifyToken/', TokenVerifyView.as_view(), name='token_verify')
]
