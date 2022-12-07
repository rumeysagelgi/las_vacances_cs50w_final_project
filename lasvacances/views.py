import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import List, List_item, Suite, Rating, Review, User


def index(request):
    return render(request, "lasvacances/index.html")


@csrf_exempt
def add_suite(request):

    # Checks if current user is staff
    if not request.user.is_authenticated:
        messages.error(request, f"Forbidden.")
        return render(request, "lasvacances/apology.html", status=403)

    if request.method == "POST":
        image = request.POST["image"]
        title = request.POST["title"]
        address = request.POST["address"]
        price = request.POST["price"]
        details = request.POST["details"]

        # Attempts to save new suite
        try:
            suite = Suite(image=image, title=title, address=address, price=price, details=details)
            suite.save()
            messages.success(request, "Successfully added to the database.")
        except ValueError:
            messages.error(request, "Failed to add to the database.")
            return render(request, "lasvacances/add_suite.html", status=500)

        return render(request, "lasvacances/add_suite.html")

    return render(request, "lasvacances/add_suite.html")


@csrf_exempt
def add_list(request):

    if request.method == "GET":
        if not request.user.username:
            messages.error(request, f"You must be logged in to access this page.")
            return render(request, "lasvacances/apology.html", status=403)

        return render(request, "lasvacances/add_list.html")

    if request.method == "POST":
        author = request.user
        name = request.POST['name']

        if not author.username:
            messages.error(request, f"Failed. You must be logged in to create a list.")
            return render(request, "lasvacances/apology.html", status=403)

        if not name:
            messages.error(request, f"Failed. Your list must have a name.")
            return render(request, "lasvacances/apology.html", status=500)

        # Attempts to save new list
        try:
            new_list = List(author=author, name=name)
            new_list.save()
            messages.success(request, "Successfully added to the database.")
        except Exception:
            messages.error(request, f"Failed to create new list.")
            return render(request, "lasvacances/apology.html", status=500)

        return HttpResponseRedirect(reverse("list", args=(new_list.id,)))


@csrf_exempt
def add_to_list(request):
    if request.method == "POST":

        # Checks if user is logged in
        if not request.user.is_authenticated:
            messages.error(request, f"You must be logged in to perform this action.")
            return render(request, "lasvacances/apology.html", status=403)

        # Attemps to find provided list and suite
        try:
            list = List.objects.get(pk=request.POST['list'])
            suite = Suite.objects.get(pk=request.POST['suite'])
        except list.DoesNotExist or suite.DoesNotExist:
            messages.error(request, f"Failed. Invalid suite or invalid list.")
            return render(request, "lasvacances/apology.html", status=500)

        # Ensures suite is not already on the list
        if suite.listed.filter(list=list):
            messages.error(request, f"Suite is already on the list.")
            return render(request, "lasvacances/apology.html", status=500)

        # Attempts to save new list entry
        try:
            new_list_item = List_item(list=list, suite=suite)
            new_list_item.save()
            messages.success(request, "Successfully added to the selected list.")
        except Exception:
            messages.error(request, f"Failed to add to the selected list.")
            return render(request, "lasvacances/apology.html", status=500)

        return HttpResponseRedirect(reverse("list", args=(list.id,)))


@csrf_exempt
def add_review(request, suite_id):
    if request.method == "POST":
        author = request.user
        if not author.is_authenticated:
            messages.error(request, f"You must be logged in to perform this action.")
            return render(request, "lasvacances/apology.html", status=403)

        # Attempts to find suite
        try:
            suite = Suite.objects.get(pk=suite_id)
        except Suite.DoesNotExist:
            messages.error(request, f'Suite not found.')
            return render(request, "lasvacances/apology.html", status=500)

        rating = request.POST['rating']
        review = request.POST['review']
        title = request.POST['title']

        if int(rating) < 0 or int(rating) > 10:
            messages.error(request, f"Rating has to be an integer between 0 and 10.")
            return render(request, "lasvacances/apology.html", status=500)

        # Ensures movie is not already reviewd
        check_reviewed = suite.reviewed.filter(suite=suite, author=author)
        if check_reviewed:
            messages.error(request, f"You have already reviewed this suite.")
            return HttpResponseRedirect(reverse("review", args=(check_reviewed[0].id,)))

        # Attempts to add new review entry to the database
        try:
            new_review = Review(author=author, suite=suite, rating=rating, review=review, title=title)
            new_review.save()
        except Exception:
            messages.error(request, f"Failed to add review to the database.")
            return render(request, "lasvacances/apology.html", status=500)

        # Calculates new movie rating
        average_review_ratings = suite.reviewed.all().aggregate(Avg('rating'))
        suite_rating = round(average_review_ratings['rating__avg'], 2)

        # Attempts to update movie rating
        try:
            new_rating = Rating.objects.get(suite=suite)
            new_rating.rating = Decimal(suite_rating)
            new_rating.save()
        except Rating.DoesNotExist:
            new_rating = Rating(suite=suite, rating=suite_rating)
            new_rating.save()
        except Exception:
            messages.error(request, f"Failed to add rating to the database.")
            return render(request, "lasvacances/apology.html", status=500)

        messages.success(request, "Successfully added review to the database.")
        return HttpResponseRedirect(reverse("suite", args=(suite.id,)))


@csrf_exempt
def edit_review(request, review_id):

    # Attempts to query requested post
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found."}, status=404)

    suite = review.suite

    # Ensures edit is made by the reviews's author
    if not request.user.id == review.author.id:
        return JsonResponse({"error": "Forbidden action."}, status=403)

    # Handles edit button request
    if request.method == "GET":
        return JsonResponse({
            "title": review.title,
            "rating": review.rating,
            "review": review.review
        })

    # Handles confirm button request
    if request.method == "PUT":
        data = json.loads(request.body)
        review.title = data['title']
        review.rating = data['rating']
        if int(data['rating']) < 0 or int(data['rating']) > 10:
            return JsonResponse({"error": "Rating has to be an integer between 0 and 10."}, status=500)
        review.review = data['review']
        review.save()

        # Calculates new movie rating
        average_review_ratings = suite.reviewed.all().aggregate(Avg('rating'))
        suite_rating = round(average_review_ratings['rating__avg'], 2)

        # Updates movie rating
        new_rating = Rating.objects.get(suite=suite)
        new_rating.rating = Decimal(suite_rating)
        new_rating.save()

    # Handles delete button request
    if request.method == "POST":
        review.delete()
        reviews = suite.reviewed.all()
        new_rating = Rating.objects.get(suite=suite)

        if not reviews:
            new_rating.delete()
        else:
            average_review_ratings = reviews.aggregate(Avg('rating'))
            suite_rating = round(average_review_ratings['rating__avg'], 2)
            new_rating.rating = Decimal(suite_rating)
            new_rating.save()

        messages.success(request, f'Review "{review.title}" is successfully deleted.')
        return HttpResponseRedirect(reverse('suite', args=(review.suite.id,)))

    return HttpResponse(status=204)


@csrf_exempt
def delete_list(request, list_id):
    if request.method == "POST":

        # Attempts to find list
        try:
            requested_list = List.objects.get(pk=list_id)
        except List.DoesNotExist:
            messages.error(request, f'List not found.')
            return render(request, "lasvacances/apology.html", status=500)

        # Ensures request is made by the list's author
        if not request.user.id == requested_list.author.id:
            messages.error(request, f'Forbidden action.')
            return render(request, "lasvacances/apology.html", status=403)

        # Deletes list from the database
        requested_list.delete()
        messages.success(request, f'List "{requested_list.name}" is successfully deleted.')
        return HttpResponseRedirect(reverse('lists', args=(request.user.username,)))
    else:
        messages.error(request, f'Forbidden request.')
        return render(request, "lasvacances/apology.html", status=403)


def get_suite(request):

    # Handles kwargs request from index page search
    query = str(request.GET.get('suite', ''))
    if not query:
        return JsonResponse({'suites': None})

    # Selects all movies
    suites = Suite.objects.filter(address__contains=query).order_by('address')

    return JsonResponse([suite.serialize() for suite in suites], safe=False)


@csrf_exempt
def list(request, list_id):
    if request.method == "GET":

        # Attempts to find list
        try:
            requested_list = List.objects.get(pk=list_id)
        except List.DoesNotExist:
            messages.error(request, f'List not found.')
            return render(request, "lasvacances/apology.html", status=500)

        # Gets requested_list items
        list_items = List_item.objects.filter(list=requested_list)

        return render(request, "lasvacances/list.html", {
            "list": requested_list,
            "list_items": list_items
        })


@csrf_exempt
def lists(request, username):
    if request.method == "GET":

        # Attempt to find user
        try:
            requested_user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f'User "{username}" not found.')
            return render(request, "lasvacances/apology.html", status=500)

        # Gets all requested_user lists in reverse chronological order
        requested_user_lists = List.objects.filter(author=requested_user).order_by('-id')

        return render(request, "lasvacances/lists.html", {
            "requested_user": requested_user,
            "lists": requested_user_lists,
            "suites_qnt": len(requested_user_lists)
        })


@csrf_exempt
def suite(request, suite_id):
    if request.method == "GET":

        # Attempts to find suite
        try:
            suite = Suite.objects.get(pk=suite_id)
        except Suite.DoesNotExist:
            messages.error(request, f'Suite not found.')
            return HttpResponseRedirect(reverse('index'))

        # Attempts to get suite's rating
        try:
            rating = Rating.objects.get(suite=suite)
        except Rating.DoesNotExist:
            rating = None

        # Gets recent 3 reviews
        reviews = Review.objects.filter(suite=suite).order_by("-id")[:3]

        # Gets all current user lists
        lists = None
        if request.user.is_authenticated:
            lists = List.objects.filter(author=request.user).order_by("-id")

        return render(request, "lasvacances/suite.html", {
            "suite": suite,
            "rating": rating,
            "reviews": reviews,
            "lists": lists
        })


@csrf_exempt
def suite_reviews(request, suite_id):
    if request.method == "GET":

        # Attempts to find suite
        try:
            suite = Suite.objects.get(pk=suite_id)
        except Suite.DoesNotExist:
            messages.error(request, f'Suite not found.')
            return render(request, "lasvacances/apology.html", status=500)

        # Gets all suite reivews
        suite_reviews = Review.objects.filter(suite=suite).order_by('-id')

        return render(request, "lasvacances/suite_reviews.html", {
            "suite": suite,
            "reviews": suite_reviews
        })


@csrf_exempt
def profile(request, username):
    if request.method == "GET":

        # Attempts to find user
        try:
            requested_user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f'User "{username}" not found.')
            return render(request, "lasvacances/apology.html", status=500)

        # Gets recent 3 requested_user lists in reverse chronological order
        requested_user_lists = List.objects.filter(author=requested_user).order_by("-id")

        # Gets recent 3 requested_user reviews in reverse chronological order
        requested_user_reviews = Review.objects.filter(author=requested_user).order_by("-id")

        return render(request, "lasvacances/profile.html", {
            "requested_user": requested_user,
            "lists": requested_user_lists[:3],
            "reviews": requested_user_reviews[:3],
            "reviews_num": len(requested_user_reviews),
            "lists_num": len(requested_user_lists)
        })


@csrf_exempt
def review(request, review_id):
    if request.method == "GET":

        # Attempts to find review
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            messages.error(request, f'Review not found.')
            return render(request, "lasvacances/apology.html", status=500)

        return render(request, "lasvacances/review.html", {
            "review": review
        })


@csrf_exempt
def user_reviews(request, username):
    if request.method == "GET":

        # Attempt to find user
        try:
            requested_user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f'Username "{username}" not found')
            return render(request, "lasvacances/apology.html", status=500)

        # Gets all reviews from requested_user
        user_reviews = Review.objects.filter(author=requested_user).order_by('-id')

        return render(request, "lasvacances/user_reviews.html", {
            "requested_user": requested_user,
            "reviews": user_reviews
        })


@csrf_exempt
def login_view(request):
    if request.method == "POST":

        # Attempts to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Checks if authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "lasvacances/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            messages.error(request, f"You are already logged in.")
            return render(request, "lasvacances/apology.html", status=403)
        return render(request, "lasvacances/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def register(request):
    if request.method == "POST":
        avatar = request.POST["avatar"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensures password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "lasvacances/register.html", {
                "message": "Passwords must match."
            })

        # Attempts to create new user
        try:
            user = User.objects.create_user(avatar=avatar, username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "lasvacances/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            messages.error(request, f"You are already logged in.")
            return render(request, "lasvacances/apology.html", status=403)
        return render(request, "lasvacances/register.html")