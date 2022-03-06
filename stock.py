from html.parser import HTMLParser
import re
import requests

url = "https://XXXX"

excludeList = []

staleList = []

class Parser(HTMLParser):
  start_tags = []
  end_tags = []
  all_data = []
  comments = []
  doPrint = False

  # method to append the start tag to the list start_tags.
  def handle_starttag(self, tag, attrs):
    self.start_tags.append(tag)
  
  # method to append the end tag to the list end_tags.
  def handle_endtag(self, tag):
    self.end_tags.append(tag)
  
  # method to append the data between the tags to the list all_data.
  def handle_data(self, data):
    line = re.sub(r'\s+', '', data)
    if line != "":
      if line == "(Rs.cr)":
        self.doPrint = True
        return
      if line in ["AddtoWatchlist", "AddtoPortfolio"]:
        return
      if ".mrktSts" in line:
        self.doPrint = False
      if self.doPrint == True:
        self.all_data.append(line)
  
  # method to append the comment to the list comments.
  def handle_comment(self, data):
    self.comments.append(data)
  
  def print_parser_vars(self):
    print("start tags:", self.start_tags)
    print("end tags:", self.end_tags)
    print("data:", self.all_data)
    print("comments", self.comments)

def convStrToFloat(floatStr):
  return float(floatStr.replace(',', ''))

def printMap(stockPrice, defHighPcMap, totalCap, limit=20):
  priceSum = 0
  sortdDefHighPcMap = sorted(defHighPcMap.items(), key=lambda x: x[1], reverse=True)
  freqList = {}
  innerloop = False

  tempMap = []
  for i in range(0, len(sortdDefHighPcMap)):
    if i >= limit:
      #print(sortdDefHighPcMap[i])
      #continue
      break
    tuple = sortdDefHighPcMap[i]
    tempMap.append((tuple[0], tuple[1]))

  sortdDefHighPcMap = tempMap

  while True:
    for tuple in sortdDefHighPcMap:
      company = tuple[0]
      highDef = tuple[1]
      yrHigh = stockPrice[company]["yrHigh"]
      yrLow = stockPrice[company]["yrLow"]
      price= stockPrice[company]["lastPrice"]
      totalDef = (yrHigh - yrLow) / yrLow * 100
      totalDef = float("{:.2f}".format(totalDef))
      if (priceSum + price) > totalCap:
        innerloop = True
        break
      #if totalDef > 60 and highDef > 15 and price < 3000 :
      if company not in freqList:
        freqList[company] = {"company": company, "price": price, "totalDef": totalDef, "highDef": highDef, "sharecount": 1}
      else:
        freqList[company]["sharecount"] += 1
      priceSum = priceSum + price
    if innerloop == True:
      break
  
  for company, tuple in freqList.items():
    print((tuple["company"], tuple["price"], tuple["totalDef"], tuple["highDef"], tuple["sharecount"]), "{:,.2f}".format(tuple["price"] * tuple["sharecount"]))
  print("Total Sum = {}".format("{:,.2f}".format(priceSum)))

if __name__ == "__main__":
  stockPrice = {}
  defHighPcMap = {}

  smallcap = {}
  midcap = {}
  largecap = {}

  # Creating an instance of our class.
  parser = Parser()
  res = requests.get(url)
  parser.feed(res.text)

  for i in range(0, len(parser.all_data), 6):
    company = parser.all_data[i+0]
    entry = {
      "lastPrice": convStrToFloat(parser.all_data[i+1]),
      "changePc": convStrToFloat(parser.all_data[i+2]),
      "yrHigh": convStrToFloat(parser.all_data[i+3]),
      "yrLow": convStrToFloat(parser.all_data[i+4]),
      "cap": convStrToFloat(parser.all_data[i+5]),
    }
    if entry["lastPrice"] > 100000:
      continue
    defHigh = float("{:.2f}".format(entry["yrHigh"] - entry["lastPrice"]))
    defpercent = float("{:.2f}".format(defHigh / entry["yrHigh"] * 100))
    entry["defpercent"] = defpercent
    
    if defpercent < 0:
      continue
    if company in excludeList or company in staleList:
      continue
    
    stockPrice[company] = entry
  
  for company, entry in stockPrice.items():
    if entry["lastPrice"] < 1100:
      smallcap[company] = entry["defpercent"]
    elif entry["lastPrice"] < 3100:
      midcap[company] = entry["defpercent"]
    elif entry["lastPrice"] < 5100:
      largecap[company] = entry["defpercent"]
  
  totalCap = XXXX
  printMap(stockPrice, smallcap, float(totalCap * 0.10), 14)
  print('#' * 20)
  printMap(stockPrice, midcap, float(totalCap * 0.40), 16)
  print('#' * 20)
  printMap(stockPrice, largecap, float(totalCap * 0.50), 10)
