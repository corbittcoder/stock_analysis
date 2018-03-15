import boto3
import json

def print_j(entity):
	print(json.dumps(entity, indent=4, sort_keys=True))

def is_neg(num):
	if num < 0:
		return True
	return False

def get_percent_change(start, end):
	difference = end - start
	percent_change = difference / start
	return percent_change * 100
