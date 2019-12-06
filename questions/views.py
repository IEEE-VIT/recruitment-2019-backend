import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from questions.models import Question
from questions.serializers import QuestionSerializer


@action(methods=['GET'], detail=False, url_path='questions', serializer_class=QuestionSerializer)
@permission_classes(AllowAny)
@csrf_exempt
def questions(self):
	questions = []
	rand_question_id = random.sample(range(1, 5), 3)
	for i in rand_question_id:
		question = Question.objects.filter(question_id=i).values()
		questions.append(list(question))

	return JsonResponse({'questions': questions}, status=200)

@csrf_exempt
def get_question(request, pk):

	try:
		question = Question.objects.get(pk=pk)
	except Question.DoesNotExist:
		return Response({'Detail': 'Question not found'}, status=404)

	if request.method == 'GET':
		serializer = QuestionSerializer(question)
		return JsonResponse(serializer.data)