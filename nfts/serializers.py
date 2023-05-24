from rest_framework import serializers

from nfts.models import Nft


class NftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nft
        fields = "__all__"
