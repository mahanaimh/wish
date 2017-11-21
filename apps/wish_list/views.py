from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'wish_list/index.html')

def process(request):
    if request.method == 'POST':
		errors = User.objects.validator(request.POST)
		if errors:
			for error in errors:
				print errors
				messages.error(request, errors[error])
			return redirect('/')
		else:
			hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hashed_pw)
			request.session['id'] =  user.id
			request.session['username'] = user.username
			messages.success(request, 'You have successfully registered')
			return redirect('/dashboard')
    return redirect('/')

def login(request):
	if request.method == 'POST':
		model_return = User.objects.login(request.POST)
		if 'user' in model_return:
			request.session['id'] = model_return['user'].id
			request.session['username'] = model_return['user'].username
			return redirect('/dashboard')
		else:
			for error in model_return:
				messages.error(request, model_return[error])
			print messages
			return redirect('/')
	return redirect('/')

def dashboard(request):
    if not 'id' in request.session:
		return redirect('/')
    user = User.objects.get(id = request.session['id'])
    context = {
		'user': user,
		'liked_items': Item.objects.filter(liked_user = user).order_by('-created_at'),
		'all_items' : Item.objects.exclude(liked_user = user)
	}
    return render(request, 'wish_list/dashboard.html', context)

def create(request):
	if request.method == 'POST':
		errors = Item.objects.item(request.POST, request.session['id'])
		if errors['status'] != 'adding':
			messages.error(request, errors['status'])
			return render(request, 'wish_list/create.html')
		else:
			return redirect('/dashboard')
	return redirect('/dashboard')

def create_item(request):
	return render(request, 'wish_list/create.html')

def add(request, item_id):
	User.objects.get(id = request.session['id']).liked_items.add(Item.objects.get(id=item_id))
	return redirect('/dashboard')

def remove(request, item_id):
	Item.objects.get(id=item_id).liked_user.remove(User.objects.get(id=request.session['id']))
	return redirect('/dashboard')

def show(request, item_id):
	context ={
		'clicked_items': Item.objects.get(id=item_id),
		'liked_user':User.objects.filter(liked_items = Item.objects.get(id=item_id))
	}
	return render(request, 'wish_list/item.html', context)

def logout(request):
	del request.session['id']
	del request.session['username']
	return redirect('/')