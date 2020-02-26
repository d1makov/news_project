from .tasks import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages
from .models import CustomUser
from .tokens import account_activation_token
# from django.db.models import signals


def signup(request):
    form = CustomUserCreationForm()
    template_name = 'signup.html'
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            group = Group.objects.get(name='Users')
            user.groups.add(group)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email, ])
            # send_mail.delay(mail_subject, message, settings.EMAIL_HOST_USER, [to_email, ])
            return HttpResponse('Please confirm your email address to complete the registration')
    return render(request, template_name, {"form": form})


def signin(request):
    form = CustomUserLoginForm()
    template_name = 'signin.html'
    if request.method == "POST":
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            get_email = form.cleaned_data['email']
            get_password = form.cleaned_data['password']
            user = authenticate(email=get_email, password=get_password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "You are not registered!")
                return redirect('signup')
    return render(request, template_name, {'form': form})


def signout(request):
    logout(request)
    return redirect(reverse_lazy('home'))


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# signals.post_save.connect(signup, sender=CustomUser)