from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

from ModuleProfil.models import Model_Profil
from ModuleServices.models import Model_Demande


@receiver(post_save,sender=Model_Profil)
def Post_Model_Profil(sender,instance,created, **kwargs):

    print("********* Post_Model_Profil*************")
    print('--------- instance : ', instance)
    if created:
        try:
            generated_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, f"{instance.id}")
            instance.uuid = str(generated_uuid)
            instance.save(update_fields=["uuid"])
        except Exception as e:
            print("-----erreur Post_Model_Profil:", e)