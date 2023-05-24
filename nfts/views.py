import logging
import os
import random
from io import BytesIO

import boto3
import requests
from django.http import FileResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from nfts.models import Nft
from nfts.serializers import NftSerializer


DEFAULT_BUCKET = 'ilyats-aws-engx-images'
REGION = 'eu-central-1'

class NftList(generics.ListCreateAPIView):
    queryset = Nft.objects.all()
    serializer_class = NftSerializer


class NftDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nft.objects.all()
    serializer_class = NftSerializer

    def delete(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            img_obj = Nft.objects.get(pk=pk)
        except Exception:
            return Response("Object not found", status=400)

        file_name = img_obj.url.split("/")[-1]
        s3 = boto3.client('s3')
        s3.delete_object(
            Bucket=DEFAULT_BUCKET,
            Key=f'nfts/{file_name}',
        )

        img_obj.delete()

        return Response("Deleted successfully")


@api_view(['GET'])
def download_nft(request):
    path = request.GET.get("path")
    if path:
        path = path.strip().replace('"', '').replace("'", "")
        try:
            file_res = requests.get(path)
            file_name = os.path.split(path)[1]
            response = FileResponse(BytesIO(file_res.content), as_attachment=True)
            response['Content-Type'] = file_res.headers.get('Content-Type')
            response['Content-Length'] = file_res.headers.get('Content-Length')
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
        except Exception as exc:
            logging.error(f"Failed with {exc}")

    return Response("Wrong URL provided", status=400)


@api_view(['POST'])
def upload_nft(request):
    file = request.FILES.get('file')
    if file:
        s3 = boto3.resource('s3')
        res = s3.Bucket(DEFAULT_BUCKET).put_object(
            Key=f'nfts/{file.name}',
            Body=file,
            ACL='public-read'
        )

        img_name = file.name.split('.')[0]
        new_obj = Nft(
            name=img_name,
            description=img_name,
            url=f"https://{res.bucket_name}.s3.{REGION}.amazonaws.com/{res.key}",
            size="1024x1024",
            price=random.randrange(100)
        )
        new_obj.save()
        return Response("ok")
    else:
        Response("No file found", 400)


@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "NftList": reverse("nft-list", request=request, format=format),
        "NftDetails": reverse("nft-detail", request=request, format=format, kwargs={"pk": 1})
    })
