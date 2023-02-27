from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from front.forms import NewUserForm
from perso.models import Perso, SaveDocument, AskTalkPerso, SaveAsk, HistoryAskTalkPerso


# Create your views here.
def base(request):
    all_perso = Perso.objects.filter(user=None)
    if request.user.is_authenticated:
        try:
            perso = Perso.objects.get(user=request.user)
        except Perso.DoesNotExist:
            perso = None
    else:
        perso = None
        return redirect('/login/')
    return render(template_name="base.html", request=request, context={"perso": perso, "all_perso": all_perso})


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


def custom_save(talk_perso, perso):
    save_document = SaveDocument.objects.get_or_create(name="Document de " + perso.name)
    for secret in talk_perso.secrets.all():
        save_document[0].secrets.add(secret)
        save_document[0].save()
        s_d_def = SaveDocument.objects.get(id=save_document[0].id)
        perso.saveDocument = s_d_def
        perso.save()


def saveAskPerso(request, perso_ask, pk):
    perso = Perso.objects.get(user=request.user)
    talk_perso = Perso.objects.get(id=perso_ask)
    custom_save(talk_perso, perso)
    instance = AskTalkPerso.objects.get(id=pk)
    user_join = instance.join_perso.user
    user_ask = instance.user
    perso_join = Perso.objects.get(user=user_join)
    custom_save(talk_perso, perso_join)
    instance.delete()
    save_ask_join = SaveAsk.objects.get_or_create(user=user_join)
    comp = save_ask_join[0].compte
    save_ask_join[0].compte = comp + 1
    save_ask_join[0].save()
    save_ask = SaveAsk.objects.get_or_create(user=user_ask)
    comp = save_ask[0].compte
    save_ask[0].compte = comp + 1
    save_ask[0].save()
    return redirect('/account')


def askTalkPerso(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            perso_ask = Perso.objects.get(id=pk)
            perso = Perso.objects.get(user=request.user)
            ask_perso = AskTalkPerso.objects.get_or_create(user=request.user, perso_ask=perso_ask, perso=perso)
            HistoryAskTalkPerso.objects.get_or_create(user=request.user, perso_ask=perso_ask, perso=perso)

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

            if ask_perso.join_perso is not None and ask_perso.join_perso.user == request.user:
                ask_perso.join_perso = None
                ask_perso.save()
            else:
                ask_perso.join_perso = perso
                ask_perso.save()
                HistoryAskTalkPerso.objects.get_or_create(user=ask_perso.user, perso_ask=ask_perso.perso_ask,
                                                          perso=ask_perso.perso, join_perso=perso)

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'chat_{ask_perso.perso.slug_name}',
                    {
                        'type': 'chat_message',
                        'message': f"{perso.name} veut rejoindre le clash du frigo"
                    }
                )
            return redirect('/guilty')
    else:
        return redirect('/')


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        perso_name = request.POST.get('slug_name')
        # envoyer un message sur la websocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{perso_name}',
            {
                'type': 'chat_message',
                'message': message
            }
        )
        # return json response
        return JsonResponse({'message': message})


def accept_clash(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            perso = Perso.objects.get(user=request.user)
            clash = AskTalkPerso.objects.get(id=pk)
            if clash.join_perso is None:
                return redirect('/clash')
            else:
                saveAskPerso(request, clash.perso_ask.id, clash.id)
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'chat_{clash.join_perso.slug_name}',
                    {
                        'type': 'chat_message',
                        'message': f"{perso.name} à accepté que vous participiez au clash !"
                    }
                )

            return redirect('/account')
        else:
            return redirect('/login')
    else:
        return redirect('/guilty')


def cancel_clash(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            perso = Perso.objects.get(user=request.user)
            clash = AskTalkPerso.objects.get(id=pk)
            if clash.join_perso:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'chat_{clash.join_perso.slug_name}',
                    {
                        'type': 'chat_message',
                        'message': f"{perso.name} à annuler le clash contre {clash.perso_ask.name} !"
                    }
                )
                clash.delete()
            else:
                clash.delete()

            return redirect('/clash')
        else:
            return redirect('/login')
    else:
        return redirect('/guilty')


def refuse_clash(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            perso = Perso.objects.get(user=request.user)
            clash = AskTalkPerso.objects.get(id=pk)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{clash.join_perso.slug_name}',
                {
                    'type': 'chat_message',
                    'message': f"{perso.name} à refuser que vous rejoignez le clash contre {clash.perso_ask.name} !"
                }
            )
            clash.join_perso = None
            clash.save()
            return redirect('/clash')
        else:
            return redirect('/login')
    else:
        return redirect('/guilty')


def clash(request):
    if request.user.is_authenticated:
        perso = Perso.objects.get(user=request.user)
        clash = AskTalkPerso.objects.filter(user=request.user)
        return render(request=request, template_name="userAccount/clash.html", context={"clash": clash, "perso": perso})
    else:
        return redirect('/')


def logout_request(request):
    logout(request)
    return redirect('/')


def history(request):
    if request.user.is_authenticated:
        perso = Perso.objects.get(user=request.user)
        history = HistoryAskTalkPerso.objects.filter(Q(user=request.user) | Q(join_perso=perso))
        return render(request=request, template_name="userAccount/history.html",
                      context={"history": history, "perso": perso})
    else:
        return redirect('/')

def all(request):
    if request.user.is_authenticated:
        perso = Perso.objects.all().exclude(user=request.user)
        save_ask = SaveAsk.objects.get_or_create(user=request.user)

        return render(request=request, template_name="perso/all.html", context={"save_ask": save_ask[0], "persos": perso})
    else:
        return redirect('/')

def select_perso(request, pk):
    if request.user.is_authenticated:
        perso = Perso.objects.get(id=pk)
        perso.user = request.user
        perso.save()
        return redirect('/')
    else:
        return redirect('/')