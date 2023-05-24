from django.db import models


class Nft(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField()
    url = models.CharField(max_length=1024, default="/")
    owner = models.CharField(max_length=512, default="Ilya")
    size = models.CharField(max_length=32)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "nfts"
