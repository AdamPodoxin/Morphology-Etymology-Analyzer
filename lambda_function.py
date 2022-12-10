import json
from main import analyze

def lambda_handler(event, context):
	word = event['rawQueryString']
	response = analyze(word)

	return {
		'statusCode': 200,
		'body': response
	}