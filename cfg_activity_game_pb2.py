
import sys
import gen_python.cfg_activity_game_pb2 as CFG_ACTIVITY_GAME

dataArray = CFG_ACTIVITY_GAME.CFG_ACTIVITY_GAMEARRAY()


data0 = dataArray.rows.add()
data0.id = 10101 
data0.type = 1 
data0.name = "决战沙巴克" 
data0.sequence = 1 
data0.condition = 10050 
data0.weekDay.append(3)
data0.weekDay.append(6)
data0.time.append(20)
data0.time.append(0)
data0.colse_time.append(21)
data0.colse_time.append(0)
data0.showRewards.append("615")
data0.showRewards.append("10&513")
data0.showRewards.append("50&2102")
data0.showRewards.append("500")
data0.hyperlink = 7503 
data0.remind = 1 
data0.remindTime.append("19")
data0.remindTime.append("45&19")
data0.remindTime.append("55")
data0.info = "岁月不改当年激情，兄弟携手共战沙城！" 
data0.announce = "23" 
data0.show = 1 
data0.firstActivity.append(5)
data0.mergeActivity.append(5)
data0.showcondition = 1350004 
data0.mail = 534 
data0.tubiao = "icon_richanghd_07.png" 


data1 = dataArray.rows.add()
data1.id = 10201 
data1.type = 2 
data1.name = "封魔探宝" 
data1.sequence = 1 
data1.condition = 10050 
data1.weekDay.append(1)
data1.weekDay.append(2)
data1.weekDay.append(4)
data1.weekDay.append(5)
data1.time.append(20)
data1.time.append(0)
data1.colse_time.append(20)
data1.colse_time.append(15)
data1.showRewards.append("2102")
data1.showRewards.append("1&500")
data1.showRewards.append("1&501")
data1.showRewards.append("1")
data1.hyperlink = 1856 
data1.remind = 1 
data1.remindTime.append("19")
data1.remindTime.append("45&19")
data1.remindTime.append("55")
data1.info = "封魔密室宝箱现世，打开后获得大量资源！" 
data1.show = 1 
data1.firstActivity.append(1)
data1.firstActivity.append(2)
data1.firstActivity.append(4)
data1.firstActivity.append(5)
data1.mergeActivity.append(1)
data1.mergeActivity.append(2)
data1.mergeActivity.append(4)
data1.mergeActivity.append(5)
data1.showcondition = 10050 
data1.tubiao = "btn_gjgw_02.png" 


data2 = dataArray.rows.add()
data2.id = 10301 
data2.type = 3 
data2.name = "魔神入侵" 
data2.sequence = 1 
data2.condition = 10100 
data2.weekDay.append(1)
data2.weekDay.append(2)
data2.weekDay.append(3)
data2.weekDay.append(4)
data2.weekDay.append(5)
data2.weekDay.append(6)
data2.weekDay.append(7)
data2.time.append(12)
data2.time.append(0)
data2.colse_time.append(12)
data2.colse_time.append(10)
data2.showRewards.append("7")
data2.showRewards.append("300&499")
data2.showRewards.append("50000")
data2.hyperlink = 1858 
data2.remind = 1 
data2.remindTime.append("11")
data2.remindTime.append("45&11")
data2.remindTime.append("55")
data2.info = "魔神入侵行会领地，行会成员速速前往消灭！" 
data2.show = 1 
data2.firstActivity.append(1)
data2.firstActivity.append(2)
data2.firstActivity.append(3)
data2.firstActivity.append(4)
data2.firstActivity.append(5)
data2.firstActivity.append(6)
data2.firstActivity.append(7)
data2.mergeActivity.append(1)
data2.mergeActivity.append(2)
data2.mergeActivity.append(3)
data2.mergeActivity.append(4)
data2.mergeActivity.append(5)
data2.mergeActivity.append(6)
data2.mergeActivity.append(7)
data2.showcondition = 10100 
data2.tubiao = "icon_richanghd_24.png" 


data3 = dataArray.rows.add()
data3.id = 10302 
data3.type = 3 
data3.name = "魔神入侵" 
data3.sequence = 1 
data3.condition = 10100 
data3.weekDay.append(1)
data3.weekDay.append(2)
data3.weekDay.append(3)
data3.weekDay.append(4)
data3.weekDay.append(5)
data3.weekDay.append(6)
data3.weekDay.append(7)
data3.time.append(19)
data3.time.append(30)
data3.colse_time.append(19)
data3.colse_time.append(40)
data3.showRewards.append("7")
data3.showRewards.append("300&499")
data3.showRewards.append("50000")
data3.hyperlink = 1858 
data3.remind = 1 
data3.remindTime.append("19")
data3.remindTime.append("15&19")
data3.remindTime.append("25")
data3.info = "魔神入侵行会领地，行会成员速速前往消灭！" 
data3.show = 1 
data3.firstActivity.append(1)
data3.firstActivity.append(2)
data3.firstActivity.append(3)
data3.firstActivity.append(4)
data3.firstActivity.append(5)
data3.firstActivity.append(6)
data3.firstActivity.append(7)
data3.mergeActivity.append(1)
data3.mergeActivity.append(2)
data3.mergeActivity.append(3)
data3.mergeActivity.append(4)
data3.mergeActivity.append(5)
data3.mergeActivity.append(6)
data3.mergeActivity.append(7)
data3.showcondition = 10100 
data3.tubiao = "icon_richanghd_24.png" 


data4 = dataArray.rows.add()
data4.id = 10401 
data4.name = "锁妖塔" 
data4.sequence = 1 
data4.condition = 10060 
data4.weekDay.append(1)
data4.weekDay.append(2)
data4.weekDay.append(3)
data4.weekDay.append(4)
data4.weekDay.append(5)
data4.weekDay.append(6)
data4.weekDay.append(7)
data4.time.append(9)
data4.time.append(0)
data4.colse_time.append(21)
data4.colse_time.append(0)
data4.showRewards.append("7")
data4.showRewards.append("750&516")
data4.showRewards.append("20")
data4.hyperlink = 608 
data4.remind = 0 
data4.info = "集满boss能量，开启锁妖塔！" 
data4.show = 0 
data4.firstActivity.append(1)
data4.firstActivity.append(2)
data4.firstActivity.append(3)
data4.firstActivity.append(4)
data4.firstActivity.append(5)
data4.firstActivity.append(6)
data4.firstActivity.append(7)
data4.mergeActivity.append(1)
data4.mergeActivity.append(2)
data4.mergeActivity.append(3)
data4.mergeActivity.append(4)
data4.mergeActivity.append(5)
data4.mergeActivity.append(6)
data4.mergeActivity.append(7)
data4.showcondition = 10060 
data4.tubiao = "btn_gjgw_01.png" 


data5 = dataArray.rows.add()
data5.id = 10501 
data5.type = 4 
data5.name = "双倍押镖" 
data5.sequence = 1 
data5.condition = 10500 
data5.weekDay.append(1)
data5.weekDay.append(2)
data5.weekDay.append(3)
data5.weekDay.append(4)
data5.weekDay.append(5)
data5.weekDay.append(6)
data5.weekDay.append(7)
data5.time.append(11)
data5.time.append(0)
data5.colse_time.append(12)
data5.colse_time.append(0)
data5.showRewards.append("501")
data5.showRewards.append("100&500")
data5.showRewards.append("150&513")
data5.showRewards.append("5")
data5.hyperlink = 4147 
data5.remind = 1 
data5.remindTime.append("10")
data5.remindTime.append("45&10")
data5.remindTime.append("55")
data5.info = "11:00-12:00和21:00-22:00为双倍时间，期间押镖可以获得双倍奖励" 
data5.show = 1 
data5.firstActivity.append(1)
data5.firstActivity.append(2)
data5.firstActivity.append(3)
data5.firstActivity.append(4)
data5.firstActivity.append(5)
data5.firstActivity.append(6)
data5.firstActivity.append(7)
data5.mergeActivity.append(1)
data5.mergeActivity.append(2)
data5.mergeActivity.append(3)
data5.mergeActivity.append(4)
data5.mergeActivity.append(5)
data5.mergeActivity.append(6)
data5.mergeActivity.append(7)
data5.showcondition = 10500 
data5.tubiao = "btn_gjgw_04.png" 


data6 = dataArray.rows.add()
data6.id = 10502 
data6.type = 4 
data6.name = "双倍押镖" 
data6.sequence = 1 
data6.condition = 10500 
data6.weekDay.append(1)
data6.weekDay.append(2)
data6.weekDay.append(3)
data6.weekDay.append(4)
data6.weekDay.append(5)
data6.weekDay.append(6)
data6.weekDay.append(7)
data6.time.append(21)
data6.time.append(0)
data6.colse_time.append(22)
data6.colse_time.append(0)
data6.showRewards.append("501")
data6.showRewards.append("100&500")
data6.showRewards.append("150&513")
data6.showRewards.append("5")
data6.hyperlink = 4147 
data6.remind = 1 
data6.remindTime.append("20")
data6.remindTime.append("45&20")
data6.remindTime.append("55")
data6.info = "11:00-12:00和21:00-22:00为双倍时间，期间押镖可以获得双倍奖励" 
data6.show = 1 
data6.firstActivity.append(1)
data6.firstActivity.append(2)
data6.firstActivity.append(3)
data6.firstActivity.append(4)
data6.firstActivity.append(5)
data6.firstActivity.append(6)
data6.firstActivity.append(7)
data6.mergeActivity.append(1)
data6.mergeActivity.append(2)
data6.mergeActivity.append(3)
data6.mergeActivity.append(4)
data6.mergeActivity.append(5)
data6.mergeActivity.append(6)
data6.mergeActivity.append(7)
data6.showcondition = 10500 
data6.tubiao = "btn_gjgw_04.png" 



with open('D:/Kof/Tools/Excel2Protobuffers/gen_bytes/cfg_activity_game.bytes', 'wb') as f:
	f.write(dataArray.SerializeToString())
