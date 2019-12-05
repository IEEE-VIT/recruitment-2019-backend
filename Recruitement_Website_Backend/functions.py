import json as jsonparse

import requests
from rest_framework.response import Response


def send_email_to_candidate(candidate_email, subject, mail_body):
    try:
        mail_url = 'https://justanothersender.herokuapp.com/sendEmailsExternal'
        r = requests.post(
            url=mail_url,
            json=jsonparse.dumps(
                {"email": [candidate_email],
                 "html": mail_body,
                 "subject": subject,
                 "sender": "noreply@ieeevit.com",
                 "nameOfEmail": "IEEE-VIT Recruitment 2019",
                 "secret": "RealDevilIsWithIn"
                 }
            )
        )
        print(r)
        if r.status_code == 200:
            print(r.content)
            return Response({'detail': "Email has been sent to candidate"}, status=200)
        else:
            print(r.content)
            return Response({'message': "Email could not been sent to candidate"}, status=400)
    except Exception as e:
        print(f"Couldn't send email to candidate function. Error: {e}")
        return Response({'detail': 'Email is Invalid. We recommend deleting the candidate'}, status=400)
