from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from .models import Post, Category
from django.http import Http404
from django.core.paginator import Paginator
from .forms import RegisterForm, LoginForm, PostForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages




# posts = [
#     {
#         'id': 1,
#         'title': 'Smart Farming Technologies Transforming Indian Agriculture',
#         'content': 'Smart farming uses sensors, drones, and IoT devices to collect real-time data from the field. This helps farmers make better decisions about irrigation, fertilization, and pest control, leading to higher yields and reduced costs.',
#         'image': '../static/blog/image/automation.jpg'
#     },
#     {
#         'id': 2,
#         'title': 'How Artificial Intelligence is Enhancing Crop Yields',
#         'content': 'AI is playing a major role in modern agriculture by analyzing weather patterns, soil data, and crop health. Farmers can now predict diseases early, optimize their planting schedule, and reduce waste with machine learning tools.',
#         'image': '../static/blog/image/AI_image.jpg'
#     },
#     {
#         'id': 3,
#         'title': '5G Connectivity to Boost Precision Farming',
#         'content': 'With the rollout of 5G networks, smart devices and machines on farms can communicate instantly. This enables better automation, live monitoring, and remote management of equipment, greatly improving efficiency in the field.',
#         'image': '../static/blog/image/5g.jpg'
#     },
#     {
#         'id': 4,
#         'title': 'The Rise of Vertical Farming in Urban Spaces',
#         'content': 'Vertical farming uses stacked layers to grow crops in controlled environments. It saves space, reduces water usage by up to 90%, and provides fresh produce year-round in cities where traditional farming is difficult.',
#         'image': '../static/blog/image/devops.jpg'
#     },
#     {
#         'id': 5,
#         'title': 'Blockchain for Transparent and Fair Agriculture Supply Chains',
#         'content': 'Blockchain technology allows for secure tracking of agricultural products from farm to market. It ensures fair pricing, prevents fraud, and builds trust among farmers, suppliers, and consumers by recording every transaction.',
#         'image': '../static/blog/image/blockchain.jpg'
#     },
#     {
#         'id': 6,
#         'title': 'Climate-Resilient Crops for a Sustainable Future',
#         'content': 'Scientists are developing new crop varieties that can survive extreme heat, droughts, and floods. These climate-resilient crops help farmers adapt to changing weather and ensure food security for the growing population.',
#         'image': '../static/blog/image/automation.jpg'
#     },
#     {
#         'id': 7,
#         'title': 'Drone Technology in Crop Monitoring and Spraying',
#         'content': 'Drones can scan large farm areas quickly and provide detailed images of crop health. They are also used for precision spraying of fertilizers and pesticides, reducing labor costs and environmental impact.',
#         'image': '../static/blog/image/AI_image.jpg'
#     },
#     {
#         'id': 8,
#         'title': 'Organic Farming: Healthier Soil and Food',
#         'content': 'Organic farming avoids synthetic chemicals and promotes the use of compost, green manure, and natural pest control. This not only improves soil fertility but also produces healthier, chemical-free food for consumers.',
#         'image': '../static/blog/image/5g.jpg'
#     },
#     {
#         'id': 9,
#         'title': 'Empowering Farmers Through Mobile Apps and e-Marketplaces',
#         'content': 'Digital platforms allow farmers to check crop prices, weather updates, and connect directly with buyers. These tools empower small-scale farmers to make informed decisions and access wider markets without middlemen.',
#         'image': '../static/blog/image/devops.jpg'
#     },
#     {
#         'id': 10,
#         'title': 'Sustainable Irrigation Methods Saving Water in Agriculture',
#         'content': 'Drip and sprinkler irrigation systems deliver water directly to the roots, minimizing waste. These sustainable methods help conserve water, reduce energy use, and ensure better crop productivity even in dry regions.',
#         'image': '../static/blog/image/blockchain.jpg'
#     }
# ]


# Create your views here.
def index(request):
    blog_title = "Latest Blogs"

    #all post get
    all_posts = Post.objects.all()

    #pagination 
    paginator = Paginator(all_posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'index.html',{'blog_title' : blog_title, 'page_obj' : page_obj})

def about(request):
    return render(request,'block/about.html')

# def index(request):
#     return HttpResponse("hello world")

# def detail(request):
#     return HttpResponse("You are viewing post details page")

def detail(request, slug):
    # get static data based on Id
    # post = next((item for item in posts if item['id'] == post_id), None)
    
    try:
        # getting data from model by post id
        post = Post.objects.get(slug=slug)
        posts = Post.objects.all()
        related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)

    except Post.DoesNotExist:
        raise Http404("Post Does Not Exist")

    # logger = logging.getLogger("TESTING")
    # logger.debug(f'post id is {post}')
    return render(request,'detail.html',{'post' : post, 'posts' : posts, 'related_posts' : related_posts })

def contact(request):
    return render(request, 'contact.html')

def old_url_redirect (request):
    return redirect(reverse('blog:new_url_usingname'))  

def new_url(request):
    return HttpResponse("Redirect successfully") 

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration Successful. You can login now.')
            return redirect("blog:login")

            print('register success')
        else:
            print('register failed')

    return render(request, 'register.html',{'form' : form})


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                print("Login success")
                messages.success(request, f'Welcome back, {user.username}! You have successfully logged in.')
                return redirect("blog:dashboard")
            
    return render(request, 'login.html',{'form' : form})

def dashboard(request):
    #getting post details
    all_posts = Post.objects.filter(user=request.user)

    #pagination 
    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html',{'all_posts' : all_posts, 'page_obj' : page_obj})

def logout(request):
    auth_logout(request)
    messages.success(request, 'logout success')
    return redirect("blog:index")

def new_post(request):
    categories = Category.objects.all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:dashboard')

    return render(request, 'new_post.html', {'categories' : categories, 'form' : form})