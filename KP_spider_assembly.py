"""retrieve the metadata from NCBI using assembly accession"
import requests
import time
import re
import csv
from concurrent import futures
from bs4 import BeautifulSoup
# baseurl = "https://www.ncbi.nlm.nih.gov/assembly/GCF_012971585.1/"
# headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"}
#
# response = requests.get(url=baseurl,headers=headers).text
# soup = BeautifulSoup(response,'html.parser')
# summary = soup.find_all('div',id='summary')
# print(summary)


# //*[@id="summary"]/dl/dd[1]/a

class Spider_KP:
    def __init__(self,filename):
        self.baseurl = "https://www.ncbi.nlm.nih.gov/biosample/"
        self.headers = {
        'User-Agent':'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 90.0.4430.93 Safari / 537.36'
    }
        with open(filename,'r') as f:
            csv_reader = csv.reader(f)
            self.csv_reader = list(csv_reader)
    def each_info(self,biosample):
        lst = []
        url = self.baseurl
        lst.append(biosample)
        params = {
            "term":biosample
        }
        print(biosample)
        request = requests.get(url=url,headers=self.headers,params=params)
        #print(request.text)

        # id = tree.xpath('//div[@id="viewercontent1"]/@val')[0]
        # print(id)

        # each_url = "http://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?"
        # each_request = requests.get(url=each_url,params=params,headers=self.headers)
        # print(each_request.status_code)
        # each_request = each_request.text
        try:
            host = re.findall(r'host</th><td>(.*?)</td>',request.text)[0]
        except:
            host = ""
        print(host)
        try:
            source = re.findall(r'isolation source</th><td>(.*?)</td></tr>',request.text)[0]
        except:
            source = ""
        print(source)
        try:
            country = re.findall(r'geographic location</th><td>(.*?)</td>',request.text)[0]
        except:
            country = ""
        print(country)
        try:
            collection_date = re.findall(r'collection date</th><td>(.*?)</td>',request.text)[0]
        except:
            collection_date = ""
        print(collection_date)
        try:
            Organism = re.findall(r'Organism</dt><dd><a href="/taxonomy/(.*?)"',request.text)[0]
        except:
            Organism = ""
        print(Organism)

        # try:
        #     title_pattern = re.compile(r'TITLE(.*?)JOURNAL',re.S)
        #     title = re.findall(title_pattern,each_request)[0].strip().replace('\n','')
        #     title = re.sub(' +'," ",title)
        # except:
        #     title = ""
        # print(title)
        lst.append(host)
        lst.append(source)
        lst.append(country)
        lst.append(collection_date)
        lst.append(Organism)
        with open(r'\assembly_example.csv','a',newline="") as f:
            f_writer = csv.writer(f)
            f_writer.writerow(lst)

    # 获取所有信息并保存
    def all_info(self):
        executor_1 = futures.ThreadPoolExecutor(max_workers=10)
        fs = []
        name_lst = []
        for item in self.csv_reader:
            # self.each_info(item)
            if item:
                name_lst.append(item[0])
        for item in name_lst:
            f = executor_1.submit(self.each_info, item)
            fs.append(f)
            time.sleep(0.2)
        futures.wait(fs)
        executor_1.shutdown(wait=True)
        print("All jobs done")
if __name__ == "__main__":
    spider_KP = Spider_KP(r"\metadata.csv")
    spider_KP.all_info()

