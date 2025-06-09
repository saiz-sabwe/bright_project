from django.utils.timezone import now
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Agent, Presence
from .serializers import AgentSerializer, PresenceSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def api_liste_agents(request):
    agents = Agent.objects.all()
    serializer = AgentSerializer(agents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_liste_presences(request):
    presences = Presence.objects.select_related('agent').all()
    serializer = PresenceSerializer(presences, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def verifier_agent_par_matricule(request, matricule):
    try:
        agent = Agent.objects.get(matricule=matricule)
        serializer = AgentSerializer(agent, context={'request': request})
        return Response({
            "success": True,
            "message": "Agent reconnu.",
            "agent": serializer.data
        })
    except Agent.DoesNotExist:
        return Response({
            "success": False,
            "message": "❌ Matricule invalide ou agent introuvable."
        }, status=404)

@api_view(['POST'])
@permission_classes([AllowAny])
def enregistrer_presence(request):
    matricule = request.data.get('matricule')

    if not matricule:
        return Response({
            "success": False,
            "message": "Le matricule est requis."
        }, status=400)

    try:
        agent = Agent.objects.get(matricule=matricule)
    except Agent.DoesNotExist:
        return Response({
            "success": False,
            "message": "Agent introuvable."
        }, status=404)

    date_du_jour = now().date()
    heure_actuelle = now().time()

    presence, created = Presence.objects.get_or_create(
        agent=agent,
        date=date_du_jour,
        defaults={'heure_arrivee': heure_actuelle}
    )

    if not created:
        if presence.heure_depart is None:
            presence.heure_depart = heure_actuelle
            presence.save()
            message = "Heure de départ enregistrée."
        else:
            message = "Présence déjà enregistrée pour aujourd'hui."
    else:
        message = "Heure d'arrivée enregistrée."

    agent_data = AgentSerializer(agent, context={'request': request}).data

    return Response({
        "success": True,
        "message": message,
        "agent": agent_data,
        "presence": {
            "date": str(date_du_jour),
            "heure_arrivee": str(presence.heure_arrivee) if presence.heure_arrivee else None,
            "heure_depart": str(presence.heure_depart) if presence.heure_depart else None,
        }
    })