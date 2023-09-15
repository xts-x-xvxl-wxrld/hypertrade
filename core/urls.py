from django.urls import path
from core.views import candleInfo, candlePage, setDbValues
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/candle-csv/', candleInfo, name='candle-info-live'), # type: ignore
    path('', candlePage, name='candle-webpage'),
    path('populate-db/', setDbValues, name='populate_db')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
