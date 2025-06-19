from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.http import HttpResponse



class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # désactiver le compte jusqu’à validation
        user.save()

        # Création du lien d'activation
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        domain = get_current_site(self.request).domain
        link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        activate_url = f"http://{domain}{link}"

        send_mail(
            'Active ton compte SmartBiz',
            f"Clique ici pour activer ton compte : {activate_url}",
            'noreply@smartbiz.com',
            [user.email],
            fail_silently=False,
        )
        return redirect('login')


def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    return HttpResponse('Activation invalide', status=400)


