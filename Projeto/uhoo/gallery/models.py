from django.db import models
from sorl.thumbnail import ImageField
from django.core.urlresolvers import reverse
from choices import GENERAL_PRIVACY 
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import permalink
from likeable.models import Likeable
import simplejson

    

class album(Likeable):
    titulo = models.CharField(u'Titulo', max_length = 100)
    slug = models.SlugField(max_length = 100, blank = True, unique = True)
    data = models.DateTimeField(auto_now = True)
    privacidade = models.CharField(max_length = 2, choices = GENERAL_PRIVACY)
    owner = models.ForeignKey(User) 
    capa = models.ForeignKey('photo', blank=True, null=True)
    photos = models.ManyToManyField('photo', related_name='photo_sets')
    
    def __unicode__(self):   
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('album', kwargs={'slug': self.slug})
    
    class Meta:
        ordering = ('titulo', )
        db_table = 'album' 
        verbose_name_plural = 'Albuns'



class photo(Likeable):
    titulo = models.CharField(u'Titulo', max_length = 100)
    slug = models.SlugField(max_length = 100, blank = True, unique = True)
    descricao = models.TextField(blank = True)
    image = ImageField(upload_to = 'galeria')
    dataPublicacao = models.DateTimeField(auto_now = True)
    privacidade = models.CharField(max_length = 2, choices = GENERAL_PRIVACY)
    
    
    def _set_exif(self, d):
        self._exif = simplejson.dumps(d)

    def _get_exif(self):
        if self._exif:
            return simplejson.loads(self._exif)
        else:
            return {}

    exif = property(_get_exif, _set_exif, "Photo EXIF data, as a dict.")
    
    def __unicode__(self):
        return self.titulo
    
    @permalink
    def get_absolute_url(self):
        #return reverse('album', kwargs={'slug': self.slug})
        return self.original
    
    def get_exibicao(self):
        nome_arq = str(self.original)
        delimiter = nome_arq.find(".jpg")
        nome_arq = nome_arq[:delimiter] + ".500x500.jpg"
        return nome_arq
    
    def get_thumbnail(self):
        nome_arq = str(self.original)
        delimiter = nome_arq.find(".jpg")
        nome_arq = nome_arq[:delimiter] + ".125x125.jpg"
        return nome_arq
        
      
    @property
    def url(self):
        return '%s%s' % (settings.MEDIA_URL, self.image)
    
   
        
    class Meta: 
        ordering =('dataPublicacao',)
        db_table = 'photo'
        
    