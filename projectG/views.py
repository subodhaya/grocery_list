from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse 
from .models import User,ListDatabase,GroceryList,GroceryItem
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import HttpResponse,HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db.models import Q








# Create your views here.

  # Authenticated users view their inbox
 
def index(request):
    if request.user.is_authenticated:
         all_lists =GroceryList.objects.filter(Q(user=request.user) | Q(shared_with=request.user))
         print("ffffffff out display")
    # Create a dictionary to organize the data by lists
         data_by_lists = {}
         for grocery_list in all_lists:
          items = GroceryItem.objects.filter(list=grocery_list)
          data_by_lists[grocery_list] = items
        

         return render(request, 'index.html', {'data_by_lists': data_by_lists}) 
    else:
        print("ffffffffffffffindex")
        return HttpResponseRedirect(reverse("login"))

    # Everyone else is prompted to sign in

@csrf_exempt
@login_required
def get_items(request, list_id):
    try:
        # Fetch the grocery list based on the provided list_id
        grocery_list_name = GroceryList.objects.get(id=list_id)

        # Fetch items for the specified grocery list
        items = GroceryItem.objects.filter(list=grocery_list_name)

        # Serialize the items to JSON format
        serialized_items = []
        for item in items:
            serialized_items.append({
                'name': item.name,
                'quantity': item.quantity,
                'instruction': item.instruction,
                'added': item.added
            })

        # Return the serialized items and the name of the grocery list as a JSON response
        return JsonResponse({
            'list_name': grocery_list_name.name,
            'items': serialized_items
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@login_required
def update_item(request, list_id, item_id):
    if request.method == 'POST':
        try:
            item = GroceryItem.objects.get(pk=item_id)
            item.added = not item.added
            print("added=true")
            item.save()
            return JsonResponse({'message': 'Item updated successfully'})
        except GroceryItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)    

@login_required
def delete_list(request, list_id):
    grocery_list = get_object_or_404(GroceryList, id=list_id)
    print("in delete")
    if request.user == grocery_list.user:
        grocery_list.delete()
        return JsonResponse({'message': 'List deleted successfully'})
    else:
        return JsonResponse({'message': 'Permission denied.'}, status=403)
    
@login_required
def edit_list(request, list_id):
    try:
        # Fetch the grocery list based on list_id
        grocery_list = GroceryList.objects.get(id=list_id)

        # Fetch the associated grocery items
        items = GroceryItem.objects.filter(list=grocery_list)
        print("ffffffffffffffsedit now")
        # Pass the data to the template
        context = {
            'list_name': grocery_list.name,
            'items': items,
        }
        print(context)

        return render(request, 'edit.html', context)

    except GroceryList.DoesNotExist:
        # Handle the case where the list doesn't exist
        return render(request, 'edit.html', {'error_message': 'List not found'})  

@login_required
def shopnow_view(request, list_id):
    try:
        # Fetch the grocery list based on list_id
        grocery_list = GroceryList.objects.get(id=list_id)

        # Fetch the associated grocery items
        items = GroceryItem.objects.filter(list=grocery_list)
        print("ffffffffffffffshop now")
        # Pass the data to the template
        context = {
            'list_name': grocery_list.name,
            'items': items,
            'finished' :grocery_list.finished,
        }

        return render(request, 'shopnow.html', context)

    except GroceryList.DoesNotExist:
        # Handle the case where the list doesn't exist
        return render(request, 'shopnow.html', {'error_message': 'List not found'})

@login_required
def display_all_lists(request):
    # Fetch all GroceryList objects
    all_lists = GroceryList.objects.all()
    print("ffffffff out display")
    # Create a dictionary to organize the data by lists
    data_by_lists = {}
    for grocery_list in all_lists:
        items = GroceryItem.objects.filter(list=grocery_list)
        data_by_lists[grocery_list] = items
        

    return render(request, 'index.html', {'data_by_lists': data_by_lists}) 
   



@login_required
def grocery_list(request):
   # grocery_list = GroceryList.objects.get(pk=name)
    items = GroceryItem.objects.filter(list=grocery_list)
    return render(request, 'list.html', {'list': grocery_list, 'items': items})

@login_required
def create_list(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST['name']
        if name:
            grocery_list = GroceryList.objects.create(user=user, name=name)
    return HttpResponseRedirect('grocery_lists')


@login_required
def add_item(request, name):
    print("ffffffff out add item")
    if request.method == 'POST':
        grocery_list = GroceryList.objects.get(pk=name)
        name = request.POST['name']
        if name:
            item = GroceryItem.objects.create(list=grocery_list, name=name)
    return HttpResponseRedirect('grocery_list', list_id=name)

@login_required
@csrf_exempt
def share_list(request, list_id):
    if request.method == 'POST':
       
        tdata = json.loads(request.body.decode('utf-8'))
        target_userName = tdata.get('target_username', '')
        print(tdata)
        print(target_userName)
        grocery_list = get_object_or_404(GroceryList, id=list_id)
        print("inside sharelist")
        if request.user == grocery_list.user:
            try:
                target_user = User.objects.get(username=target_userName)
                grocery_list.shared_with.add(target_user)
                return JsonResponse({'message': f'Shared with {target_userName}.'})
            except User.DoesNotExist:
                return JsonResponse({'message': 'User not found.'}, status=400)
        else:
            return JsonResponse({'message': 'please give valid user name.'}, status=403)

    return JsonResponse({'message': 'Invalid request.'}, status=400)

@login_required
@csrf_exempt
def log_lists(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)

            for list_name, items in data.items():
                # Check if a list with the given name already exists
                grocery_list, created = GroceryList.objects.get_or_create(name=list_name, user=request.user)

                for item_data in items:
                    item_name = item_data['name']
                    item_quantity = item_data['quantity']
                    item_instruction = item_data['instruction']

                    GroceryItem.objects.create(
                        list=grocery_list,
                        name=item_name,
                        quantity=item_quantity,
                        instruction=item_instruction,
                        user=request.user,
                        added=False,
                    )

            print("out of log_list")
            return JsonResponse({'message': 'Data stored successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data', 'error': str(e)}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=400)




@login_required
def delete_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(GroceryItem, pk=item_id)
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully'})
    return JsonResponse({'message': 'Invalid request'}, status=400)

@login_required
def log_Edit_lists(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)

            
            edit_list_data = data.get('editListItems', [])
            newly_added_data = data.get('newlyAddedItems', [])
            
            list_name = data.get('listName')  # Get the listName from the JSON data
            print(list_name)
            GroceryItem.objects.filter(list__name=list_name).delete()
            # Create or get the GroceryList instance
            grocery_list, created = GroceryList.objects.get_or_create(name=list_name)
            
        # Delete the grocery list
            
            
            # Process editListItems data
            for item_data in edit_list_data:
                item_name = item_data.get('name')
                item_quantity = item_data.get('quantity')
                item_instruction = item_data.get('instruction')
                # Assuming you have a ForeignKey to User for the user who added the item
                user = request.user 
                

                GroceryItem.objects.create(
                    list=grocery_list,
                    name=item_name,
                    quantity=item_quantity,
                    instruction=item_instruction,
                    user=user,
                    added=False,
                )

            # Process newlyAddedItems data
            for item_data in newly_added_data:
                item_name = item_data.get('name')
                item_quantity = item_data.get('quantity')
                item_instruction = item_data.get('instruction')
                # Assuming you have a ForeignKey to User for the user who added the item
                user = request.user  # Replace this with your actual user logic
                GroceryItem.objects.create(
                    list=grocery_list,
                    name=item_name,
                    quantity=item_quantity,
                    instruction=item_instruction,
                    user=user,
                    added=False,
                )

            return JsonResponse({'message': 'Data stored successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data', 'error': str(e)}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=400)

@login_required    
def submit_list(request, list_id):
    if request.method == 'POST':
        grocery_list = GroceryList.objects.get(pk=list_id)
        grocery_items = request.POST.getlist('grocery_item')
        print(grocery_list)
        print(grocery_items)
        for item_data in grocery_items:
            item_name, item_quantity, item_instruction = item_data.split(',')
            GroceryItem.objects.create(list=grocery_list, name=item_name, quantity=item_quantity, instruction=item_instruction)
        
        return HttpResponseRedirect('index')  # Redirect to the main page or wherever you want

    return HttpResponseRedirect('index')


@login_required
def finished_task(request, list_id):
    if request.method == 'POST':
        grocery_list = GroceryList.objects.get(pk=list_id)
        grocery_items = request.POST.getlist('grocery_item')
        
        for item_data in grocery_items:
            item_name, item_quantity, item_instruction = item_data.split(',')
            GroceryItem.objects.create(list=grocery_list, name=item_name, quantity=item_quantity, instruction=item_instruction)

    if request.method == "PUT":
        data = json.loads(request.body)
        
        if data.get("finished") is not None:
            grocery_list.finished = data["finished"]
        grocery_list.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)       
        

@login_required
@csrf_exempt  # You may need to handle CSRF protection differently in your project
def update_task_status(request, list_id):
    try:
        
        grocery_list = GroceryList.objects.get(id=list_id)
        print(grocery_list)
        print("hi inside update_task_status")
        if request.method == 'POST':
            # Toggle the 'finished' status
            print(grocery_list.finished)
            grocery_list.finished = not grocery_list.finished
            print(grocery_list.finished)
            grocery_list.save()
            return JsonResponse({'message': 'Status updated successfully'})
    except GroceryList.DoesNotExist:
        return JsonResponse({'message': 'List not found'}, status=404)
    return JsonResponse({'message': 'Invalid request'}, status=400)


@login_required
def update_list_status(request, list_id):
    try:
        grocery_list = GroceryList.objects.get(id=list_id)
        print("ffffffff out update save")
        if request.method == 'POST':
            # Toggle the 'finished' status
            grocery_list.saved_list = not grocery_list.saved_list
            grocery_list.save()
            return JsonResponse({'message': 'Status updated successfully'})
    except GroceryList.DoesNotExist:
        return JsonResponse({'message': 'List not found'}, status=404)
    return JsonResponse({'message': 'Invalid request'}, status=400)

@login_required
def get_finished_lists(request):
   if request.user.is_authenticated:
        # Fetch all the finished lists and their associated items
        finished_lists = GroceryList.objects.filter(finished=True).prefetch_related('groceryitem_set')
        print(finished_lists)
        # Create a dictionary to organize the data by lists
        data_by_lists = {}
        for grocery_list in finished_lists:
            items = grocery_list.groceryitem_set.all()  # Retrieve associated items
            data_by_lists[grocery_list] = items

        return render(request, 'index.html', {'data_by_lists': data_by_lists})
   else:
        return HttpResponseRedirect(reverse("login"))

@login_required   
def get_saved_lists(request):
   if request.user.is_authenticated:
        # Fetch all the finished lists and their associated items
        saved_lists = GroceryList.objects.filter(saved_list=True).prefetch_related('groceryitem_set')

        # Create a dictionary to organize the data by lists
        data_by_lists = {}
        for grocery_list in saved_lists:
            items = grocery_list.groceryitem_set.all()  # Retrieve associated items
            data_by_lists[grocery_list] = items

        return render(request, 'index.html', {'data_by_lists': data_by_lists})
   else:
        return HttpResponseRedirect(reverse("login"))   
   


@csrf_exempt
@login_required

@login_required
def get_list_names(request):
    list_names_queryset = GroceryList.objects.values('name')

    # Convert the QuerySet to a list of dictionaries
    list_names = list(list_names_queryset)
    print(list_names)

    # Return the list names as JSON
    return JsonResponse({'list_names': list_names})


@csrf_exempt
def login_view(request):
    
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "login.html", {
                "message": "Invalid user name and/or password."
            })
    else:
        return render(request, "login.html")
    
@csrf_exempt
def logout_view(request):
    print("fffffffffffffff")
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
    
    

