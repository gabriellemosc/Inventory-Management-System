from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_mode_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'admin':
            # Mensagem que vai aparecer como toast
            messages.error(request, "Você precisa estar no modo ADMIN para acessar essa página!")
            return redirect('homepage')
        return view_func(request, *args, **kwargs)
    return wrapper
