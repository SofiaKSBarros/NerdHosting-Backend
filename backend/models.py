from django.db import models


class Plans(models.Model):
    class RAM:
        GB_4 = 4
        GB_8 = 8
        GB_16 = 16

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    cpu = models.IntegerField(default=4, min_value=4, max_value=8)
    ram = models.IntegerField(choices=[(RAM.GB_4, '4G'), (RAM.GB_8, '8G'), (RAM.GB_16, '16G')])
    gpu = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.gpu:
            self.is_google = False
        elif self.is_google:
            self.gpu = False
        super().save(*args, **kwargs)

    is_google = models.BooleanField(default=False)
    

class MinecraftServer(models.Model):
    class Modloader:
        VANILLA = 'VANILLA'
        NEOFORGE = 'NEOFORGE'
        FORGE = 'FORGE'
        FABRIC = 'FABRIC'
        PAPER = 'PAPER'
        FOLIA = 'FOLIA'
        CURSEFORGE = 'CURSEFORGE'
        
    name = models.CharField(max_length=100)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='minecraft_servers')
    version = models.CharField(max_length=20)
    curseforge_url = models.URLField(blank=True, null=True)
    modloader = models.CharField(max_length=20, choices=[
        (Modloader.VANILLA, 'VANILLA'),
        (Modloader.NEOFORGE, 'NEOFORGE'),
        (Modloader.FORGE, 'FORGE'),
        (Modloader.FABRIC, 'FABRIC'),
        (Modloader.PAPER, 'PAPER'),
        (Modloader.FOLIA, 'FOLIA'),
        (Modloader.CURSEFORGE, 'CURSEFORGE')
    ])  
        