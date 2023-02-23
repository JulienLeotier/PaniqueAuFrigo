from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from front.forms import NewUserForm
from perso.models import Perso, SaveDocument, AskTalkPerso, SaveAsk


# Create your views here.
def base(request):
    return render(template_name="base.html", request=request)


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(template_name="connexion/login.html", request=request, context={"form": form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('/')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="connexion/register.html", context={"register_form": form})


def account(request):
    if request.user.is_authenticated:
        perso = Perso.objects.get(user=request.user)
        other_perso = Perso.objects.exclude(user=request.user)
        save_ask = SaveAsk.objects.get_or_create(user=request.user)
        return render(request=request, template_name="userAccount/account.html",
                      context={"perso": perso, "other_perso": other_perso, "save_ask": save_ask[0]})
    else:
        return redirect('/')


def saveAskPerso(request, perso_ask, pk):
    perso = Perso.objects.get(user=request.user)
    talkPerso = Perso.objects.get(id=perso_ask)
    save_document = SaveDocument.objects.get_or_create(name="Document de " + perso.name)
    for secret in talkPerso.secrets.all():
        save_document[0].secrets.add(secret)
        save_document[0].save()
        s_d_def = SaveDocument.objects.get(id=save_document[0].id)
        perso.saveDocument = s_d_def
        perso.save()
    instance = AskTalkPerso.objects.get(id=pk)
    user_join = instance.join_perso.user
    user_ask = instance.user
    perso_join = Perso.objects.get(user=user_ask)
    save_document_join = SaveDocument.objects.get_or_create(name="Document de " + perso_join.name)
    for secret in talkPerso.secrets.all():
        save_document_join[0].secrets.add(secret)
        save_document_join[0].save()
        s_d_def = SaveDocument.objects.get(id=save_document[0].id)
        perso_join.saveDocument = s_d_def
        perso_join.save()
    instance.delete()
    save_ask_join = SaveAsk.objects.get_or_create(user=user_join)
    compt = save_ask_join[0].compte
    save_ask_join[0].compte = compt + 1
    save_ask_join[0].save()
    save_ask = SaveAsk.objects.get_or_create(user=user_ask)
    compt = save_ask[0].compte
    save_ask[0].compte = compt + 1
    save_ask[0].save()
    return redirect('/account')


def askTalkPerso(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            perso_ask = Perso.objects.get(id=pk)
            perso = Perso.objects.get(user=request.user)
            ask_perso = AskTalkPerso.objects.get_or_create(user=request.user, perso_ask=perso_ask, perso=perso)
            if ask_perso[0].join_perso is None:
                return redirect('/guilty')
            else:
                saveAskPerso(request, ask_perso.perso_ask.id, ask_perso.id)
        else:
            return redirect('/login')
    else:
        return redirect('/guilty')


def guilty(request):
    if request.user.is_authenticated:
        ask_perso = AskTalkPerso.objects.all()
        save_ask = SaveAsk.objects.get_or_create(user=request.user)
        perso = Perso.objects.get(user=request.user)
        return render(request=request, template_name="userAccount/guilty.html",
                      context={"perso": perso, "ask_perso": ask_perso, "save_ask": save_ask[0]})
    else:
        return redirect('/')


def joinAskTalkPerso(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            perso = Perso.objects.get(user=request.user)
            ask_perso = AskTalkPerso.objects.get(id=pk)
            ask_perso.join_perso = perso
            ask_perso.save()
            saveAskPerso(request, ask_perso.perso_ask.id, pk)
        return redirect('/account')
    else:
        return redirect('/')
