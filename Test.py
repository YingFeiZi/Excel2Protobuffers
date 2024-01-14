import sys
import gen_Python.Item_pb2 as Item

# message Item {
#     uint32 Id = 1;
#     string Name = 2;
#     uint32 NameId = 3;
#     string Note = 4;
#     int32 Type = 5;
#     int64 SubType = 6;
#     uint32 ExeType = 7;
#     double PosType = 8;
#     float UseType = 9;
#     uint64 Binding = 10;
#     sint32 Overlaying = 11;
#     sint64 Level = 12;
#     fixed32 Quality = 13;
#     fixed64 Beauty = 14;
#     sfixed32 Icon = 15;
#     sfixed64 SmallIcon = 16;
#     bool Ismodel = 17;
#     repeated uint32 Getway = 18;
#     repeated int32 Callback = 19;
#     repeated float Importance = 20;
#     repeated string Belong = 21;
#     repeated bool Partner = 22;
# }

itemconfig = Item.ItemArray()

with open('gen_bytes/Item.bytes', 'rb') as f:
    itemconfig.ParseFromString(f.read())

for data in itemconfig.datas:
    print(data.Id, data.Name, data.NameId, data.Note, data.Type, data.SubType, data.ExeType, data.PosType, data.UseType, data.Binding, data.Overlaying, data.Level, data.Quality, data.Beauty, data.Icon, data.SmallIcon, data.Ismodel, data.Getway, data.Callback, data.Importance, data.Belong,data.Partner)