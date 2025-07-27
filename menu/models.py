from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    path = models.CharField(max_length=500, editable=False)

    def save(self, *args, **kwargs):
        old_path = None
        if self.pk:
            try:
                old_path = Menu.objects.get(pk=self.pk).path
            except Menu.DoesNotExist:
                old_path = None

        if self.parent:
            self.path = f"{self.parent.path}/{self.name}"
        else:
            self.path = self.name

        super().save(*args, **kwargs)

        if old_path and self.path != old_path:
            prefix = old_path + '/'
            descendants = Menu.objects.filter(path__startswith=prefix)
            for desc in descendants:
                desc.path = self.path + desc.path[len(old_path):]
                desc.save(update_fields=['path'])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Menu item"
        verbose_name_plural = "Menu items"
        ordering = ['id']
