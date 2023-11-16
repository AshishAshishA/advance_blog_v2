from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    
# class Authen(models.Model):
#     author = models.CharField(max_length=30,unique=True)
#     password = models.CharField(max_length=15)
    
#     def __str__(self):
#         return f"Author {self.author} : password {self.password}"
    
    # def authenticate(self,user,author,username,password,real_password):
    #     if author==username and password==real_password:
    #         return user
    #     else:
    #         return None


class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories  = models.ManyToManyField("Category" ,related_name="posts")
    authen = models.ForeignKey(User, on_delete=models.CASCADE)
    slug=models.SlugField(null=True,unique=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'slug': self.slug})
    
class Comment(models.Model):
    author = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.post} by {self.author}"
