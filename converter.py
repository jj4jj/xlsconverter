import os
import sys
import xlrd
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append('./python')
#rsc=__import__('resconvert')
def protocompile(protoname):
	execString = 'protoc --proto_path=./meta ./meta/'+protoname+' --python_out=python --cpp_out=cpp';
	print("system is exec :'"+execString+"' , pls waiting ...")
	os.system(execString)

def get_token_list(meta_desc,strval):
	names = strval.split(".")
	#####################################
	#token list
	token_list = []
	current_desc = meta_desc
	#print(meta_desc.name)
	#print(names)
	#print("----------------")
	for name in names:
		token={}
		desc = name.split("#")
		if(len(desc) > 1):
			token["name"] = desc[0]
			token["idx"] = int(desc[1])
		else:
			token["name"] = name
			token["idx"] = 0
		#############################
		#get cname meta
		#_CName nested type
		#print("================")
		#print(current_desc.name,current_desc.full_name)
		#print(dir(current_desc))
		cname_desc = current_desc.nested_types_by_name["_CName"]
		if(cname_desc != None):
			for cname_field in cname_desc.fields:
				if	cname_field.default_value == token["name"]:
					token["name"] = cname_field.name
					break
		field_desc = current_desc.fields_by_name[token["name"]]
		if(field_desc != None):
			current_desc = field_desc.message_type
		token_list.append(token)
	#####################################
	return token_list


'''
	TYPE_DOUBLE         = 1,   // double, exactly eight bytes on the wire.
    TYPE_FLOAT          = 2,   // float, exactly four bytes on the wire.
    TYPE_INT64          = 3,   // int64, varint on the wire.  Negative numbers
                               // take 10 bytes.  Use TYPE_SINT64 if negative
                               // values are likely.
    TYPE_UINT64         = 4,   // uint64, varint on the wire.
    TYPE_INT32          = 5,   // int32, varint on the wire.  Negative numbers
                               // take 10 bytes.  Use TYPE_SINT32 if negative
                               // values are likely.
    TYPE_FIXED64        = 6,   // uint64, exactly eight bytes on the wire.
    TYPE_FIXED32        = 7,   // uint32, exactly four bytes on the wire.
    TYPE_BOOL           = 8,   // bool, varint on the wire.
    TYPE_STRING         = 9,   // UTF-8 text.
    TYPE_GROUP          = 10,  // Tag-delimited message.  Deprecated.
    TYPE_MESSAGE        = 11,  // Length-delimited message.

    TYPE_BYTES          = 12,  // Arbitrary byte array.
    TYPE_UINT32         = 13,  // uint32, varint on the wire
    TYPE_ENUM           = 14,  // Enum, varint on the wire
    TYPE_SFIXED32       = 15,  // int32, exactly four bytes on the wire
    TYPE_SFIXED64       = 16,  // int64, exactly eight bytes on the wire
    TYPE_SINT32         = 17,  // int32, ZigZag-encoded varint on the wire
    TYPE_SINT64         = 18,  // int64, ZigZag-encoded varint on the wire
'''
def fill_table_row_field(obj,field_desc,value):
	field = field_desc[0]
	fieldObjDesc = obj.DESCRIPTOR.fields_by_name[field["name"]]
	attrType = fieldObjDesc.type
	#print(attrType)
	print("set object value : "+obj.DESCRIPTOR.name+"."+field['name']+"#"+str(field['idx'])+"="+value)
	if(field['idx'] > 0):
		arrayObj = getattr(obj,field["name"])
		while(len(arrayObj) < field["idx"]):
			if(fieldObjDesc.has_default_value):
				arrayObj.extend(fieldObjDesc.default_value)
			elif(attrType < 9 or attrType >= 13 and attrType <= 18):
				arrayObj.extend([0])
			elif(attrType == 9 ):
				arrayObj.extend([""])
			elif(attrType == 11):
				arrayObj.add()
			else:
				print("FATAL ERROR Known attr type ="+str(attrType))
				arrayObj.add()
	if(len(field_desc) == 1):
		#9 is string type
		if(attrType != 9):
			if(field["idx"] > 0):
				arrayObj = getattr(obj,field['name'])
				arrayObj[field["idx"]-1] = int(float(value))	
				#setattr(obj,field_desc[0]['name'],int(float(value)))
			else:
				setattr(obj,field_desc[0]['name'],int(float(value)))
		#string
		else:
			if(field["idx"] > 0):
				arrayObj = getattr(obj,field['name'])
				arrayObj[field["idx"]-1] = value	
				#setattr(obj,field_desc[0]['name'],int(float(value)))
			else:
				setattr(obj,field['name'],value)
	else:
		fieldObj = getattr(obj,field["name"])
		#array
		if(field["idx"] > 0):
			fill_table_row_field(fieldObj[field["idx"]-1],field_desc[1:],value)
		else:
			fill_table_row_field(fieldObj,field_desc[1:],value)
#*.xls *.proto meta *.bin
def convertxls(xls,convertparam):
	proto = convertparam[0]
	meta = convertparam[1]
	binf = convertparam[2]
	proto_mod_name = proto.split(".")[0]+"_pb2"
	proto_mod = __import__(proto_mod_name)
	objMeta = getattr(proto_mod,meta)
	desc = objMeta.DESCRIPTOR
	xls_column_token_map = {};
	tableObjTypeName = meta+'Table';
	tableObjProtoType = getattr(proto_mod,tableObjTypeName)
	#print(dir(tableObjProtoType))
	tableObj = tableObjProtoType()
	xlsFilePath = "./xls/"+xls
	binFilePath = "./data/"+binf
	print('convert '+xlsFilePath+' to '+binFilePath+' ...')
	xlsData = xlrd.open_workbook(xlsFilePath)
	for table in xlsData.sheets():
		for row in range(table.nrows):
			if row > 0:
				entry = tableObj.list.add()
			for col in range(table.ncols):
				if row == 0:
					xls_column_token_map[col] = get_token_list(desc,unicode(table.cell(row,col).value))
				else:
					fill_table_row_field(entry,xls_column_token_map[col],unicode(table.cell(row,col).value))
	f=open(binFilePath,"wb")
	f.write(tableObj.SerializeToString())
	f.close()

import datetime,time
def convert_main():
	# *.xls:*.proto:meta
	convertmap = {};
	convertmap_file = open("convertmap.conf")
	for line in convertmap_file:
		attrs = line.split(":")
		attrs.append(attrs[2]+"Table.bin")
		print(attrs)
		convertmap[attrs[0]] = attrs[1:]
	convertmap_file.close()
	cpp_include_file = open("./cpp/include.h","w+")	
	cpp_include_file.write("#pragma once\n")
	cpp_include_file.write("//protobufer generate code include file . don't edit it !\n")
	now = datetime.datetime.now()
	cpp_include_file.write("//generate time :"+str(now)+"\n")

	for xls in convertmap.keys():
		#generate proto buffer src code
		protocompile(convertmap[xls][0])
		#append_cpp_include
		cpp_include_file.write('#include "'+convertmap[xls][0].split(".")[0]+'.pb.h"\n')		
		#convert to data
		convertxls(xls,convertmap[xls])
	cpp_include_file.write('\n')	
	cpp_include_file.close()



##########################################################################################################
if len(sys.argv) > 1 and sys.argv[1] == 'run' :
	print("welcome using game conf res loader tools  !")
	convert_main()


