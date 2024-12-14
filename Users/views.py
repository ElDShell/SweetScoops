from .models import Profile,User
from .forms import CustomerCreationForm
from utils import get_object_from_signed_url
from itsdangerous import URLSafeSerializer,BadSignature
from django.http import Http404
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import DetailView,UpdateView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin




# User authentication (login,logout,register...etc) Views
class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    
    def form_invalid(self, form):
        if form.errors:
            messages.error(self.request,f"{form.non_field_errors()}")     
        response = super().form_invalid(form)
        return redirect('login')
        
class logout(LogoutView):
    template_name = None

class UserCreateView(CreateView):
    model = User
    form_class = CustomerCreationForm
    template_name = "login.html"
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        messages.success(self.request, 'Your account has been successfully created! Please log in to continue.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if 'email' in form.errors:
            messages.error(self.request, f'There was an issue with your email address. Please ensure it is valid.')
        elif 'username' in form.errors:
            messages.error(self.request, 'Your username is invalid. Please choose a different one.')
        elif 'password1' in form.errors:
            messages.error(self.request, 'Your password is too weak. Please choose a stronger password.')
        elif 'password2' in form.errors:
            messages.error(self.request, 'Your passwords do not match. Please confirm your password correctly.')
        elif form.errors:
            messages.error(self.request, f'{form.non_field_errors()}')

        return redirect(self.success_url)    
    
## User profile Views
class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = "profile.html"
    context_object_name = 'profile'
    
    def get_object(self):
        try:
            profile = Profile.objects.get(slug=self.kwargs['slug'])
            return profile
        except Profile.DoesNotExist:
            raise Http404("Profile not found")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        
        user = profile.user  
        context['signed_url'] = user.genrate_signed_url()  
        
        return context

    
class ProfileImageUpdateView(LoginRequiredMixin,UpdateView):
    model = Profile
    fields = ('image',)
    template_name = None
    
    def get_object(self, queryset = None):
        profile = super().get_object(queryset)
        if profile.user != self.request.user:
            raise PermissionDenied('You are not allowed to update this profile')
        return profile
    
    def form_valid(self, form):
        profile = form.save(commit=False)
        profile_img = self.request.FILES.get('profile_img')  
        if profile_img:
            # Remove old image if it exists
            old_image = profile.image
            if old_image:
                old_image.delete(save=False)
            profile.image = profile_img
        profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})

class ProfilePhoneUpdateView(LoginRequiredMixin,UpdateView):
    model = Profile
    template_name = None
    fields = ['phone_number']
    
    def get_object(self, queryset = None):
        profile = super().get_object(queryset)
        if profile.user != self.request.user:
            raise PermissionDenied('You are not allowed to update this profile')
        return profile
    
    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please check the input fields.")
        return redirect('profile_detail', slug=self.get_object().profile.slug)
    
    def get_success_url(self):
        profile = self.get_object()
        return reverse_lazy('profile_detail',kwargs={'slug':profile.slug})

## User Views 
class UserFullNameUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    template_name = None
    fields = ['first_name','last_name',]
    
    def get_object(self, queryset = ...):

        user = get_object_from_signed_url(self.kwargs['signed_url'],User)

        if user != self.request.user:
            raise PermissionDenied('Your are not allowed to update this user')
        return user   
    
    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please check the input fields.")
        return redirect('profile_detail', slug=self.get_object().profile.slug)
    
    def get_success_url(self):
        profile = self.get_object().profile
        return reverse_lazy('profile_detail',args=[profile.slug]) 

class UserEmailUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    template_name = None
    fields = ['email']
    
    def get_object(self, queryset = ...):

        user = get_object_from_signed_url(self.kwargs['signed_url'],User)

        if user != self.request.user:
            raise PermissionDenied('Your are not allowed to update this user')
        return user   
    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please check the input fields.")
        return redirect('profile_detail', slug=self.get_object().profile.slug)
    
    def get_success_url(self):
        profile = self.get_object().profile
        return reverse_lazy('profile_detail',args=[profile.slug]) 
    
class UserAddressUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    template_name = None
    fields = ['address']
    
    def get_object(self, queryset = ...):
        user = get_object_from_signed_url(self.kwargs['signed_url'],User)
        if user != self.request.user:
            raise PermissionDenied('You are not allowed to update this user')
        return user
    
    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please check the input fields.")
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        profile = self.get_object().profile
        return reverse_lazy('profile_detail', kwargs={'slug': profile.slug})
    

