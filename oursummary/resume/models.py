from django.urls import reverse

from django.db import models


class Resume(models.Model):
    title = models.CharField(max_length=255, verbose_name='Должность')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')
    letter = models.TextField(blank=True, verbose_name='Сопроводительное письмо')

    photo = models.ImageField(upload_to='photos/%Y/%m/%d')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_shown = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('resume', kwargs={'username': 'user',
                                         'resume_slug': self.slug})


class Education(models.Model):
    title = models.CharField(max_length=255, verbose_name='Учебное учреждение')
    year_start = models.CharField(max_length=4)
    year_end = models.CharField(max_length=4, blank=True)
    specialization = models.CharField(max_length=255, verbose_name='Специальность')
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.year_start}-{self.year_end} {self.title}\n {self.specialization}'


class Experience(models.Model):
    title = models.CharField(max_length=255)
    date_start = models.DateField()
    date_end = models.DateField(blank=True)
    post = models.CharField(max_length=255)
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date_start}-{self.date_end} {self.title}\n {self.post}'


