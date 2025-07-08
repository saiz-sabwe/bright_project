import requests


def send_push_notification(external_ids: list, message: str, data: dict):
    url = "https://onesignal.com/api/v1/notifications"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Basic os_v2_app_xrfcceombbcwfdezh7mgr3ss4ebbxqxz6c5elp4aek6gu7f3yt6qak2fu33vmbjbsrxq44tvnmhq5wrs5cja5av7oy42m65k5ldsaly"
    }

    payload = {
        "app_id": "bc4a2111-cc08-4562-8c99-3fd868ee52e1",
        "target_channel": "push",
        "headings": {
            "en": "Tempo"
        },
        "contents": {
            "en": message
        },
        "include_aliases": {
            "external_id": external_ids
        },
        "data": data
    }

    response = requests.post(url, json=payload, headers=headers)

    # Gestion de la réponse
    if response.status_code == 200:
        print("Notification envoyée avec succès !")
    else:
        print(f"Erreur lors de l'envoi : {response.status_code}")
        print(response.json())
