from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate(self, form): #i had used postData here and in the if statements instead of form -what's the difference?
        errors = {}
        if len(form['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(form['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        EMAIL_REGEX =re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form['email']):                
            errors["email"] = "Invalid email address"
        email_check = self.filter(email=form['email']) #forgot to add
        if email_check:
            errors['email'] = "Email already in use"
        if len(form['password']) < 8:
            errors["password"] = "Password must be a minimum of eight characters"
        PASSWORD_REGEX =re.compile(r'')
        if not PASSWORD_REGEX.match(form['password']):                
            errors["password"] = "Invalid password"
        #if form['password'] != form['confirm']:
            #errors['password'] = 'Passwords do not match'
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()