from django.urls import path

from nfts import views


urlpatterns = [
    path("", views.api_root),
    path("nfts/", views.NftList.as_view(), name="nft-list"),
    path("nft/<int:pk>/", views.NftDetail.as_view(), name="nft-detail"),
    path("download_nft/", views.download_nft),
    path("upload_nft/", views.upload_nft),
]
