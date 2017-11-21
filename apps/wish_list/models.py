from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
	def validator(self, postData):
		errors = {}
		if len(postData['name']) < 2 or len(postData['username']) < 2:
			errors['name_error'] = "First Name and Username must be at least two characters"
		if len(postData['password']) < 8 or len(postData['confirm_password']) < 8:
			errors['password_length'] = "Password must be at least eight characters"
		if postData['password'] != postData['confirm_password']:
			errors['password_match'] = "Passwords must match"
		if User.objects.filter(username = postData['username']):
			errors['exist'] = "Username already taken.  Please choose another Username."
		return errors

	def login(self, postData):
		member = User.objects.filter(username = postData['username'])
		if len(member) > 0:
			member = member[0]
			if bcrypt.checkpw(postData['password'].encode(), member.password.encode()):
				user = {'user': member}
				return user
			else:
				errors = { 'error': "Login Invalid"}
				return errors
		else:
			errors = { 'error': "Login Invalid"}
			return errors
class ItemManager(models.Manager):
	def item(self, postData, user_id):
		print postData
		item = Item.objects.filter(item_name= postData['product'])
		if len(item) > 0:
			return {'status': 'Item already exist'}
		if len(postData['product']) == 0:
			errors = {'status': "No item added. Please add an item"}
			return errors
		else:
			newitem = Item.objects.create(item_name = postData['product'], user = User.objects.get(id=user_id))
			User.objects.get(id=user_id).liked_items.add(newitem)
			return {'status': 'adding'}


class User(models.Model):
	name = models.CharField(max_length = 255)
	username = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Item(models.Model):
	item_name = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(User, related_name = 'items')
	liked_user = models.ManyToManyField(User, related_name = "liked_items")
	objects = ItemManager()

