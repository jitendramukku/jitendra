from multiprocessing.dummy.connection import families
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, Http404, HttpResponse
from inventory.config import *
from thingstodo.models import ThingsToDoCategory, ThingsToDoSubCategory, ThingsToDoGroups, ThingsToDoGroupsCategory, LangaugeMaster
from collections import OrderedDict
import json
from rehlat.settings import MEDIA_ROOT, b2c_admin_url, MEDIA_URL, env_type
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.contrib import messages
import os
import traceback
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
import json
from bson import json_util
from datetime import datetime
import string
import random
from slugify import slugify
import pandas as pd
import math
from pathlib import Path
import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import re
import csv



def upload_ttd_image(image_file, ttd_id):
	try:
		ttd_details = ttd_collection.find_one({'things_todo_id':ttd_id},{'address_details.en.city':1, 'address_details.en.country':1, 'title_description.en.name':1,'city_id':1})
		# image_file = request.FILES.get('file')
		city_name = ttd_details.get('address_details').get('en').get('city')
		if city_name : city_name = city_name.lower().replace(' ','_')
		if not city_name:
			city_name = ttd_details.get('address_details').get('en').get('country').lower().replace(' ','_')
		city_id = ttd_details.get('city_id')
		
		place_name = ttd_details.get('title_description').get('en').get('name').lower()
		place_name = slugify(place_name).replace('-','_')
		image_url = MEDIA_URL+""
		# dest_id = request.POST.get('id')
		image_path = MEDIA_ROOT + '/searchdestination/' + \
			'thingstodo/images/{city_name}/{place_name}/'.format(city_name=city_name,place_name=place_name)
		if not os.path.exists(image_path):
			os.makedirs(image_path)
		data = image_file.read()
		image_name = image_file.name
		image_name = image_name.replace(" ","_")
		suffix = Path(image_file.name).suffix

		if suffix == ".webp":
			image_url = image_path+""+image_name
			default_storage.save(image_url, image_file)
		else:
			new_file_name = str(Path(image_file.name).with_suffix('.webp'))
			image = Image.open(image_file.file)
			thumb_io = io.BytesIO()
			image.save(thumb_io,"webp",optimize=True,quality=95)
			field_name = image_file.field_name if image_file.field_name else 'file'
			new_f_object = InMemoryUploadedFile(thumb_io,field_name,new_file_name,image_file.size,image_file.charset,image_file.content_type_extra)
			image_name = image_name.split('.')[0:-1]
			image_name = ''.join(image_name) + '.webp'
			image_url = image_path + image_name
			default_storage.save(image_url,new_f_object)
		new_img = Image.open(image_url)
		
		img_sizes = [(1920,'large_'),(285,'thumbnail_')]
		for val in img_sizes:
			base_width = val[0]
			width_percent = (base_width / float(new_img.size[0]))
			hsize = int((float(new_img.size[1]) * float(width_percent)))
			resized_image = new_img.resize((base_width,hsize),Image.ANTIALIAS)
			file_name = image_path + val[1] + image_name
			resized_image.save(file_name)
			os.chmod(file_name, 0777)
		
		image_url = MEDIA_URL + 'searchdestination/' + \
			'thingstodo/images/{city_name}/{place_name}/{img_name}'.format(city_name=city_name,place_name=place_name,img_name=image_name)
		os.chmod(image_path+image_name, 0777)
		if env_type == "live":
			image_url = "https://htccadmin.rehlat.com"+image_url
		elif env_type == 'stage':
			image_url = "http://stageb2cadminhtl.rehlat.ae"+image_url
		else:
			image_url = 'http://127.0.0.1:8000'+image_url
			
		print('return final path:',image_url)
		return {"path": image_url, "status": True}
	except:
		print(traceback.format_exc())
		return {"status": False}



def upload_image(image_file, ttd_id):
	try:
		ttd_details = ttd_collection.find_one({'things_todo_id':ttd_id},{'address_details.en.city':1, 'address_details.en.country':1, 'title_description.en.name':1,'city_id':1})
		# image_file = request.FILES.get('file')
		city_name = ttd_details.get('address_details').get('en').get('city')
		if city_name : city_name = city_name.lower().replace(' ','_')
		if not city_name:
			city_name = ttd_details.get('address_details').get('en').get('country').lower().replace(' ','_')
		city_id = ttd_details.get('city_id')
		# if not city_name:
		# 	city = ttd_collection.find_one({'city_id': city_id,'tripadvisor_city_name':{'$ne':''}},{'tripadvisor_city_name':1})
		# 	city_name = city.get('tripadvisor_city_name')
		# 	if not city_name:
		# 		city = city_col.find_one({'_id': city_id},{'city'})
		# 		city_name = city.get('city')  
		place_name = ttd_details.get('title_description').get('en').get('name').lower()
		place_name = slugify(place_name).replace('-','_')
		image_url = MEDIA_URL+""
		# dest_id = request.POST.get('id')
		image_path = MEDIA_ROOT + '/searchdestination/' + \
			'thingstodo/images/{city_name}/{place_name}/'.format(city_name=city_name,place_name=place_name)
		if not os.path.exists(image_path):
			os.makedirs(image_path)
		data = image_file.read()
		image_name = image_file.name
		image_name = image_name.replace(" ","_")
		suffix = Path(image_file.name).suffix

		if suffix == ".webp":
			image_url = image_path+""+image_name
			default_storage.save(image_url, image_file)
		else:
			new_file_name = str(Path(image_file.name).with_suffix('.webp'))
			image = Image.open(image_file.file)
			thumb_io = io.BytesIO()
			image.save(thumb_io,"webp",optimize=True,quality=95)
			field_name = image_file.field_name if image_file.field_name else 'file'
			new_f_object = InMemoryUploadedFile(thumb_io,field_name,new_file_name,image_file.size,image_file.charset,image_file.content_type_extra)
			image_name = image_name.split('.')[0:-1]
			image_name = ''.join(image_name) + '.webp'
			image_url = image_path + image_name
			default_storage.save(image_url,new_f_object)
		# image_url = image_path+"/"+image
		# default_storage.save(image_url, image_file)
		
		image_url = MEDIA_URL + 'searchdestination/' + \
			'thingstodo/images/{city_name}/{place_name}/{img_name}'.format(city_name=city_name,place_name=place_name,img_name=image_name)
		os.chmod(image_path+image_name, 0777)
		if env_type == "live":
			image_url = "https://htccadmin.rehlat.com"+image_url
		elif env_type == 'stage':
			image_url = "http://stageb2cadminhtl.rehlat.ae"+image_url
		else:
			image_url = 'http://127.0.0.1:8000'+image_url
			
		print('return final path:',image_url)
		return {"path": image_url, "status": True}
	except:
		print(traceback.format_exc())
		return {"status": False}


def get_state_list():

	result_list = []
	obj = state_col.find({},{'_id','state'})
	for doc in obj:
		t = (doc['_id'],doc['state'])
		result_list.append(t)

	return result_list


def get_country_list():

	result_list = []
	obj = country_col.find({},{'_id','name'})
	for doc in obj:
		t = (doc['_id'],doc['name'])
		result_list.append(t)

	return result_list


def add_thingstodo(request):
	if request.session.get('name') is not None:
		username = request.session.get('name')
		if request.method=='POST':
			
			fdata=request.POST
			print(fdata)
			
			# letters = string.digits + string.ascii_uppercase+string.ascii_lowercase
			letters = string.digits + string.ascii_lowercase + string.digits + string.ascii_lowercase
			id = ''.join(random.choice(letters) for i in range(10)) 

			cityid = int(fdata.get('cityid')) if fdata.get('cityid') else None
			area_id = int(fdata.get('areaid')) if fdata.get('areaid') else None
			country_id = int(fdata.get('countryid')) if fdata.get('countryid') else None
			ttd_type = str(fdata.get('ttd_type'))
			place_name = str(fdata.get('place_name'))
			
			if cityid == None and ttd_type == 'CITY':
				messages.error(request, "Please enter a valid City")
				return render(request, 'thingstodo/add_thingstodo.html')
			elif country_id == None and ttd_type == 'COUNTRY':
				messages.error(request, "Please enter a valid Country")
				return render(request,'thingstodo/add_thingstodo.html')

			stateid = "" #int(fdata.get('stateid')) if fdata.get('stateid') else None -- for now we are not adding state
			# country_id = city_country_dict.get("country_id")

			searchdest_id = ''
			city_country_dict = dict()
			if ttd_type == "CITY":
				city_country_dict = city_col.find_one({'_id':cityid},{'_id':1,'city':1,'country':1,'city_ar':1,'country_ar':1,"country_id":1})
				searchdest_id = search_destination.find_one({'city_id':{'$exists':True, '$eq':cityid}}, {'_id':0, "id":1})
			else:
				searchdest_id = search_destination.find_one({'country_id':{'$exists':True, '$eq':cityid}}, {'_id':0, "id":1})
			
			if stateid:
				state_dict=state_col.find_one({'_id':stateid},{'_id':0,'state':1})
			else:
				state_dict = {}
			country_details = country_col.find_one({'_id':country_id}, {'_id':1, "alpha_2_code":1,'country':1,'country_ar':1})            
			explore_url_text = '{}-{}-{}'.format(place_name, city_country_dict.get("city"), country_details.get("country"))
			explore_url = slugify(explore_url_text) if explore_url_text else ''
			new_record={
			'things_todo_id':id,
			'city_id':cityid,
			'ID':{'r_province_id':stateid,'r_area_id':area_id,'location_id':fdata.get('location_id'),
				'r_city_id':cityid,'r_country_id':country_id},
			'country_id':country_id,
			'address_details':{'en':{'website':"",'street1':"",'street2':"",'address_string':"",'phone':"",'postal_code':"",
									'timezone':"",'city':city_country_dict.get('city'),'country':country_details.get('country'),
									'longitude':"",'latitude':"",'state':state_dict.get("state"),'email':""},
							'fr':{'street1':"",'street2':"",'address_string':"",
									'city':"",'country':"",
									'state':""},
							'ar':{'street1':"",'street2':"",'address_string':"",
									'city':city_country_dict.get('city_ar'),'country':country_details.get('country_ar'),
									'state':state_dict.get("state")}},
			'subcategory':{'en':[],'fr':[],'ar':[]},
			'rating':{'rating':"",'review_rating_count':{'1':"",'2':"",'3':"",'4':"",'5':""},'num_of_reviews':"",'rating_image_url':""},
			'tripadvisor_id':"",
			'tripadvisor_rank':"",
			'ancestors':{'en':{'province':{"location_id":"","name":""},'city':{"location_id":"","name":""},'country':{"location_id":"","name":""},'region':{"location_id":"","name":""},'municipality':{"location_id":"","name":""},'state':{"location_id":"","name":""}},
						'fr':{'province':{"location_id":"","name":""},'city':{"location_id":"","name":""},'country':{"location_id":"","name":""},'region':{"location_id":"","name":""},'municipality':{"location_id":"","name":""},'state':{"location_id":"","name":""}},
						'ar':{'province':{"location_id":"","name":""},'city':{"location_id":"","name":""},'country':{"location_id":"","name":""},'region':{"location_id":"","name":""},'municipality':{"location_id":"","name":""},'state':{"location_id":"","name":""}}},
			'search_destination_id':"",
			'open_close':{'sunday':[{'close':"",'open':"",'isopen':0,'is24hours':0}],'monday':[{'close':"",'open':"",'isopen':0,'is24hours':0}],'tuesday':[{'close':"",'open':"",'isopen':0,'is24hours':0}],'wednesday':[{'close':"",'open':"",'isopen':0,'is24hours':0}],'thursday':[{'close':"",'open':"",'isopen':0,'is24hours':0}],'friday':[{'close':"",'open':"",'isopen':0,'is24hours':0}],'saturday':[{'close':"",'open':"",'isopen':0,'is24hours':0}]},
			'is_timing_available':0,
			'neighbourhood_info':{'en':[],'fr':[],'ar':[]},
			'trip_types':{'en':[],'fr':[],'ar':[]},
			'category':{'en':{},'fr':{},'ar':{}},
			'ranking_data':{'en':{'ranking_string':"",'ranking':"",'geo_location_id':"",'geo_location_name':"",'ranking_out_of':""},
							'fr':{'ranking_string':"",'ranking':"",'geo_location_id':"",'geo_location_name':"",'ranking_out_of':""},
							'ar':{'ranking_string':"",'ranking':"",'geo_location_id':"",'geo_location_name':"",'ranking_out_of':""}},
			'is_active':1,
			'groups':{'en':{},'fr':{},'ar':{}},
			'prices':{'book_now_url':"",'r_booking_note':"",'r_ticket_prices':"",'r_entry_ticket':"",'vendor_prices':[],
					'book_price':""},
			'tripadvisor_city_id':"",
			'title_description':{'en':{'description':"",'r_shortdescription':"",'r_description':"",
									'r_avg_time_to_spend':"",'r_title':place_name,'name': place_name  },
								'fr':{'description':"",'r_shortdescription':"",'r_description':"",
									'r_avg_time_to_spend':"",'r_title':"",'name':""},
								'ar':{'description':"",'r_shortdescription':"",'r_description':"",
									'r_avg_time_to_spend':"",'r_title':"",'name':""}},
			'tripadvisor_city_name':"",
			'country_code':country_details.get("alpha_2_code") if country_details else None,
			"search_destination_id":searchdest_id.get("id") if searchdest_id else None,
			"rehlat_city_name":city_country_dict.get("city"),
			"rehlat_country_name":country_details.get("country"),
			"created_by": username,
			"created_on": datetime.now(),
			"type": ttd_type,
			'explore_url':explore_url,
			"is_popular":0,
			"nearbyttd": []
			}
			ttd_collection.insert_one(new_record)
			url='/thingstodo/edit/'+id+'/en/'
			return redirect(url)
		return render(request,'thingstodo/add_thingstodo.html')
	else:
		print(traceback.format_exc())
		print(e)
		return HttpResponseRedirect("/")


def edit_thingstodo(request, id, langauge_code):
	try:
		if request.session.get('name') is not None:
			langauge_di = {'en':1, 'fr':2, 'ar':3}
			langauge_ids = {1:'en', 2:'fr', 3:'ar'}
			default_langauge, second_language = langauge_code.split('-') if '-' in langauge_code else ['en', None]
			
			category_obj = ThingsToDoCategory.objects.filter(is_active=1)
			groups_obj = ThingsToDoGroups.objects.filter(language_master_id__in = [langauge_di.get(lan) for lan in [default_langauge, second_language]]).values('id', 'name')
			groups_dict = {group['id']:(group['name'], group['id'])  for group in groups_obj}
			group_category_obj = ThingsToDoGroupsCategory.objects.filter(language_master_id__in=[langauge_di.get(lan) for lan in [default_langauge, second_language]])
			# sub_category_obj = ThingsToDoSubCategory.objects.filter(language_master_id__in=[
			# langauge_di.get(lan) for lan in [default_langauge, second_language]])
			sub_category_obj = ThingsToDoSubCategory.objects.filter(is_active=1)
			sub_cat_di = {}
			for obj in sub_category_obj:
				if langauge_ids.get(obj.language_master_id) in sub_cat_di:
					sub_cat_di[langauge_ids.get(
						obj.language_master_id)][obj.id] = obj.localized_name
				else:
					sub_cat_di[langauge_ids.get(obj.language_master_id)] = {
						obj.id: obj.localized_name}

			cat_group_obj = {}
			try:
				for cat in group_category_obj:
					if langauge_ids.get(cat.language_master_id) in cat_group_obj:
						if groups_dict.get(cat.thingstodo_groups_id) in cat_group_obj[langauge_ids.get(cat.language_master_id)]:
							cat_group_obj[langauge_ids.get(cat.language_master_id)][groups_dict.get(cat.thingstodo_groups_id)]['subs'].append(
								{'title': cat.localized_name, 'id': str(cat.id)+'_'+str(cat.thingstodo_groups_id)})
						else:
							cat_group_obj[langauge_ids.get(cat.language_master_id)][groups_dict.get(cat.thingstodo_groups_id)] = {'subs': [
								{'title': cat.localized_name, 'id': str(cat.id)+'_'+str(cat.thingstodo_groups_id)}]}

					else:
						cat_group_obj[langauge_ids.get(cat.language_master_id)] = {groups_dict.get(cat.thingstodo_groups_id): {'subs': [
							{'title': cat.localized_name, 'id': str(cat.id)+'_'+str(cat.thingstodo_groups_id)}]}}
				
			except Exception as e:
				print(traceback.format_exc())
				print(e)

			cat_group_json = json.dumps([{'title': cgroup[0], 'id':str(
				cgroup[1]), 'subs':category['subs']} for cgroup, category in cat_group_obj['en'].items()])

			try:
				if second_language in cat_group_obj:
					cat_group_langauge_json = json.dumps(
						[
							{'title': cgroup[0],
							'id':str(cgroup[1]),
							'subs':category['subs']
							} for cgroup, category in cat_group_obj[second_language].items()]) if second_language else []
				else:
					cat_group_langauge_json = []
			except Exception as e:
				print(traceback.format_exc())
				print(e)

			trip_obj = ttd_collection.find_one({"things_todo_id": id}, {'_id': 0})

			data = {}
			data['is_timing_available'] = trip_obj.get('is_timing_available')
			data['id'] = trip_obj.get('ID')
			data['title'] = trip_obj.get('title_description', {})

			data['address'] = trip_obj.get('address_details', {})

			data['ancestors'] = trip_obj.get('ancestors')

			data['category'] = trip_obj.get('category')
			data['sub_category_ids'] = [sub_cat['id'] for sub_cat in trip_obj['subcategory']['en']] if 'subcategory' in trip_obj else []

			sub_cat_language = {}

			try:
				for langauge, sub_cat in trip_obj['subcategory'].items():
					if langauge in [default_langauge, second_language]:
						for cat in sub_cat:
							if langauge in sub_cat_language:
								sub_cat_language[langauge].append(cat['id'])
							else:
								sub_cat_language[langauge] = [cat['id']]
			except Exception as e:
				print(traceback.format_exc())
				print(e)

			# data['groups'] = []
			group_cat_ids = {}

			try:
				if 'groups' in trip_obj:
					for langauge, langauge_data in trip_obj['groups'].items():
						if langauge in [default_langauge, second_language]:
							for group in langauge_data:
								for gcat in group['categories']:
									if langauge in group_cat_ids:
										group_cat_ids[langauge].extend(
											[str(gcat['id'])+'_'+str(group['id']), str(group['id'])])
									else:
										group_cat_ids[langauge] = [
											str(gcat['id'])+'_'+str(group['id']), str(group['id'])]
			except Exception as e:
				print(traceback.format_exc())
				print(e)

			try:

				data['group_cat_ids'] = json.dumps(list(set(group_cat_ids['en'])))
			except Exception as e:
				data['group_cat_ids']=[]
				print(traceback.format_exc())
				print(e)
				
			try:
				data['group_cat_ids_langauge'] = json.dumps(list(set(group_cat_ids[second_language]))) if second_language else []
			except Exception as e:
				print(traceback.format_exc())
				print(e)
				data['group_cat_ids_langauge'] = []
				

			data['neighbourhood'] = trip_obj.get(
				'neighbourhood_info', []) if 'neighbourhood_info' in trip_obj else []

			data['trip_types'] = trip_obj.get(
				'trip_types', []) if 'trip_types' in trip_obj else []
			#print(trip_obj['things_todo_id'])
			data['open_close'] = {weekday: timings[0] for weekday, timings in trip_obj['open_close'].items()} if 'open_close' in trip_obj else{}

			data['rating_data'] = {}
			data['rating_data']['rating'] = trip_obj['rating'].get('rating', 0)
			data['rating_data']['rating_image_url'] = trip_obj['rating'].get(
				'rating_image_url', '')
			data['rating_data']['number_of_reviews'] = trip_obj['rating'].get(
				'num_of_reviews', '')
			data['rating_data']['review_rating_count'] = OrderedDict()

			if 'rating' in trip_obj:
				if 'review_rating_count' in trip_obj['rating']:
					if trip_obj['rating']['review_rating_count']:
						data['rating_data']['review_rating_count'] = OrderedDict(sorted(trip_obj['rating']['review_rating_count'].items()))

			data['prices'] = trip_obj['prices'] if 'prices' in trip_obj else {}
			data['beforego']=trip_obj['know_before_you_go'] if 'know_before_you_go' in trip_obj else {}
			data['blog']=trip_obj['blog'] if 'blog' in trip_obj else {}
			data['nearbyttd']=trip_obj['nearbyttd'] if 'nearbyttd' in trip_obj else {}
			data['city_id'] = trip_obj.get('city_id')
			data['things_todo_id'] = id
			data['seo_data']=trip_obj['seo_data'] if 'seo_data' in trip_obj else {}
			data['images']=trip_obj['images'] if 'images' in trip_obj else {} 
			seo_data_obj = seo_destination_mapping.find_one({'seo_type': 'thingstodo', 'is_active': 1}, {'seo_valid_tags': 1, '_id': 0})
			
			return render(request, "thingstodo/edit_thingstodo.html", {'data': data, "second_language": second_language, 'cat_group_json': cat_group_json, 'id': id, 'category_obj': category_obj,
																	'sub_category_obj': sub_category_obj, 'sub_cat_language': sub_cat_language, 
																	'sub_cat_di': sub_cat_di, 'cat_group_langauge_json': cat_group_langauge_json, 'seo_data_obj':seo_data_obj})
		else:
			return HttpResponseRedirect("/")
	except Exception as e:
		print(traceback.format_exc())
		print(e)
		return HttpResponseRedirect("/")


def format_language_data(data_dict):
	formated_data = {}
	for title_key, title_value in data_dict.items():
		langauge, key = title_key.split('-')
		if langauge not in formated_data:
			formated_data[langauge] = {key: title_value}
		else:
			formated_data[langauge][key] = title_value
	return formated_data


def get_image_path(request, id):
	try:
		if request.method == 'POST':
			img_name=request.FILES.get('file')
			img_from = request.POST.get('image_from')
			uploaded_image = upload_ttd_image(img_name, id) if img_from == "uploads" else upload_image(img_name, id)
			# uploaded_image= upload_image(img_name, id)
			if uploaded_image.get('status') == True:
				path=uploaded_image.get('path')
				path_dict={'path':path}
				return JsonResponse(path_dict,safe=False)
			else:
				return JsonResponse({"message": "Exception occured", "error": traceback.format_exc(), "action": "Failed"})
	except:
		print(traceback.format_exc())
		return JsonResponse({"message": "Exception occured", "error": traceback.format_exc(), "action": "Failed"})
	
	
def search_thingstodo(request):
    try:
        search_term = request.GET.get('search_term')
        if search_term : search_term = search_term.strip()
        city_id = request.GET.get('city_id')
        if city_id : city_id = int(city_id)
        ttd_id = request.GET.get('ttd_id')
        # ttd_name = request.GET.get('ttd_name')
        # if ttd_name : ttd_name = str(ttd_name)
        near_thingstodo_list = ttd_collection.find({'things_todo_id': {'$ne':ttd_id}, 'city_id':city_id,'is_active':1,'title_description.en.name':{'$regex':search_term,'$options':'i'}},{'_id':0,'things_todo_id':1,'title_description.en.name':1})
        result_list = [{'id':ttd.get('things_todo_id'),'value': ttd.get('title_description').get('en').get('name')} for ttd in near_thingstodo_list]
        return JsonResponse(result_list,safe=False)
    except:
        print(traceback.print_exc())

def thingstodo_status_update(request):
	
	if request.method == "POST":
		# print(request.POST)
		ttd_id = str(request.POST.get('ttd_id'))
		obj = ttd_collection.find_one({'things_todo_id':ttd_id},{'is_active':1})
		value = obj.get('is_active')
		status = 0
		if value == 1:
			ttd_collection.update_one({'things_todo_id':ttd_id},{'$set':{'is_active':0}})
			status = 0
		else:
			ttd_collection.update_one({'things_todo_id':ttd_id},{'$set':{'is_active':1}})
			status = 1 
		data = {
			'status':status,
			'item_id':ttd_id
		}
		# return JsonResponse({'data': json_util.dumps(data)})   
		return JsonResponse({'data': json.loads(json_util.dumps(data))})


def edit_thingstodo_tite_page(request, id, type):
	try:
		if type not in ['deleteimage', 'titledetails', 'addressdetails', 'ancestordetails', 'categorydetails', 'neighbourdetails', 'ratingdetails', 
						'pricingdetails', 'timingdetails', 'imagedetails', 'seodetails', 'blogdetails','beforegodetails','nearbyttddetails','dynamiccontent']:
			raise Http404
			   
		if request.method == 'POST':
			
			if type == 'deleteimage':
				
				img_path= request.POST.get('file')
			
				img_meta_data=request.POST.get('image_meta_data') 
				img_data={'r_image':img_path,'meta_data':img_meta_data}  
				respective_data2=ttd_collection.find_one({"things_todo_id":id})
				img_list=respective_data2.get('images',[])
				remove_idx = []
				if img_data in img_list:
					for idx, images in enumerate(img_list):
						if img_path in images.values():
							remove_idx.append(idx)

					if remove_idx:
						for idxs in remove_idx:
							del img_list[idxs]
						ttd_collection.update_one({'things_todo_id': id}, {'$set': {'images': img_list}}) 
				
				return JsonResponse({"message": "Success"})
			
			if type == 'seodetails':
				image_file = request.FILES.get('seo_image_file')

				seo_lang_data = {}

				for seo_key, seo_value in request.POST.items():
					lang, seotype, seo_id = seo_key.split("-")
					if lang not in seo_lang_data:
						uploaded_image = upload_image(image_file, id)
						ogimage = uploaded_image['path'] if uploaded_image['status'] == True else None
						seo_lang_data[lang] = {seo_id: {seotype:seo_value, 'ogimage':ogimage}}
					else:
						if seo_id not in seo_lang_data[lang]:
							uploaded_image = upload_image(image_file, id)
							ogimage = uploaded_image['path'] if uploaded_image['status'] == True else None
							seo_lang_data[lang][seo_id] = {seotype:seo_value, 'ogimage':ogimage}
						else:
							seo_lang_data[lang][seo_id][seotype] = seo_value

				seodata = {langdata: datavalues.values() for langdata, datavalues in seo_lang_data.items()}
				
				ttd_collection.update_one({"things_todo_id": id}, {'$set': {'seo': seodata}})

				return JsonResponse({"message": "Success"})

			request_data = json.loads(request.POST.get('data'))
		
			if request_data:
				if type == 'categorydetails':
					form_data = {}
					
					for category in request_data:
						if category['value']:
							if category['name'] in form_data:
								form_data[category['name']].append(int(category['value']))
							else:
								form_data[category['name']] = [int(category['value'])]
				else:
					form_data = {data['name']: data['value'].strip() for data in request_data}

				if type == 'titledetails':
					standard_data = {}
					for title_key, title_value in form_data.items():
						langauge, key = title_key.split('-')
						title_value = "" if title_value.strip() == '<p><br></p>' else title_value.replace("&lt;p&gt;", '').replace("&lt;/p&gt;", '').replace("<p><br></p>", "<br>")
						if langauge not in standard_data:
							standard_data[langauge] = {key: title_value}
						else:
							standard_data[langauge][key] = title_value

					sddetails = ttd_collection.find_one({"things_todo_id": id})
					title_data = sddetails['title_description']
					for langauge, value in title_data.items():
						for title_name, title_value in value.items():
							if langauge in standard_data:
								title_data[langauge] = standard_data[langauge]
					title_data['fr']['r_avg_time_to_spend'] = title_data['ar']['r_avg_time_to_spend'] = title_data['en']['r_avg_time_to_spend'] = standard_data['en']['r_avg_time_to_spend']
					ttd_collection.update_one({"things_todo_id": id}, {
											'$set': {'title_description': title_data}})
					
					return JsonResponse({"mesaage": "Success"})        
				
				if type == 'nearbyttddetails':
					add_ttd = json.loads(request.POST.get('add_ttd'))
					select_ttd = json.loads(request.POST.get('select_ttd'))
					nearby_ttd_data = []
					for name,ttd_id in add_ttd.items():
						if {'thingstodo_id':ttd_id.strip(),'name':name} not in nearby_ttd_data:
							nearby_ttd_data.append({'thingstodo_id':ttd_id.strip(),'name':name})
					for name_id in select_ttd:
						ttd_id,ttd_name = name_id.split('---')
						if {'thingstodo_id':ttd_id.strip(),'name':ttd_name} not in nearby_ttd_data:
							nearby_ttd_data.append({'thingstodo_id':ttd_id.strip(),'name':ttd_name})
					ttd_collection.update_one({"things_todo_id":id},{'$set':{'nearbyttd':nearby_ttd_data}})
					return JsonResponse({"message": "Success"})     
					
				if type =='beforegodetails':
					
					old_beforego_data=ttd_collection.find_one({'things_todo_id':id},{'_id':0,'know_before_you_go':1})
					old_beforego_data=old_beforego_data.get('know_before_you_go',{})
					beforego_data={}
					
					for before_key,before_value in form_data.items():
						lang, before_type = before_key.split("-")
						before_type=before_type.split("_")[-1]
						before_value = "" if before_value.strip() == "<p><br></p>" else before_value.replace("&lt;p&gt;", '').replace("&lt;/p&gt;", '')
						if lang not in beforego_data:
							beforego_data[lang]={before_type:before_value}
						else:
							beforego_data[lang][before_type]=before_value 
					
					# beforego_data_final={langdata: datavalues.values() for langdata,datavalues in beforego_data.items()}
					
					for lang,data in beforego_data.items():
						old_beforego_data[lang]=data 
					
					ttd_collection.update_one({"things_todo_id":id},{'$set':{'know_before_you_go':old_beforego_data}})
					return JsonResponse({"message": "Success"}) 
						
				if type == 'blogdetails':
					old_blog_data=ttd_collection.find_one({'things_todo_id':id},{'_id':0,'blog':1})
					old_blog_data=old_blog_data.get('blog',{})
				
					blog_lang_data = {}

					for blog_key, blog_value in form_data.items():
						lang, blogtype, blog_id = blog_key.split("-")
						blogtype=blogtype.split("_")[-1]
						blog_value = "" if blog_value.strip() == '<p><br></p>' else blog_value.replace("&lt;p&gt;", '').replace("&lt;/p&gt;", '')
						if lang not in blog_lang_data:
							blog_lang_data[lang] = {
								blog_id: {blogtype: blog_value}}
						else:
							if blog_id not in blog_lang_data[lang]:
								blog_lang_data[lang][blog_id] = {
									blogtype: blog_value}
							else:
								blog_lang_data[lang][blog_id][blogtype] = blog_value

					blogdata = {langdata: datavalues.values() for langdata, datavalues in blog_lang_data.items()}
					for lang,data in blogdata.items():
						old_blog_data[lang]=data

					ttd_collection.update_one({"things_todo_id": id}, {'$set': {'blog':old_blog_data}})

					return JsonResponse({"message": "Success"})    
					
				if type == 'dynamiccontent':
			
					old_seo_data=ttd_collection.find_one({'things_todo_id':id},{'_id':0,'seo_data':1})
					old_seo_data = old_seo_data.get('seo_data',{})
					
					seo_data={}
					for content_key,content_value in form_data.items():
						lang, contenttype = content_key.split("-")
						content_value = "" if content_value == '<p><br></p>' else content_value.replace("&lt;p&gt;", '').replace("&lt;/p&gt;", '')
						if lang not in seo_data:
							seo_data[lang]={contenttype:content_value} 
						else:
							seo_data[lang][contenttype]=content_value 
							
					for lang,data in seo_data.items():
						old_seo_data[lang]=data
						
					ttd_collection.update_one({"things_todo_id":id},{"$set":{"seo_data":old_seo_data}})
					return JsonResponse({"message": "Success"})    

				if type == 'addressdetails':
					sddetails = ttd_collection.find_one({"things_todo_id": id})
					ttd_type = sddetails.get('type')
					address_data = sddetails['address_details']
					country_id = form_data.pop('countryid',None)
					city_id = form_data.pop('cityid',None)
					standard_data = format_language_data(form_data)
					name = sddetails.get('title_description').get('en').get('name')
					country = standard_data.get('en').get('country')                   
					city = standard_data.get('en').get('city')
					
					update_set = {}
					sd_data = ''
					if ttd_type == "CITY" and city_id:
						sd_data = search_destination.find_one({'type':'CITY','city_id':int(city_id)},{'id':1,'_id':0})
					elif ttd_type == "COUNTRY" and country_id:
						sd_data = search_destination.find_one({'type':'COUNTRY','country_id':int(country_id)},{'id':1,'_id':0})
					sd_id = sd_data.get('id') if sd_data else None
     
					if sd_id: update_set.update({'search_destination_id': sd_id})	
					if country_id and country: update_set.update({'country_id':int(country_id),'ID.r_country_id':int(country_id),'rehlat_country_name':country})
					if city_id and city: update_set.update({'city_id':int(city_id),'ID.r_city_id':int(city_id),'rehlat_city_name':city})
					if country and city and name : update_set.update({'explore_url': slugify('{0} {1} {2}'.format(name, city, country))})
					explore_url = slugify('{0} {1} {2}'.format(name, city, country))
					
					for language, value in address_data.items():
						for address_name, address_value in value.items():
							if language in standard_data:
								if address_name in standard_data[language]:
									address_data[language][address_name] = standard_data[language][address_name]
					update_set.update({'address_details': address_data})
					# ttd_collection.update_one({"things_todo_id": id}, {
					#                     '$set': {'address_details': address_data}})
					ttd_collection.update_one({"things_todo_id": id},{'$set':update_set})

					return JsonResponse({"mesaage": "Success"})

				if type == 'ancestordetails':
					sddetails = ttd_collection.find_one({"things_todo_id": id})
					ancestors_data = sddetails['ancestors']

					standard_data = {}

					for form_key, ancetor_value in form_data.items():
						langauge, ancetor = form_key.split('-')
						ancetor_type = ancetor.split('_')[0]
						ancetor_key = ancetor.split('_')[1].replace(
							'location', 'location_id')
						if langauge not in standard_data:
							standard_data[langauge] = {
								ancetor_type: {ancetor_key: ancetor_value}}
						else:
							if ancetor_type not in standard_data[langauge]:
								standard_data[langauge][ancetor_type] = {
									ancetor_key: ancetor_value}
							else:
								standard_data[langauge][ancetor_type][ancetor_key] = ancetor_value

					for langauge, value in ancestors_data.items():
						if langauge in standard_data:
							for ancestor, data in value.items():
								if ancestor in standard_data[langauge]:
									for ancetor_name, ancetor_value in data.items():
										if ancetor_name in standard_data[langauge][ancestor]:
											ancestors_data[langauge][ancestor][ancetor_name] = standard_data[langauge][ancestor][ancetor_name]
											

					ttd_collection.update_one({"things_todo_id": id}, {
										'$set': {'ancestors': ancestors_data}})

					return JsonResponse({"mesaage": "Success"})

				if type == 'categorydetails':
					things_todo_id = id
					sddetails = ttd_collection.find_one({"things_todo_id": things_todo_id})
					try:
						selected_groups = eval(request.POST.get('selected_groups')) if request.POST.get('selected_groups') else []
					except:
						selected_groups = {}
					
					group_category = ThingsToDoGroupsCategory.objects.filter(id__in=[int(id.split('_')[0]) for group, ids in selected_groups.items() for id in ids if '_' in str(id)])
					category_obj_en = ThingsToDoCategory.objects.filter(id__in=[ id for cat, values in form_data.items() for id in values if 'en-category_ids' in cat])
					# category_obj_fr = ThingsToDoCategory.objects.filter(id__in=[ id for cat, values in form_data.items() for id in values if 'fr-category_ids' in cat])
					# category_obj_ar = ThingsToDoCategory.objects.filter(id__in=[ id for cat, values in form_data.items() for id in values if 'ar-category_ids' in cat])
					sub_category_obj_en = ThingsToDoSubCategory.objects.filter(
						id__in=[id for cat, values in form_data.items() for id in values if 'en-sub_category_ids' in cat]) 
					# sub_category_obj_fr = ThingsToDoSubCategory.objects.filter(
					#     id__in=[id for cat, values in form_data.items() for id in values if 'fr-sub_category_ids' in cat])
					# sub_category_obj_ar = ThingsToDoSubCategory.objects.filter(
					#     id__in=[id for cat, values in form_data.items() for id in values if 'ar-sub_category_ids' in cat])
					

					category_details, group_category_details = {}, {}
					
			
					for obj in category_obj_en:
						print(obj)
						if 'en' not in category_details:
							category_details['en'] = {
								'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name}
						else:
							category_details = {'en' :{
								'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name}}
					
						if 'fr' not in category_details:
							category_details['fr'] = {
								'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_fr}
						else:
							category_details = {'fr' :{
								'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_fr}}

						if 'ar' not in category_details:
							category_details['ar'] = {
								'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_ar}
						else:
							category_details = {'ar' :{
								'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_ar}}
					
					# for obj in category_obj_fr:
					#     print(obj)
					#     if 'fr' not in category_details:
					#         category_details['fr'] = {
					#             'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_fr}
					#     else:
					#         category_details = {'fr' :{
					#             'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_fr}}
					# for obj in category_obj_ar:
					#     print(obj)
					#     if 'ar' not in category_details:
					#         category_details['ar'] = {
					#             'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_ar}
					#     else:
					#         category_details = {'ar' :{
					#             'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_ar}}
								
					sub_category_details = {}

					for obj in sub_category_obj_en:
						if 'en' in sub_category_details:
							sub_category_details['en'].append(
							{'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name})
						else:
							sub_category_details['en'] = [
							{'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name}]

						if 'fr' in sub_category_details:
							sub_category_details['fr'].append(
							{'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_fr})
						else:
							sub_category_details['fr'] = [
							{'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_fr}]
					
						if 'ar' in sub_category_details:
							sub_category_details['ar'].append(
							{'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_ar})
						else:
							sub_category_details['ar'] = [
							{'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_ar}]

					# for obj in sub_category_obj_fr:
					#     if 'fr' in sub_category_details:
					#         sub_category_details['fr'].append(
					#         {'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_fr})
					#     else:
					#         sub_category_details['fr'] = [
					#         {'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_fr}]
							
					# for obj in sub_category_obj_ar:
					#     if 'ar' in sub_category_details:
					#         sub_category_details['ar'].append(
					#         {'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_ar})
					#     else:
					#         sub_category_details['ar'] = [
					#         {'id': obj.id, 'name': obj.name, 'localized_name': obj.localized_name_ar}]
						   
					for obj in group_category:
						if obj.language_master.language_code not in group_category_details:
							group_category_details[obj.language_master.language_code] = {
								obj.thingstodo_groups_id: {'id': obj.thingstodo_groups_id, 'localized_name': obj.thingstodo_groups.localized_name,
														'categories': [{'id': obj.id, 'groupid': obj.thingstodo_groups_id, 'category_localized_name': obj.localized_name, 'name': obj.name}]}}

						else:
							if obj.thingstodo_groups_id not in group_category_details[obj.language_master.language_code]:
								group_category_details[obj.language_master.language_code][obj.thingstodo_groups_id] = {
									'id': obj.thingstodo_groups_id, 'localized_name': obj.thingstodo_groups.localized_name,
									'categories': [{'id': obj.id, 'groupid': obj.thingstodo_groups_id, 'category_localized_name': obj.localized_name, 'name': obj.name}]
								}
							else:
								group_category_details[obj.language_master.language_code][obj.thingstodo_groups_id]['categories'].append(
									{'id': obj.id, 'groupid': obj.thingstodo_groups_id, 'category_localized_name': obj.localized_name, 'name': obj.name})

					group_details = sddetails['groups']
					for language, groups in group_details.items():
						if language in group_category_details:
							group_details[language] = group_category_details[language].values()

					category = sddetails['category']
					for language, groups in category.items():
						if language in category_details:
							category[language] = category_details[language]

					subcategory = sddetails['subcategory']
					for language, groups in subcategory.items():
						if language in sub_category_details:
							subcategory[language] = sub_category_details[language]

					# ttd_collection.update_one({"things_todo_id":id}, {'$set': {
					#            'subcategory': sub_category_details, 'category': category_details, 'groups': group_category_details.values()}})
					
					ttd_collection.update_one({"things_todo_id":things_todo_id}, {'$set': {'subcategory':subcategory, 'category': category, 'groups': group_details}})
					
					return JsonResponse({"mesaage": "Success"})

				if type == 'neighbourdetails':

					neighbour, trip = {}, {}

					sddetails = ttd_collection.find_one({"things_todo_id": id}, {
													'neighbourhood_info': 1, 'trip_types': 1, '_id': 0})

					neighbour_data = sddetails['neighbourhood_info']
					trip_data = sddetails['trip_types']

					for name, value in form_data.items():

						# if '-' in name:
						langauge, name = name.split('-')

						if 'neighbor' in name:
							type = name.split('_')
							type[1] = 'location_id' if type[1] == 'location' else type[1]


							if langauge not in neighbour:
								neighbour[langauge] = {type[-1]: {type[1]: value}}
							else:
								if type[-1] not in neighbour[langauge]:
									neighbour[langauge][type[-1]] = {type[1]: value}
								else:
									neighbour[langauge][type[-1]][type[1]] = value
						else:
							type = name.split('_')

							if langauge not in trip:
								trip[langauge] = {
									type[-1]: {type[1].replace('localized', 'localized_name'): value}}
							else:

								if type[-1] not in trip[langauge]:
									trip[langauge][type[-1]] = {type[1].replace('localized', 'localized_name'): value}
								else:
									trip[langauge][type[-1]][type[1].replace('localized', 'localized_name')] = value



					for langauge, data in neighbour_data.items():
						if langauge in neighbour:
							neighbour_data[langauge] = [neigh_data for val, neigh_data in neighbour[langauge].items()]

					for langauge, data in trip_data.items():
						if langauge in trip:
							trip_data[langauge] = [trip_value for val, trip_value in trip[langauge].items()]


					ttd_collection.update_one({"things_todo_id": id}, {'$set': {'neighbourhood_info': neighbour_data, 'trip_types': trip_data}})
					return JsonResponse({"mesaage": "Success"})

				if type == 'pricingdetails':
					sddetails = ttd_collection.find_one({"things_todo_id": id})
					price_details = sddetails['prices']

					for name, value in form_data.items():
						if name in price_details:
							price_details[name] = value
						else:
							price_details[name] = value
							
					ttd_collection.update_one({"things_todo_id": id}, {'$set': {'prices': price_details}})
					return JsonResponse({"mesaage": "Success"})

				if type == 'timingdetails':
					week_details = {}
					print('------------------------->OpenClose:',)
					isopen_key_list = ['sunday_isopen','monday_isopen','tuesday_isopen','wednesday_isopen','thursday_isopen','friday_isopen','saturday_isopen']
					is24hours_key_list = ['sunday_is24hours','monday_is24hours','tuesday_is24hours','wednesday_is24hours','thursday_is24hours','friday_is24hours','saturday_is24hours']
					form_data_keys_list = form_data.keys()
					istiming_available = 0
					if 'istiming_available' in form_data_keys_list:
						istiming_available = 1 
					for isopen_key in isopen_key_list:
						if isopen_key in form_data_keys_list:
							form_data[isopen_key] = 1
						else:
							form_data[isopen_key] = 0
					for is24hours_key in is24hours_key_list:
						if is24hours_key in form_data_keys_list:
							form_data[is24hours_key] = 1
						else:
							form_data[is24hours_key] = 0
					for weekname, value in form_data.items():
						if weekname.split('_')[0] in week_details:
							week_details[weekname.split('_')[0]][0][weekname.split('_')[1]] = value
						else:
							week_details[weekname.split('_')[0]] = [{weekname.split('_')[1]: value}]


					ttd_collection.update_one({"things_todo_id": id}, {'$set': {'open_close': week_details,'is_timing_available':istiming_available}})
					return JsonResponse({"mesaage": "Success"})

				if type == 'ratingdetails':

					rating_li = ['num_of_reviews', 'rating_image_url', 'rating']
					# review_count = ["1", "2", "3", "4", "5"]
					rating_data = {}
					for rating_key, rating_val in form_data.items():
						if rating_key in rating_li:
							rating_data[rating_key] = rating_val
						else:
							if 'review_rating_count' in rating_data:
								rating_data['review_rating_count'][rating_key] = rating_val
							else:
								rating_data['review_rating_count'] = {
									rating_key: rating_val}
					ttd_collection.update_one({"things_todo_id": id}, {'$set': {'rating': rating_data}})
					return JsonResponse({"mesaage": "Success"})
				
				if type == 'imagedetails':

					image_data={}
					for image_key,image_val in form_data.items():
						img_key, image_id =image_key.split("-")
						if image_id not in image_data:
							if img_key == "meta_data": 
								image_data[image_id]={img_key:image_val}
							else:
								image_data[image_id]={img_key:image_val, "r_image_small":image_val, "r_image_large":image_val, "r_image_medium":image_val, "r_image_thumbnail":image_val}
						else:
							if img_key == "meta_data": 
								image_data[image_id][img_key]=image_val 
							else:
								image_data[image_id][img_key] = image_val
								image_details = image_val.split('/')
								image_path = "/".join(image_details[0:-1])
								image_url = image_path + "{size}" + image_details[-1]
								# image_data[image_id]["r_image_small"] = image_url.format(size="/small_")
								image_data[image_id]["r_image_large"] = image_url.format(size="/large_")       
								# image_data[image_id]["r_image_medium"] = image_url.format(size="/medium_")
								image_data[image_id]["r_image_thumbnail"] = image_url.format(size="/thumbnail_")
					image_list=image_data.values()
					
					ttd_collection.update_one({'things_todo_id': id}, {'$set': {'images':image_list}})
					
					return JsonResponse({"message": "Success"})
				
			else:
				return JsonResponse({"message": "Please Provide Data", "error": traceback.format_exc(), "action": "Failed"})
	except:
		print(traceback.format_exc())
		return JsonResponse({"message": "Exception occured", "error": traceback.format_exc(), "action": "Failed"})


def subcategory_list(request):
	subcategory_data = ThingsToDoSubCategory.objects.all().values('id', 'name', 'localized_name', 'localized_name_ar','localized_name_fr','language_master', 'is_active')

	page = request.GET.get('page', 1)

	paginator = Paginator(subcategory_data, 10)  # here 10 is no.of records for page
	
	try:
		sub_data = paginator.page(page)
	except PageNotAnInteger:
		sub_data = paginator.page(1)
	except EmptyPage:
		sub_data = paginator.page(paginator.num_pages)

	return render(request, 'thingstodo/list_subcategory.html', {'sub_data': sub_data})

	# context={'sub_data':subcategory_data}
	# return render(request,'thingstodo/list_subcategory.html',context)


def subcategory_add(request):

	# language_data = LangaugeMaster.objects.all().values('id', 'language_code')
	# context = {'languages': language_data}

	if request.method == "POST":

		name = request.POST.get('name')
		localized_name = request.POST.get('local_name')
		localized_name_ar = request.POST.get('localized_name_ar')
		localized_name_fr = request.POST.get('localized_name_fr')

		is_active = request.POST.get('is_active')

		# language = request.POST.get('language')

		# language_int = int(language)
		# language_instance = LangaugeMaster.objects.get(id=language_int)

		sub_cat_data_for_check = ThingsToDoSubCategory.objects.filter(
			name=name)

		# language_data = LangaugeMaster.objects.all().values('id', 'language_code')
		# context = {'languages': language_data}
		if (len(sub_cat_data_for_check) == 0):

			sub_cat = ThingsToDoSubCategory(
				name=name, localized_name=localized_name, localized_name_ar=localized_name_ar,localized_name_fr=localized_name_fr, is_active=int(is_active))
			sub_cat.save()
			messages.success(request, 'submitted successfully.')
			return render(request, 'thingstodo/add_subcategory.html')

		else:
			messages.error(request, 'Already existed!')
			return render(request, 'thingstodo/add_subcategory.html')

	return render(request, 'thingstodo/add_subcategory.html')


def subcategory_edit(request, id):
	
	subcategory_data = ThingsToDoSubCategory.objects.get(id=id)
	# language_data = LangaugeMaster.objects.all().values('id', 'language_code')
	context = {'sub_data': subcategory_data}

	if request.method == "POST":
		name_u = request.POST.get('name')
		localized_name_u = request.POST.get('localized_name')
		localized_name_ar = request.POST.get('localized_name_ar')
		localized_name_fr = request.POST.get('localized_name_fr')

		# language_u = request.POST.get('language')
		is_active_u = request.POST.get('is_active')

		# language_int = int(language_u)
		# language_instance = LangaugeMaster.objects.get(id=language_int)
		subcategory_data = ThingsToDoSubCategory.objects.using('default').get(id=id)
		
		# subcategory_data = ThingsToDoSubCategory.objects.get(id=id)

		subcategory_data.name = name_u
		subcategory_data.localized_name = localized_name_u
		subcategory_data.localized_name_ar = localized_name_ar
		subcategory_data.localized_name_fr = localized_name_fr

		# subcategory_data.language = language_instance
		subcategory_data.is_active = int(is_active_u)

		subcategory_data.save()

		# messages.success(request, 'updated successfully.')
		return redirect('thingstodo_subcategory_list')
	return render(request, 'thingstodo/edit_subcategory.html', context)



def get_city_list():
	
	result_list = []
	obj = city_col.find({},{'_id','city'})
	for doc in obj:
		t = (doc['_id'],doc['city'])
		result_list.append(t)
	return result_list



def thingstodo_list(request):
	
	projections =  {'_id':0,'things_todo_id':1,'title_description.en.name':1,'tripadvisor_city_name':1,'category.en.localized_name':1,'search_destination_id':1,'tripadvisor_id':1,'type':1,'is_active':1,'is_popular':1, "rehlat_city_name":1}
	page = request.GET.get('page', 0)
	entries_per_page = int(request.GET.get('entries_per_page', 20))  # default to 20 if not specified
	is_active = request.GET.get('is_active')
	if is_active == "1" or is_active == "0":
		is_active = int(is_active)
		data_obj = list(ttd_collection.find({'is_active':is_active},projections).skip(page*entries_per_page).limit(entries_per_page))
		data_obj_count = ttd_collection.find({'is_active':is_active}).count()
	else:
		data_obj = list(ttd_collection.find({},projections).sort('is_active',-1).skip(page*entries_per_page).limit(entries_per_page))
		data_obj_count = ttd_collection.count()
	paginator_count = range(1, int(data_obj_count/entries_per_page)+1)
	
	paginator = Paginator(data_obj, entries_per_page)
	try:         
		thingstodo_docs = paginator.page(page)
	except PageNotAnInteger:
		thingstodo_docs = paginator.page(1)
	except EmptyPage:
		thingstodo_docs = paginator.page(paginator.num_pages)
	start = (page * entries_per_page)+1
	end = (page+1) * entries_per_page
	if end > data_obj_count:
		end = data_obj_count
	page_options = [10,20,50,100]
	return render(request, 'thingstodo/listing_page.html', {'thingstodo_docs': thingstodo_docs, "paginator_count":paginator_count,'data_obj_count':data_obj_count,'start':start,'end':end,'entries_per_page':entries_per_page,'page_options':page_options,'is_active':is_active})

def thingstodo_filter_list(request):
	
	city_id = 0 
	city_name = ""
	data_obj = ""
	input_value = ""
	projections =  {'_id':0,'things_todo_id':1,'title_description.en.name':1,'tripadvisor_city_name':1,'category.en.localized_name':1,'search_destination_id':1,'tripadvisor_id':1,'type':1,'is_active':1,'is_popular':1, "rehlat_city_name":1}
	page = int(request.GET.get('page', 0))
	entries_per_page = int(request.GET.get('entries_per_page', 20))  # default to 20 if not specified
	is_active = request.GET.get('is_active')
	if request.method == 'GET':
	
		input_value = str(request.GET.get('text_box_search'))
		city_id = str(request.GET.get('cityid'))
		if input_value in ("", "None") and city_id in ("", "None"):   
			query = {}
			# data_obj_count = ttd_collection.count()
			# data_obj = list(ttd_collection.find().skip(page*20).limit(20))
		
		elif input_value != "" and city_id != "":
			obj = city_col.find_one({'_id':int(city_id)})
			city_name = obj['city']
			if input_value.isdigit():
				input_value = int(input_value)
				query =  {'$and':[{'city_id':int(city_id)},{'$or':[{'tripadvisor_id':{'$in':[input_value, str(input_value)]}},{'search_destination_id':input_value}]}]}
				
				# data_obj_count = ttd_collection.find({'$and':[{'city_id':int(city_id)},{'$or':[{'tripadvisor_id':{'$in':[input_value, str(input_value)]}},{'search_destination_id':input_value}]}]},{'_id':1}).count() 
				# data_obj = list(ttd_collection.find({'$and':[{'city_id':int(city_id)},{'$or':[{'tripadvisor_id':{'$in':[input_value, str(input_value)]}},{'search_destination_id':input_value}]}]},{'_id':0}).skip(page*20).limit(20))
			else:
				query = {'$and':[{'city_id':int(city_id)},{'$or':[{'title_description.en.name':{'$regex':input_value,'$options':'i'}},{'category.en.name':{'$regex':input_value,'$options':'i'}} ]}]}
				# data_obj_count = ttd_collection.find({'$and':[{'city_id':int(city_id)},{'$or':[{'title_description.en.name':{'$regex':input_value,'$options':'i'}},{'category.en.name':{'$regex':input_value,'$options':'i'}} ]} ]},{'_id':1}).count()
				# data_obj = list(ttd_collection.find({'$and':[{'city_id':int(city_id)},{'$or':[{'title_description.en.name':{'$regex':input_value,'$options':'i'}},{'category.en.name':{'$regex':input_value,'$options':'i'}} ]} ]},{'_id':0}).skip(page*20).limit(20))
		
		elif input_value == '':
			obj = city_col.find_one({'_id':int(city_id)})
			city_name = obj['city']
			city_id = int(city_id)
			# data_obj = list(ttd_collection.find({'city_id':city_id}).limit(250))
			query = {'city_id':city_id}

		elif city_id == "":
			
			if input_value.isdigit():
				input_value = int(input_value)
				query = {'$or':[{'tripadvisor_id':{'$in':[input_value, str(input_value)]}},{'search_destination_id':input_value}]}
				# data_obj = list(ttd_collection.find({'$or':[{'tripadvisor_id':{'$in':[input_value, str(input_value)]}},{'search_destination_id':input_value}]},{'_id':0}).limit(250))
			else:
				query = {'$or':[{'title_description.en.name':{'$regex':input_value,'$options':'i'}},{'category.en.name':{'$regex':input_value,'$options':'i'}} ]}
				# data_obj = list(ttd_collection.find({'$or':[{'title_description.en.name':{'$regex':input_value,'$options':'i'}},{'category.en.name':{'$regex':input_value,'$options':'i'}} ]},{'_id':0}).limit(250))

	if request.method == "POST":
		city_name = str(request.POST.get('cities'))
		city_id = str(request.POST.get('cityid'))
		input_value = str(request.POST.get('text_box_search'))
		city_filter_id = str(request.POST.get('city_filter_id'))

		if city_id == "" and input_value == "":
			query = {}
		elif input_value == "":
			query = {'city_id':int(city_id)}
			# data_obj = list(ttd_collection.find({'city_id':int(city_id)}).limit(250))
		elif city_id == "":
			if city_filter_id == "":
				if input_value.isdigit():
					input_value = int(input_value)
					query = {'$or':[{'tripadvisor_id':{'$in':[input_value, str(input_value)]}},{'search_destination_id':input_value}]}
					# data_obj = list(ttd_collection.find({'$or':[{'tripadvisor_id':{'$in':[input_value, str(input_value)]}},{'search_destination_id':input_value}]},{'_id':0}).limit(250))
				else:
					query = {'$or':[{'title_description.en.name':{'$regex':input_value,'$options':'i'}},{'category.en.name':{'$regex':input_value,'$options':'i'}} ]}
					# data_obj = list(ttd_collection.find({'$or':[{'title_description.en.name':{'$regex':input_value,'$options':'i'}},{'category.en.name':{'$regex':input_value,'$options':'i'}} ]},{'_id':0}).limit(250))
				
			elif city_filter_id != "" :
				obj = city_col.find_one({'_id':int(city_filter_id)})
				city_name = obj['city']
				if input_value.isdigit():
					city_filter_id = int(city_filter_id)
					query = {'$and':[{'city_id':city_filter_id},{'$or':[{'tripadvisor_id':{'$in':[int(input_value), str(input_value)]}},{'search_destination_id':int(input_value)}]}]}
					# data_obj = list(ttd_collection.find({'$and':[{'city_id':city_filter_id},{'$or':[{'tripadvisor_id':{'$in':[input_value, str(input_value)]}},{'search_destination_id':int(input_value)}]}]},{'_id':0}).limit(250))
				else:
					query = {'$and':[{'city_id':int(city_filter_id)},{'$or':[{'title_description.en.name':{'$regex':input_value,'$options':'i'}},{'category.en.name':{'$regex':input_value,'$options':'i'}} ]} ]}
					# data_obj = list(ttd_collection.find({'$and':[{'city_id':int(city_filter_id)},{'$or':[{'title_description.en.name':{'$regex':input_value,'$options':'i'}},{'category.en.name':{'$regex':input_value,'$options':'i'}} ]} ]},{'_id':0}).limit(250))
				city_id = int(city_filter_id)  
					
		elif city_id != "" and input_value != "":
			obj = city_col.find_one({'_id':int(city_id)})
			city_name = obj['city'] 
			if input_value.isdigit():
				input_value = int(input_value)
				query = {'$and':[{'city_id':int(city_id)},{'$or':[{'tripadvisor_id':{'$in':[input_value, str(input_value)]}},{'search_destination_id':input_value}]}]}
				# data_obj = list(ttd_collection.find({'$and':[{'city_id':int(city_id)},{'$or':[{'tripadvisor_id':{'$in':[input_value, str(input_value)]}},{'search_destination_id':input_value}]}]},{'_id':0}).limit(250))
			else:
				query = {'$and':[{'city_id':int(city_id)},{'$or':[{'title_description.en.name':{'$regex':input_value,'$options':'i'}},{'category.en.name':{'$regex':input_value,'$options':'i'}} ]} ]}
				# data_obj = list(ttd_collection.find({'$and':[{'city_id':int(city_id)},{'$or':[{'title_description.en.name':{'$regex':input_value,'$options':'i'}},{'category.en.name':{'$regex':input_value,'$options':'i'}} ]} ]},{'_id':0}).limit(250))
	
	if is_active =="0" or is_active == "1":
		is_active = int(is_active)
		query["is_active"] = is_active
	data_obj_count = ttd_collection.find(query, {'_id':0}).count()
	data_obj = list(ttd_collection.find(query, projections).sort('is_active',-1).skip(page*entries_per_page).limit(entries_per_page))
	paginator_count = range(1, int(data_obj_count/entries_per_page)+1)

	paginator = Paginator(data_obj, entries_per_page)
	try:
		thingstodo_docs = paginator.page(page)
	except PageNotAnInteger:
		thingstodo_docs = paginator.page(1)
	except EmptyPage:
		thingstodo_docs = paginator.page(paginator.num_pages)
	start = (page * entries_per_page)+1
	end = (page+1) * entries_per_page
	if end > data_obj_count:
		end = data_obj_count
	page_options = [10,20,50,100]
	return render(request,'thingstodo/listing_page.html', {'page_no':page,'city_id':city_id,'city':city_name,'thingstodo_docs': thingstodo_docs,'input_value':input_value, "paginator_count":paginator_count, 'data_obj_count':data_obj_count,'start':start,'end':end,'entries_per_page':entries_per_page,'page_options':page_options,'is_active':is_active})
 
def category_list(request):
	category_list = ThingsToDoCategory.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(category_list, 10)
	try:
		categories = paginator.page(page)
	except PageNotAnInteger:
		categories = paginator.page(1)
	except EmptyPage:
		categories = paginator.page(paginator.num_pages)

	return render(request, 'thingstodo/category_list_page.html', { 'categories': categories})

def language_master_list(request):
	language_master_list = LangaugeMaster.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(language_master_list, 10)
	try:
		languages = paginator.page(page)
	except PageNotAnInteger:
		languages = paginator.page(1)
	except EmptyPage:
		languages = paginator.page(paginator.num_pages)

	return render(request, 'thingstodo/language_master_list_page.html', { 'languages': languages })

def category_add(request):
	
	if request.method == 'GET':
		# lang_codes = list(LangaugeMaster.objects.values_list('language_code'))
		# li_code = [code[0] for code in lang_codes ]
		return render(request,'thingstodo/category_add_page.html')
	
	elif request.method == 'POST':
		name = str(request.POST.get('name'))
		localized_name = request.POST.get('localized_name')
		localized_name_ar = request.POST.get('localized_name_ar')
		localized_name_fr = request.POST.get('localized_name_fr')

		# language_code = request.POST.get('language_code')
		# if language_code == None:
		#     return redirect('add_page')
		
		# doc = LangaugeMaster.objects.get(language_code=language_code)
		# language_id = doc.id
		query_obj = ThingsToDoCategory.objects.filter(name=name)
		query_obj_t = ThingsToDoCategory.objects.all()
		name_li = [item.name for item in query_obj_t]
		# lang_id_li = []
		localized_name_li = [item.localized_name for item in query_obj_t]
		localized_name_ar_li = [item.localized_name_ar for item in query_obj_t]
		localized_name_fr_li = [item.localized_name_fr for item in query_obj_t]
		
		if name not in name_li and localized_name not in localized_name_li and localized_name_ar not in localized_name_ar_li and localized_name_fr not in localized_name_fr_li:
			obj = ThingsToDoCategory.objects.create(name=name,localized_name=localized_name,localized_name_ar=localized_name_ar,localized_name_fr=localized_name_fr)
			category_list = ThingsToDoCategory.objects.all()
			page = request.GET.get('page', 1)
			paginator = Paginator(category_list, 10)
			try:
				categories = paginator.page(page)
			except PageNotAnInteger:
				categories = paginator.page(1)
			except EmptyPage:
				categories = paginator.page(paginator.num_pages)
			return render(request, 'thingstodo/category_list_page.html', { 'categories': categories})
		else:
			return redirect('category_add')
		
		   
def category_edit(request):
	# lang_codes = list(LangaugeMaster.objects.values_list('language_code'))
	# li_code = [code[0] for code in lang_codes]
	if request.method == 'GET':
		try:
			c_id = request.GET.get('id')
			obj = ThingsToDoCategory.objects.get(id=c_id)
			name = obj.name
			localized_name = obj.localized_name
			localized_name_ar = obj.localized_name_ar
			localized_name_fr = obj.localized_name_fr
			
			return render(request,'thingstodo/category_edit.html',{'id':c_id,'name':name,'localized_name':localized_name,'localized_name_ar':localized_name_ar,'localized_name_fr':localized_name_fr})
		except:
			traceback.print_exc()
			return redirect('thingstodo_list')
		
	elif request.method == 'POST':
		
		try:
			c_id = request.POST.get('id')
			edit_localized_name = request.POST.get('localized_name')
			edit_localized_name_ar = request.POST.get('localized_name_ar')
			edit_localized_name_fr = request.POST.get('localized_name_fr')
			ThingsToDoCategory.objects.using('default').filter(id=c_id).update(localized_name=edit_localized_name,localized_name_ar=edit_localized_name_ar,localized_name_fr=edit_localized_name_fr)			
		
			return redirect('category_list')
		except:
			traceback.print_exc()
			return redirect('category_list')
		
	   
def active_inactive(request):
	
	id = request.POST.get('id')
	obj = ThingsToDoCategory.objects.using('default').get(id=id)
	# obj = ThingsToDoCategory.objects.get(id=id)
	val = obj.is_active
	status = 0
	if val == 1:
		obj.is_active = 0
		status = 0
	else:
		obj.is_active = 1 
		status = 1 
	obj.save()
	data = {
		'status':status
	}
	return JsonResponse({'data': json.loads(json_util.dumps(data))})

def search_cities(request):
	st = request.GET.get('in_put')
	country_id = request.GET.get('country_query_id')
	country_id = int(country_id) if country_id else None
	query = {'city':{'$regex':st,'$options':'i'}, 'country_id':country_id} if country_id else {'city':{'$regex':st,'$options':'i'}}        
	obj = city_col.find(query)
	result_list =  []
	if 'request_from' in request.GET:
		result_list = [{'id':int(doc['_id']), 'value':doc['city'].strip().title(),'name_ar':doc.get('city_ar')} for doc in obj]
	else:
		for doc in obj:
			# t = (int(doc['_id']), unicodedata.normalize('NFKD', doc['city'].strip().title()).encode('ascii', 'ignore'))
			city_di = {'id':int(doc['_id']), "value":doc['city'].strip().title()+" - "+doc['country'].strip().title()}
			result_list.append(city_di)
	return  JsonResponse(result_list, safe=False)

def country_popup(request):
	st=request.GET.get('in_put')
	city_country_dict=city_col.find_one({'city':st},{'country':1,'country_id':1})
	return JsonResponse(city_country_dict,safe=False)

def search_states(request):
	st = request.GET.get('in_put')
	obj = state_col.find({'state':{'$regex':st,'$options':'i'}})
	result_list =  []
	for doc in obj:
		t = {'id':int(doc['_id']), 'value': doc['state'].strip().title()}
		result_list.append(t)
	return  JsonResponse(result_list, safe=False)


def search_countries(request):
	
	st = request.GET.get('in_put')
	print(st)
	obj = country_col.find({'country':{'$regex':st,'$options':'i'}})
	result_list =  []
	for doc in obj:
		t = {"id":int(doc['_id']), "value":doc['country'].strip().title(),"name_ar":doc.get('name_ar')}
		result_list.append(t)
		# result_list.append(doc['country'])
	return  JsonResponse(result_list, safe=False)

def search_area(request):
	search_string =  request.GET.get('search_string')
	country_query_id = request.GET.get('country_query_id')
	query = {'area':{'$regex':search_string,'$options':'i'}, 'country_id':int(country_query_id)} if country_query_id else {'area':{'$regex':search_string,'$options':'i'}}
	area_obj = area_col.find(query, {'_id':1, 'area':1})
	area_data = [{'id':int(area['_id']), 'value':area['area'].strip().title()} for area in area_obj] if area_obj else []
	return JsonResponse(area_data, safe=False)

def thingstodo_city_list(request):
	city_id = str(request.GET.get('city_id'))
	page = int(request.GET.get('page', 0))
	city_name = ""
	data_obj = ""
	projections =  {'_id':0,'things_todo_id':1,'title_description.en.name':1,'tripadvisor_city_name':1,'category.en.localized_name':1,'search_destination_id':1,'tripadvisor_id':1,'type':1,'is_active':1,'is_popular':1, "rehlat_city_name":1}
	entries_per_page = int(request.GET.get('entries_per_page', 20))  # default to 20 if not specified
	if city_id != 'null':
		len_data_obj = ttd_collection.find({'city_id':int(city_id)}).count()
		data_obj = ttd_collection.find({'city_id':int(city_id)}, projections).sort('is_active',-1).skip(page*entries_per_page).limit(entries_per_page)
		obj = city_col.find_one({'_id':int(city_id)})
		city_name = obj['city'] 
	
	paginator_count = range(1, int(len_data_obj/entries_per_page)+1)

	paginator = Paginator(list(data_obj), entries_per_page)
	try:
		thingstodo_docs = paginator.page(page)
	except PageNotAnInteger:
		thingstodo_docs = paginator.page(1)
	except EmptyPage:
		thingstodo_docs = paginator.page(paginator.num_pages) 
	
	start = (page * entries_per_page)+1
	end = (page+1) * entries_per_page
	if end > len_data_obj:
		end = len_data_obj
	page_options = [10,20,50,100]
	return render(request,'thingstodo/listing_page.html', {'page_no':page,'city_id':city_id,'city':city_name,'thingstodo_docs': thingstodo_docs, "paginator_count":paginator_count, 'data_obj_count':len_data_obj,'start':start,'end':end,'entries_per_page':entries_per_page,'page_options':page_options})


def seo_tag_mapping_list(request):
	
	data_obj = list(seo_destination_mapping.find({}))
	page = request.GET.get('page', 1)
	paginator = Paginator(data_obj, 10)
	try:
		seo_docs = paginator.page(page)
	except PageNotAnInteger:
		seo_docs = paginator.page(1)
	except EmptyPage:
		seo_docs = paginator.page(paginator.num_pages)

	return render(request, 'thingstodo/seo_tag_mapping_listing_page.html', {'seo_docs': seo_docs})

def seo_tag_mapping_add(request):
	
	try:
		if request.method == "GET":
			seo_type_list = seo_destination_mapping.distinct('seo_type')
			return render(request, 'thingstodo/seo_tag_mapping_edit_page.html',{'seo_type_list':seo_type_list})
		
		elif request.method == "POST":
			is_active = 0 
			if 'is_active' in request.POST:
				is_active = 1 
			seo_type = request.POST.get('seo_type')
			seo_valid_tag = request.POST.get('seo_valid_tag')

			seo_destination_mapping.insert_one({
				"seo_type" : seo_type,
				"seo_valid_tags" : seo_valid_tag,
				"created_by" : 1,
				"updated_by" : 1,
				"created_at" : datetime.now(),
				"updated_at" : datetime.now(),
				"is_active" : is_active
			})
			return redirect('seo_tag_mapping_list')
	except:
		print(traceback.print_exc())
		return redirect('seo_tag_mapping_add')

def seo_tag_mapping_edit(request):
	
	try:
		if request.method == "GET":
			seo_type = request.GET.get('type')
			data = seo_destination_mapping.find_one({'seo_type':seo_type},{'_id':0})
			return render(request, 'thingstodo/seo_tag_mapping_edit_page.html',{'data':data,'type':seo_type})
		else:
			is_active = 0 
			if 'is_active' in request.POST:
				is_active = 1 
			prev_seo_type = str(request.POST.get('type'))[2:]
			updated_seo_type = request.POST.get('seo_type')
			seo_valid_tag = request.POST.get('seo_valid_tag')
			seo_destination_mapping.update_one({'seo_type':prev_seo_type},{'$set':{'seo_type':updated_seo_type,'seo_valid_tags':seo_valid_tag,'updated_at':datetime.now(),'is_active':is_active}})
			return redirect('seo_tag_mapping_list')
	except:
		return redirect('seo_tag_mapping_edit')


def seo_tag_mapping_status_update(request):
	
	seo_type = str(request.POST.get('seo_type'))
	obj = seo_destination_mapping.find_one({'seo_type':seo_type})
	value = obj['is_active']
	status = 0
	if value == 1:
		seo_destination_mapping.update_one({'seo_type':seo_type},{'$set':{'is_active':0}})
		status = 0
	else:
		seo_destination_mapping.update_one({'seo_type':seo_type},{'$set':{'is_active':1}})
		status = 1 
	data = {
		'status':status
	}
	return JsonResponse({'data': json.loads(json_util.dumps(data))})


def thingstodo_is_popular_update(request):
	
	try:
		ttd_id = str(request.POST.get('ttd_id'))
		ttd_id = ttd_id.split('_is')[0]
		obj = ttd_collection.find_one({'things_todo_id': ttd_id})
		value = obj['is_popular'] if "is_popular" in obj else None
		if value and value == 1:
			ttd_collection.update_one({'things_todo_id': ttd_id},{'$set':{'is_popular':0}})
		else:
			ttd_collection.update_one({'things_todo_id': ttd_id},{'$set':{'is_popular':1}})
		return JsonResponse({'status':"success"})
	except:
		print(traceback.print_exc())
		return JsonResponse({"status":"failure"}) 


def get_searchdestination_list(request):
	"""
	 Function to get matching set of searchdestination names(along with its id's) with the given 'input' word.
	
	Parameters:
	request object: Get request having of the input word with key name 'in_put', searchdestination Type with key name 'sd_type'.
	
	 Returns:
	JsonResponse: Json of searchdestination id and names.
 
	  """
	input_term = str(request.GET.get('in_put'))
	sd_type = str(request.GET.get('sd_type'))
	query = {'name':{'$regex':input_term,'$options':'i'},'type':sd_type}
	projections = {'id':1,'name':1,'_id':0,'type':1}
	sd_obj = list(search_destination.find(query,projections))
	result_list =  []
	for doc in sd_obj:
		item = {'id':doc['id'], "value":doc['name'].strip().title()}
		result_list.append(item)
	return  JsonResponse(result_list, safe=False)

def upload_files_add(request):
	
	"""
	 Function to upload thingstodo_data files.
	
	Saves the uploaded file in static folder and saves the path in the 'UploadFiles' collection with type and SearchDestinationID and status as 'pending'.
 
	Parameters:
	request object: Get request having of the input parameters of  'File' to get uploaded file, 'searchdestinationId' and  Type('COUNTRY/'CITY).
	
	 Returns:
	JsonResponse: Json of status of the uploaded file.
 
	  """
	if request.method == "GET":
		return render(request, 'thingstodo/thingstodo_file_upload_add_page.html',{})
	else:
		try:
			search_destination_id = int(request.POST.get('search_destination_id'))
			sd_type = str(request.POST.get('sd_type'))
			sd_name = str(request.POST.get('sd_name'))
			upload_file = request.FILES['file']
			file_name = request.FILES['file'].name
			file_extension = file_name.split('.')[-1]
			if file_extension == 'xlsx' or file_extension == 'xls':
				df = pd.read_excel(upload_file)
				column_list = list(df)
				# column_li = ['Name', 'NameArabic','NameFrench', 'Type', 'City', 'Country', 'State', 'Description', 'DescriptionArabic', 'ShortDescription', 'ShortDescriptionArabic', 'Category', 'Address', 'Timezone', 'Phone', 'Latitude', 'Longitude', 'Rating', 'AverageTimeToSpend', 'is_popular']
				if "Name" in column_list and "Type" in column_list and "Description" in column_list:
					file_path = MEDIA_ROOT + '/searchdestination/thingstodo/'
					if not os.path.exists(file_path):
						os.makedirs(file_path)
					file_name = "upload_thingstodo_"+sd_name+"_"+str(datetime.strftime(datetime.now(),'%Y-%m-%d')) +"_.xlsx"
					file_name = file_name.replace(' ','_')
					final_path = file_path + file_name
					path = default_storage.save(final_path,upload_file)
					os.chmod(path,0777)
					filepath = path.split('/b2cadmintool/')[1]
					insert_data = {"file_path":filepath,"status":"pending","search_destination_id":search_destination_id,'search_destination_name':sd_name,
									'file_name':file_name,"type":sd_type,"created_by":int(str(request.session['userid'])),"created":datetime.now()}
					ttd_uploaded_files_col.insert_one(insert_data)
					return JsonResponse({"status":"success"})
				else:
					return JsonResponse({"status":"wrong file provided"})
			else:
				return JsonResponse({"status":"wrong file extension"})
		except:
			print(traceback.print_exc())
			return JsonResponse({"status":"error","error_message":traceback.print_exc()})
   
def upload_ttd_list(request):
	"""
	 Function to Return list of Documents from 'Thingstodo_Upload_files' collection.
	 
	Parameters:
	request object: Get request of having parameters 'page' which is page number.
	
	 Returns:
	HttpResponse: Returns list of documents and renders in 'upload_files_list.html' file.
 
	  """
	data_obj = list(ttd_uploaded_files_col.find({}))
	page = request.GET.get('page', 1)
	paginator = Paginator(data_obj, 10)
	try:
		data = paginator.page(page)
	except PageNotAnInteger:
		data = paginator.page(1)
	except EmptyPage:
		data = paginator.page(paginator.num_pages)
	return render(request, 'thingstodo/upload_files_list.html', {'data': data})

def save_data_from_uploaded_files(request):
	"""
	API to retrieve and save data from uploaded Files.
 
	 Fetchs data from the uploaded files (by looping all files which are pending) which are having status as 'pending' and convert data to 
	'thingstodo_master' collection data structure(Json/dictionary) and insert the documents/records into the 
	'thingstodo_master' collection.After finishing of each file update status as 'completed'.
	 
	Parameters:
	request object: Get request object.
	
	 Returns:
	HttpResponse: Returns status of the uploaded files.
 
	  """
	try:
		path = ''
		files_details = list(ttd_uploaded_files_col.find({'status':'pending'}))
		things_todo_id_list = ttd_collection.distinct('things_todo_id')
		category_data = list(ThingsToDoCategory.objects.all().values())
		# category_name_di = { di.get('name'):str(di.get('id'))+'&&&'+di.get('localized_name_ar')+'&&&'+di.get('localized_name_fr') for di in category_data }
		category_name_di = { di.get('name').lower(): { 'en':{'id':di.get('id'),'name':di.get('name'),'localized_name':di.get('localized_name')}, 'ar':{'id':di.get('id'),'name':di.get('name'),'localized_name':di.get('localized_name_ar')}, 'fr':{'id':di.get('id'),'name':di.get('name'),'localized_name':di.get('localized_name_fr')} } for di in category_data }
		for document in files_details:
			result_list = []
			search_destination_id = document.get('search_destination_id')
			sd_obj = search_destination.find_one({'id': search_destination_id})
			city_name,city_id,country_id,country_code,country_name = None,None,None,None,None
			if sd_obj:
				country_code,country_name = sd_obj.get('CountryCode'),sd_obj.get('country')
				if sd_obj.get('type') == "CITY":
					city_name = sd_obj.get('name')
					city_obj = city_col.find_one({"city": city_name.lower(),"country": country_name.lower()})
					if city_obj:
						city_id,city_name,country_name,country_id = city_obj.get('_id'),city_obj.get('city'),city_obj.get('country'),sd_obj.get('country_id')
					else:
						city_id,country_id = sd_obj.get('city_id'),sd_obj.get('country_id')
						city_name = sd_obj.get('name') if city_id else None
				else:
					country_name = sd_obj.get('name')
					country_obj = country_col.find_one({'country':country_name}) if country_name else None
					if country_obj:
						country_id,country_name = country_obj.get('country_id'),country_obj.get('country')
						country_code = country_obj.get('alpha_2_code') if not country_code else country_code
					else:
						country_id = sd_obj.get('country_id')
	  
			root_path = MEDIA_ROOT.split('/static/')[0]
			path = document.get('file_path')
			filepath = root_path+"/"+path
			file_df = pd.read_excel(filepath)
			key_list = file_df.keys()
			
			for slno,name,name_ar,name_fr,Type,city,country,state,description,description_arabic,description_fr,s_desc,s_desc_ar,s_desc_fr,category,address,timezone,phone,latitude,longitude,rating,avg_time,is_popular,blurb,blurb_ar,blurb_fr\
				in zip(file_df['slno'],file_df['Name'],file_df['NameArabic'],file_df['NameFrench'],file_df['Type'],file_df['City'],file_df['Country'],file_df['State'],file_df['Description'],file_df['DescriptionArabic'],file_df['DescriptionFrench'],\
				file_df['ShortDescription'],file_df['ShortDescriptionArabic'],file_df['ShortDescriptionFrench'],file_df['CategoryNameEnglish'],file_df['Address'],file_df['Timezone'],file_df['Phone'],file_df['Latitude'], \
				file_df['Longitude'],file_df['Rating'],file_df['AverageTimeToSpend'],file_df['is_popular'],file_df['Blurb'],file_df['Blurb_ar'],file_df['Blurb_fr']):
				
				if not type(name) is float:
					strip_li = [search_destination_id,name,name_ar,name_fr,Type,city,country,state,category]
					for i in range(len(strip_li)):
						if strip_li[i]:
							if i == 1 : strip_li[i] = str(strip_li[i]).strip().title()
							if i == 4 : strip_li[i] = str(strip_li[i]).strip().upper()
							if i not in [1,4] : strip_li[i] = str(strip_li[i]).strip()
							  
					search_destination_id,name,name_ar,name_fr,Type,city,country,state,category = strip_li
					# letters = string.digits + string.ascii_uppercase+string.ascii_lowercase
					letters = string.digits + string.ascii_lowercase + string.digits + string.ascii_lowercase

					ttd_id = ''.join(random.choice(letters) for i in range(10))
					while ttd_id in things_todo_id_list:
						ttd_id = ''.join(random.choice(letters) for i in range(10))
	 
					category_result = {'en':[],'ar':[],'fr':[]}
					if category:
						if category.lower() in category_name_di:
							category_result = category_name_di.get(category.lower())
	   
					explore_url = None
					if name and city and country:
						explore_url = slugify('{0} {1} {2}'.format(name, city, country))
			
					state_id = state_col.find_one({'state':state.lower()},{'_id':1})
					is_popular = 1 if is_popular else 0
					new_record={
					'things_todo_id': ttd_id,
					'city_id':city_id,
					'ID':{'r_province_id':state_id,'r_area_id':None,'location_id':None,'r_city_id': city_id,'r_country_id':country_id },
					'country_id':country_id,
					'address_details':{'en':{'website':"",'street1':"",'street2':"",'address_string':address,'phone':phone,'postal_code':"",
											'timezone':timezone,'city': city,'country':country,
											'longitude':longitude,'latitude': latitude,'state': state,'email':""},
									'fr':{'street1':"",'street2':"",'address_string':"",
											'city':"",'country':"",'state':""},
									'ar':{'street1':"",'street2':"",'address_string':"",
											'city':'','country': '','state':''}},
					'subcategory':{'en':[],'fr':[],'ar':[]},
					'rating':{'rating': rating,'review_rating_count':{'1':"",'2':"",'3':"",'4':"",'5':""},'num_of_reviews':"",'rating_image_url':""},
					'tripadvisor_id':"",
					'tripadvisor_rank':"",
					'ancestors':{'en':{'province':{"location_id":"","name":""},'city':{"location_id":"","name":""},'country':{"location_id":"","name":""},'region':{"location_id":"","name":""},'municipality':{"location_id":"","name":""},'state':{"location_id":"","name":""}},
								'fr':{'province':{"location_id":"","name":""},'city':{"location_id":"","name":""},'country':{"location_id":"","name":""},'region':{"location_id":"","name":""},'municipality':{"location_id":"","name":""},'state':{"location_id":"","name":""}},
								'ar':{'province':{"location_id":"","name":""},'city':{"location_id":"","name":""},'country':{"location_id":"","name":""},'region':{"location_id":"","name":""},'municipality':{"location_id":"","name":""},'state':{"location_id":"","name":""}}},
					'open_close':{'sunday':[{'close':"",'open':"",'isopen':0,'is24hours':0}],'monday':[{'close':"",'open':"",'isopen':0,'is24hours':0}],'tuesday':[{'close':"",'open':"",'isopen':0,'is24hours':0}],'wednesday':[{'close':"",'open':"",'isopen':0,'is24hours':0}],'thursday':[{'close':"",'open':"",'isopen':0,'is24hours':0}],'friday':[{'close':"",'open':"",'isopen':0,'is24hours':0}],'saturday':[{'close':"",'open':"",'isopen':0,'is24hours':0}]},
					'is_timing_available':0,					
					'neighbourhood_info':{'en':[],'fr':[],'ar':[]},
					'trip_types':{'en':[],'fr':[],'ar':[]},
					'explore_url':explore_url,
					'category':category_result,
					'ranking_data':{'en':{'ranking_string':"",'ranking':"",'geo_location_id':"",'geo_location_name':"",'ranking_out_of':""},
									'fr':{'ranking_string':"",'ranking':"",'geo_location_id':"",'geo_location_name':"",'ranking_out_of':""},
									'ar':{'ranking_string':"",'ranking':"",'geo_location_id':"",'geo_location_name':"",'ranking_out_of':""}},
					'is_active':1,
					'groups':{'en':[],'fr':[],'ar':[]},
					'prices':{'book_now_url':"",'r_booking_note':"",'r_ticket_prices':"",'r_entry_ticket':"",'vendor_prices':[],
							'book_price':""},
					'tripadvisor_city_id':"",
					'title_description':{'en':{'description':description,'r_shortdescription': s_desc,'r_description':description,
											'r_avg_time_to_spend':avg_time,'r_title':name,'name': name,'blurb':blurb },
										'fr':{'description':description_fr,'r_shortdescription':s_desc_fr,'r_description':description_fr,
											'r_avg_time_to_spend':avg_time,'r_title':name_fr,'name':name_fr,'blurb':blurb_fr},
										'ar':{'description':description_arabic,'r_shortdescription': s_desc_ar,'r_description':description_arabic,
											'r_avg_time_to_spend':avg_time,'r_title':name_ar,'name': name_ar,'blurb':blurb_ar}},
					'tripadvisor_city_name':"",
					'country_code':country_code,
					"search_destination_id":int(search_destination_id), 
					"rehlat_city_name":city_name,
					"rehlat_country_name":country_name,
					"created_by": request.session.get('name'),
					"created_on": datetime.now(),
					"type": Type,
					"is_popular": is_popular,
					'add_type':'bulk_upload',
					"nearbyttd": []
					}
					result_list.append(new_record)
				else:      
					if math.isnan(name):
						print('No Name, Name is Mandatory')
					ttd_upload_files_error_logs.insert_one({'file_path':path,'error':'No things_todo Name in the record','record_serial_no':slno,'created':datetime.now()})
				  
			ttd_collection.insert_many(result_list)
			ttd_uploaded_files_col.update_one({'_id':document['_id']},{'$set':{'status':'completed'}})
	
		return JsonResponse({'status':'success'})
	except:
		print(traceback.print_exc())
		ttd_upload_files_error_logs.insert_one({'file_path':path,'error':traceback.format_exc(),'record_serial_no':'All records','created':datetime.now()})
		return JsonResponse({'status':'error'})
