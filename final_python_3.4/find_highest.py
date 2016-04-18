

#This program finds the highest means of percentage correct for given years and stat weights


import json
import copy



def main():
	#list_keys =   ["pts","shooting","freethrow","3shooting","to","dreb", "ast", "stl", "oreb", "blk","def_ef", "off_ef" ]
	#list_keys = ["pts","shooting","to","dreb", "ast", "oreb", "blk","def_ef", "off_ef" ]
	#list_keys = ["pts","shooting","freethrow","dreb", "oreb", "blk","def_ef", "off_ef" ]
	list_keys = ["pts","shooting", "dreb", "ast", "stl", "blk","def_ef", "off_ef","oreb" ]
	#list_keys = ["pts" ,"shooting", "dreb", "def_ef", "off_ef"]'
	
	stat_file = input("File with stats:")
	
	with open(stat_file) as data_file:
		data_pts = json.load(data_file)
	#print (len(data_pts))
	
	
	results = []
	for per_list,pt in data_pts:
		my_dict = {}
		mean = (per_list[0] + per_list[1] + per_list[2] ) / 3
		#var = ((mean - per_list[0])**2  + (mean - per_list[1])**2 + (mean - per_list[2])**2)
		per_range = max(per_list) - min(per_list)
		for k in pt:
			my_dict[list_keys[int(k)]] = pt[k]
		my_copy = copy.deepcopy(my_dict)
		copy_list = copy.deepcopy(per_list)
		if per_range < 0.20:
			results.append((mean,per_range,copy_list,my_copy))
		
	results.sort(reverse = True, key = lambda x: x[0])
	
	print ("Percent Correct")
	print ("Mean\tRange\tStat Weights")
	for mean,per,per_range,data in results[0:20]:
		print ((round(mean*100,2)),'\t',(round(per*100,2)),'\t',data)
		print ()
		
main()