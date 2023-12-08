from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
#from gtts.tts import gTTS
#from gTTS.templatetags.gTTS import say
# Create your views here.

openai_api_key = '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'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es Michel de Montaigne. Ton objectif est de sensibiliser l'utisateur au déreglement climatique de manière bienveillante et pédagogue. Tes réponses devront faire moins de 100 mots. Tu devras fournir à l'utilisateur des liens vers des sites contenant des informations pertinentes"},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer

def chatbot(request):
    try:
        chats = Chat.objects.filter(user=request.user)
    
        if request.method == 'POST':
            message = request.POST.get('message')
            #response = 'Salut, voici ma réponse'
            response = ask_openai(message)
            #obj = say(language='FR', text=response)
            #obj = gTTS(text='test', lang='fr', slow=False)
            #obj.save('test.mp3')
            chat = Chat(user=request.user, message = message, response = response, created_at = timezone.now())
            chat.save()
            return JsonResponse({'message' : message, 'response' : response})
        return render(request, 'chatbot.html', {'chats' : chats})
    except:
        if request.method == 'POST':
            message = request.POST.get('message')
            return JsonResponse({'message' : message, 'response' : "Veuillez vous connecter"})
        error_message = "Problème de connexion"
        return render(request, 'chatbot.html', {'error_message' : error_message})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Pseudo ou Mot de Passe invalide'
            return render(request, 'login.html', {'error_message' : error_message})
    else:
        return render(request, 'login.html')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = "Erreur lors de la création du compte"
            return render(request, 'register.html', {'error_message' : error_message})
        else:
            error_message = "Les mots de passes sont différents"
            return render(request, 'register.html', {'error_message' : error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def ressources(request):
    return render(request, 'ressources.html')
