from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from BRIGHT_NODE.module.module_requete import send_push_notification
from ModuleProfil.models import Model_Profil
from ModuleServices.models import Model_Demande


@receiver(post_save,sender=Model_Demande)
def Post_Model_Demande(sender,instance,created, **kwargs):

    print("********* Post_Model_Demande*************")
    print('--------- instance : ', instance)
    try:

        message = instance.get_message_statut()

        profil = instance.profil
        uuid_requester = profil.uuid

        list_receiver = [uuid_requester]

        list_receiver_staff = [profil.uuid for profil in Model_Profil.get_staff_profiles()]

        list_receiver += list_receiver_staff

        v = send_push_notification(
            external_ids = list_receiver,
            message=message,
            data={}
        )
    except Exception as e:
        print("-----erreur Post_Model_Demande:", e)