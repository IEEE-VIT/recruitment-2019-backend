import json

import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from questions.models import Question
from questions.serializers import QuestionSerializer


@action(methods=['GET'], detail=False, url_path='questions', serializer_class=QuestionSerializer)
@permission_classes(AllowAny)
@csrf_exempt
def question(self):
	questions = []
	rand_question_id = np.random.randint(1, 5, 2)
	print(rand_question_id)
	for i in rand_question_id:
		print(Question.objects.filter(question_id=i).first().question)
		questions.append(Question.objects.filter(question_id=i).first().question)
	print(questions)
	return JsonResponse( {"questions": questions}, status=200)