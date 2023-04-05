from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from datetime import date
from django.utils.safestring import mark_safe

class Department(models.Model):
    """Model representing store department or section."""
    name = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access list of items in department."""
        return reverse('department-items', args=[str(self.id)])

class Item(models.Model):
    department = models.ForeignKey('Department', models.SET_NULL, blank=True, null=True)
    writtenId = models.CharField('Written ID', help_text= mark_safe('<i>The number written on item</i>'), max_length=30, unique=True)
    name = models.CharField(max_length=30, help_text= mark_safe('<i>e.g. cordless drill 3</i>'))
    date_added = models.DateField(auto_now_add=True)
    condition = models.TextField(max_length=100, help_text='Update changes upon return if necessary', blank=True, null=True)
    donor =  models.ForeignKey(User, related_name='donor', on_delete=models.SET_NULL, null=True, blank=True)
    borrower = models.ForeignKey(User, related_name='borrower', on_delete=models.SET_NULL, null=True, blank=True)
    due_back = models.DateField(blank=True, null=True)
    image = models.CharField(max_length = 200, blank=True)

    LOAN_STATUS = (
        ('a', 'Available'),
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Item availability',
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['status','due_back']
        permissions = (
            ("can_mark_returned", "Can checkout and return items"), 
            ("donation_intake", "Process new donations"),
            )

    def __str__(self):
        return f'{self.writtenId} ({self.name})'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this item."""
        return reverse('item-detail', args=[str(self.id)])

class Transaction(models.Model):
    librarian = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='librarian')
    writtenId = models.CharField("Written ID", max_length=30, default='0000')
    name = models.CharField(max_length=30)
    condition = models.TextField(max_length=100, blank=True, null=True)
    checked_out_to = models.ForeignKey(User, models.SET_NULL, related_name='checked_out_to', blank=True, null=True)
    due_back = models.DateField(blank=True, null=True)
    transaction_date= models.DateField(auto_now_add=True)