from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Название"))
    description = models.TextField(verbose_name=_("Описание"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")