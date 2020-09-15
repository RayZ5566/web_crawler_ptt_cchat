import requests
import pandas_datareader as web
from bs4 import BeautifulSoup as bs
from requests_html import HTML
import pprint
import re
import matplotlib.pyplot as plt
import pandas as pd

def fetch(url):
  result = requests.get(url, cookies={'over18': '1'})
  return result
url = "https://www.ptt.cc/bbs/C_Chat/M.1596106802.A.210.html"
res = fetch(url)
print(res.text)

def parse(doc):
  html = HTML(html = doc)
  post_entries = html.find('div.push')
  return post_entries

res = fetch(url)
post_entries = parse(res.text)

print(post_entries)

def extract(entry):
  return {'f3.hl.push-userid': entry.find('.push-userid', first=True).text,
      'f3.push-content': entry.find('a')
    }
count = {}
none = {}
for entry in post_entries:
    meta = extract(entry)
    #print(meta)
    if len(meta['f3.push-content']) != 0:
      count['{}'.format(meta['f3.hl.push-userid'])] = str(meta['f3.push-content']).split()
    elif len(meta['f3.push-content']) == 0:
      none['{}'.format(meta['f3.hl.push-userid'])] = str(meta['f3.push-content'])
for k, v in count.items(): 
  print(k,':',v)

for k, v in none.items():
  print(k,':',v)



cl_count = {}
for k,v in count.items():
  cl_count[f'{k}'] = [] 
  for i in [4,9,14,19]:
    try:
      #print(k,v[i].split('=')[1].replace('\'',''))
      x = v[i].split('=')[1]
      for j in '\'>],':
          x = x.replace(j,'')
      cl_count[f'{k}'].append(x)
    except:
      try:
        #print(k,v[i].split('=')[1].replace('\'',''))
        x = v[i].split('=')[1]
        for j in '\'>],':
          x = x.replace(j,'')
        cl_count[f'{k}'].append(x)
      except:
        try:
          #print(k,v[i].split('=')[1].replace('\'',''))
          x = v[i].split('=')[1]
          for j in '\'>],':
              x = x.replace(j,'')
          cl_count[f'{k}'].append(x)
        except:
          pass  
print(cl_count)


none.keys()

#result
post_count = {}
for k,v in cl_count.items():
    post_count[f'{k}'] = []
    for i in v: 
       fp = i
       r = int(fp[:2],16)
       email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
       print(email.split('@'))
       for i in email.split('@'):
           if i == '':
               pass
           else:
                post_count[f'{k}'].append(i)
print(post_count)


#board



html = HTML(html = res.text)
board = html.find('div.bbs-screen.bbs-content')


#res = fetch(url)
#board = parse(res.text)

def extract(entry):
  return entry.find('div.bbs-screen.bbs-content', first=True).text


for entry in board:
    content = extract(entry)
    print(content)

content = content.split('[email\xa0protected]')
content = content[1:121]
content[119] = content[119][:13]
exclude = [' 2019春番',' 2019夏番',' 2019秋番',' 2019冬番']


for j in range(len(content)):
    for i in exclude:
        content[j] = content[j].replace(i,'')
for i in range(len(content)):
    content[i] = content[i].lstrip().rstrip()

    
ani_list = {}

k = 1
for i in range(0,3):
    for j in range(i,30,3):
        ani_list[f'{k}'] = str(k) + ': '+ content[j]
        k += 1

f = 31
for i in range(0,3):
    for j in range(k-1+i,k-1+30,3):
        ani_list[f'{f}'] = str(f)+ ': ' + content[j]
        f += 1
g = 61
for i in range(0,3):
    for j in range(f-1+i,f-1+30,3):
        ani_list[f'{g}'] = str(g)+ ': ' +content[j]
        g += 1

h = 91
for i in range(0,3):
    for j in range(g-1+i,g-1+30,3):
        ani_list[f'{h}'] = str(h)+ ': ' +content[j]
        h += 1


votes = list(post_count.values())

total_votes = []
for i in votes:
    for j in i:
        total_votes.append(j)

total_votes_count = dict((x,total_votes.count(x)) for x in set(total_votes))



final_result = {}
for k,v in total_votes_count.items():
    if k in ani_list.keys():
        final_result[f'{ani_list[k]}'] = v

check_votes_count = dict((x,total_votes.count(x)) for x in set(total_votes))



output = pd.DataFrame(final_result.items(), columns = ['動畫名稱','票數'])
output = output.sort_values(by='票數', ascending=False)
output.to_csv('2019年最喜歡的電視動畫票數統計.csv', index=False, encoding="utf_8_sig")


#decoding protected email address
import re
def deCFEmail():
    fp = '86b7c6'
    r = int(fp[:2],16)
    email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
    print(email)
if __name__ == "__main__":
    deCFEmail()

for k,v in cl_count.items():
    print(v)