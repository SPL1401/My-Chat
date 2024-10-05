from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
import json
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def getToken(req):
    appId = 'ff0e14622ec349fd879af3e5e5028db9'
    appCertificate = '43aaef9010ed454f97ed4f25cc5df836'
    channelName = req.GET.get('channel')
    uid = random.randint(1,230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid}, safe=False)
def lobby(req):
    return render(req,'project1/lobby.html')
def room(req):
    return render(req,'project1/room.html')

@csrf_exempt
def createMember(req):
    data = json.loads(req.body)
    member, created =RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    return JsonResponse({'name':data['name']}, safe=False)

def getMember(req):
    uid = req.GET.get('UID')
    room_name = req.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,

    )
    name = member.name
    return JsonResponse({'name':member.name},safe=False)

@csrf_exempt
def deleteMember(req):
    data = json.loads(req.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name'],
    )
    member.delete()
    return JsonResponse('Member was deleted', safe=False)