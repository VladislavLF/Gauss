from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category_Tasks(models.Model):
    points = models.CharField(blank=False,max_length=10,verbose_name="Maximum points")
    difficult = models.CharField(blank=False,max_length=20,verbose_name="Complexity")

    def __str__(self):
        return f'Task {self.id}'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.id})

    class Meta:
        verbose_name = 'Categories for tasks'
        verbose_name_plural = 'Categories for tasks'


class Category_Tasks_Filter(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name="Filter name")
    slug = models.SlugField(max_length=255, blank=False, db_index=True, verbose_name="URL-slug")
    cat = models.ForeignKey('Category_Tasks', on_delete=models.PROTECT, null=True, verbose_name="Category Key")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Filters for tasks'
        verbose_name_plural = 'Filters for tasks'

    def get_absolute_url(self):
        return reverse('filter_category', kwargs={'filter_slug': self.slug})


class Task(models.Model):
    condition = models.TextField(blank=False,verbose_name="Condition")
    solution = models.TextField(blank=False,verbose_name="Solution")
    answer = models.TextField(blank=False,verbose_name="Answer")
    time_create = models.DateTimeField(auto_now_add=True,verbose_name="Time of creation")
    time_update = models.DateTimeField(auto_now=True,verbose_name="Update time")
    photo_condition = models.ImageField(upload_to="photos/%Y/%m/%d/",blank=True,verbose_name="Photo in the conditions")
    photo_before = models.ImageField(upload_to="photos/%Y/%m/%d/",blank=True,verbose_name="Photo before the decision")
    photo_after = models.ImageField(upload_to="photos/%Y/%m/%d/",blank=True,verbose_name="Photo after the decision")
    is_published = models.BooleanField(default=True,blank=False,verbose_name="<= will be published?")
    ytb = models.CharField(max_length=255,blank=True,default='',verbose_name="YouTube")
    cat = models.ForeignKey('Category_Tasks', on_delete=models.PROTECT, null=True,blank=False,verbose_name="Key to the task category")
    filter = models.ForeignKey('Category_Tasks_Filter', on_delete=models.PROTECT, null=True,blank=True,verbose_name="Key to the task filter category")

    def __str__(self):
        return self.condition.replace("<span>","").replace("</span>","")

    class Meta:
        verbose_name = 'Tasks'
        verbose_name_plural = 'Tasks'
        ordering = ['time_update']

    def get_absolute_url(self):
        return reverse('task_object', kwargs={'task_id': self.id})


class Category_Options(models.Model):
    description = models.CharField(max_length=255, verbose_name="Description")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time of creation")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    difficult = models.CharField(max_length=20, blank=False, verbose_name="Complexity")
    ytb = models.CharField(max_length=255, blank=True, default='', verbose_name="YouTube")
    is_published = models.BooleanField(default=True, blank=False, verbose_name="<= will be published?")

    id_number_1 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {1}")
    id_number_2 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {2}")
    id_number_3 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {3}")
    id_number_4 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {4}")
    id_number_5 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {5}")
    id_number_6 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {6}")
    id_number_7 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {7}")
    id_number_8 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {8}")
    id_number_9 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {9}")
    id_number_10 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {10}")
    id_number_11 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {11}")
    id_number_12 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {12}")
    id_number_13 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {13}")
    id_number_14 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {14}")
    id_number_15 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {15}")
    id_number_16 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {16}")
    id_number_17 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {17}")
    id_number_18 = models.CharField(max_length=255, blank=False, db_index=True, verbose_name=f"id for task {18}")

    def __str__(self):
        return f'Option {self.id}'

    def get_absolute_url(self):
        return reverse('option', kwargs={'opt_id': self.id})

    class Meta:
        verbose_name = 'Options'
        verbose_name_plural = 'Options'


class Theory_category(models.Model):
    category = models.CharField(max_length=100,blank=False,verbose_name="Theme")

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Section of Mathematics (Theory)'
        verbose_name_plural = 'Section of Mathematics (Theory)'


class Theory_item(models.Model):
    title = models.CharField(max_length=100,blank=False,verbose_name="Headline")
    ytb = models.CharField(max_length=255,blank=True,default='',verbose_name="YouTube")
    time_create = models.DateTimeField(auto_now_add=True,verbose_name="Time of creation")
    time_update = models.DateTimeField(auto_now=True,verbose_name="Update time")
    is_published = models.BooleanField(default=True,blank=False,verbose_name="<= will be published?")
    cat = models.ForeignKey('Theory_category', on_delete=models.PROTECT, null=True,verbose_name="Category Key")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Topic (Theory)'
        verbose_name_plural = 'Topic (Theory)'
        ordering = ['time_update']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,null=False, blank=False,  verbose_name="User")
    post = models.ForeignKey('Task', on_delete=models.PROTECT,null=False, blank=False,  verbose_name="Task")
    text = models.TextField(null=False, blank=False, verbose_name="Comment text")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Time of writing", blank=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Update time", blank=False)
    is_published = models.BooleanField(default=True,blank=False,verbose_name="<= will be published?")

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Comment {self.user} to task №{self.post.id} from {str(self.created).split()[0]} : {self.text}"
