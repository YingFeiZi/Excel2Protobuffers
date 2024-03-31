
import sys
import gen_python.Item_pb2 as ITEM

dataArray = ITEM.ITEMARRAY()


data0 = dataArray.rows.add()
data0.id = 1 
data0.name = "道具1" 
data0.nameId = 1 
data0.note = "说明111" 
data0.type = 31 
data0.subType = 1 
data0.exeType = 21 
data0.posType = 111.2222 
data0.useType = 1.1111 
data0.binding = 1 
data0.overlaying = 121 
data0.level = 111 
data0.quality = 1 
data0.beauty = 11 
data0.icon = 1290001 
data0.smallIcon = 1111111111 
data0.ismodel = 1 
data0.getway = "3#2#6" 
data0.callback = "1#2#1" 
data0.importance = "0.00001#0.0001#0.1" 
data0.belong = "a#b#c1" 
data0.partner = "1#0#1" 


data1 = dataArray.rows.add()
data1.id = 2 
data1.name = "道具2" 
data1.nameId = 2 
data1.note = "说明112" 
data1.type = 32 
data1.subType = 2 
data1.exeType = 22 
data1.posType = 112.2222 
data1.useType = 2.1111 
data1.binding = 2 
data1.overlaying = 122 
data1.level = 112 
data1.quality = 2 
data1.beauty = 12 
data1.icon = 1290002 
data1.smallIcon = 1111111112 
data1.getway = "3#2#5" 
data1.callback = "1#2#2" 
data1.importance = "0.00001#0.0001#0.1" 
data1.belong = "a#b#c2" 
data1.partner = "1#0#1" 


data2 = dataArray.rows.add()
data2.id = 3 
data2.name = "道具3" 
data2.nameId = 3 
data2.note = "说明113" 
data2.type = 33 
data2.subType = 3 
data2.exeType = 23 
data2.posType = 113.2222 
data2.useType = 3.1111 
data2.binding = 3 
data2.overlaying = 123 
data2.level = 113 
data2.quality = 3 
data2.beauty = 13 
data2.icon = 1290003 
data2.smallIcon = 1111111113 
data2.ismodel = 1 
data2.getway = "3#2#4" 
data2.callback = "1#2#3" 
data2.importance = "0.00001#0.0001#0.1" 
data2.belong = "a#b#c3" 
data2.partner = "1#0#1" 


data3 = dataArray.rows.add()
data3.id = 4 
data3.name = "道具4" 
data3.nameId = 4 
data3.note = "说明114" 
data3.type = 34 
data3.subType = 4 
data3.exeType = 24 
data3.posType = 114.2222 
data3.useType = 4.1111 
data3.binding = 4 
data3.overlaying = 124 
data3.level = 114 
data3.quality = 4 
data3.beauty = 14 
data3.icon = 1290004 
data3.smallIcon = 1111111114 
data3.getway = "3#2#3" 
data3.callback = "1#2#4" 
data3.importance = "0.00001#0.0001#0.1" 
data3.belong = "a#b#c4" 
data3.partner = "1#0#1" 


data4 = dataArray.rows.add()
data4.id = 5 
data4.name = "道具5" 
data4.nameId = 5 
data4.note = "说明115" 
data4.type = 35 
data4.subType = 5 
data4.exeType = 25 
data4.posType = 115.2222 
data4.useType = 5.1111 
data4.binding = 5 
data4.overlaying = 125 
data4.level = 115 
data4.quality = 5 
data4.beauty = 15 
data4.icon = 1290005 
data4.smallIcon = 1111111115 
data4.ismodel = 1 
data4.getway = "3#2#2" 
data4.callback = "1#2#5" 
data4.importance = "0.00001#0.0001#0.1" 
data4.belong = "a#b#c5" 
data4.partner = "1#0#1" 


data5 = dataArray.rows.add()
data5.id = 6 
data5.name = "道具6" 
data5.nameId = 6 
data5.note = "说明116" 
data5.type = 36 
data5.subType = 6 
data5.exeType = 26 
data5.posType = 116.2222 
data5.useType = 6.1111 
data5.binding = 6 
data5.overlaying = 126 
data5.level = 116 
data5.quality = 6 
data5.beauty = 16 
data5.icon = 1290006 
data5.smallIcon = 1111111116 
data5.getway = "3#2#1" 
data5.callback = "1#2#6" 
data5.importance = "0.00001#0.0001#0.1" 
data5.belong = "a#b#c6" 
data5.partner = "1#0#1" 


data6 = dataArray.rows.add()
data6.id = 7 
data6.name = "道具6" 
data6.nameId = 7 
data6.note = "说明116" 
data6.type = 36 
data6.subType = 6 
data6.exeType = 26 
data6.posType = 116.2222 
data6.useType = 6.1111 
data6.binding = 6 
data6.overlaying = 126 
data6.level = 116 
data6.quality = 6 
data6.beauty = 16 
data6.icon = 1290006 
data6.smallIcon = 1111111116 
data6.getway = "3#2#1" 
data6.callback = "1#2#6" 
data6.importance = "0.00001#0.0001#0.1" 
data6.belong = "a#b#c6" 
data6.partner = "1#0#1" 



with open('E:/CY/Unity/GitPro/Excel2Protobuffers/gen_bytes/Item.bytes', 'wb') as f:
	f.write(dataArray.SerializeToString())
