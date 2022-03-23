import jsonlines
import datetime
import os

object1 = {
               "name": "name1",
               "url": "url1"
          }

object2 = {
               "name": "name2",
               "url": "url2"
          }   

currentTime = datetime.datetime.now()
mTime = currentTime.strftime("%Y/%m/%d %H:%M:%S.%f")
mDate = currentTime.strftime("%Y%m%d")

_fileName = "common/"+mDate+"1.json"

# filename.jsonl is the name of the file
# with jsonlines.open(_fileName, "a") as writer:   # for writing
#     writer.write(object1)
#     writer.write(object2)

with jsonlines.open(_fileName) as reader:      # for reading
    try:
        print(reader)
    except OSError as e:
        print("Error: "+str(e))
    # for obj in reader:
    #     print(obj)
    #     print(obj['name'])

# if os.path.isdir("data"):
#     print("OK")
# else:
#     os.mkdir("data")


