import json

import requests
from rest_framework.response import Response


def send_email_to_candidate(self, candidate_email, subject, body, sender_email, *args, **kwargs):
    try:
        mail_url = 'https://justanothersender.herokuapp.com/sendEmailsExternal'
        r = requests.post(
            url=mail_url,
            body=None,
            json=json.dumps(
                {
                    "email": candidate_email,
                    "html": body,
                    "subject": subject,
                    "sender": sender_email,
                    "nameOfEmail": "IEEE-VIT Recruitments 2019",
                    "secret": "RealDevillsWithIn"
                }
            )
        )
        if r.status_code == 200:
            print(r.content)
            return Response({'detail': "Email has been sent to candidate"}, status=200)
        else:
            print(r.content)
            return Response({'message': "Email could not been sent to candidate"}, status=400)
    except Exception as e:
        print(f"Couldn't send email to candidate function. Error: {e}")
        return Response({'detail': 'Email is Invalid. We recommend deleting the candidate'}, status=400)