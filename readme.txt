new design .

requiration:
xls file to protobuf data represitation .

convert on xls work flow as follow :
	read xls first line create map xls col-> proto message field .
	read others lines to add table message .


every messsage define as follow:

message ComposeType
{
	message _CName
	{
		optional	string	id 	= 1[default="ID"];
	};
	required	int32	id	=	1;
};

message Meta
{
	message _PrimaryKey
	{
		optional int32		id = 1;
	};
	message _CName
	{
		optional string		id = 1[default="名字"];
		optional string		ct = 2[default="复合"];
		optional string		arr = 3[default="数组"];
		optional string		arrct = 4[default="复合数组"];
	};
	required	int32	id	=	1;
	optional	ComposeType	ct 	=	2;
	repeated	int32	arr	=	3;
	repeated	ComposeType	arrct	=	4;
};

message MetaTable
{
	repeated Meta	rows;
};


XLS	file
名字	复合.ID		数组#1	数组#2	复合数组#1.ID	复合数组#2.ID
1	2		3	4	5		6


//--------------------------------------------------------------------
the tools will read xls file
output bin file to dir
if nessisery , it will create a window UI.


dir
	xls
	meta
	tools

convertmap.conf <*.proto->*.xls->*.bin >
converter.exe



//--------------------------------------------------------------------
converter
	read map.conf
	import meta need
	foreach xls convert to bin
	

convert
	read xls file 
		create proto message table
		for first row :
			build column map
		create proto message
		add message to table
	back processing
	output	
buil conumn map
	for each column text
	split them to token with "."
		token is name
			 token#digit
create proto message				
	message type -> New message
	foreach column set message field .
		addr -> value(text)








	

