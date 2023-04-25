from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from apps.accounts.models import UserSettingsForm, MyUser


# Create your views here.

@login_required(login_url="login/")
def edit_profile_settings(request):
    user = get_object_or_404(MyUser, id=request.user.id)

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserSettingsForm(instance=user)

    return render(request, 'home/page-user.html', {'form': form, 'user': request.user})



#KAZDY TASK I TAK MA INNE ID WIEC SHOW ZROBIC NOWE