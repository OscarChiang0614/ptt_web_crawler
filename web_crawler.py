import time
import requests
from bs4 import BeautifulSoup
import os
import re
import sys

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':RC4-SHA'

def get_ptt_page_url(url):
    time.sleep(0.05)
    response = requests.get(url = url,cookies = {'over18':'1'})                    #繞過滿18歲限制
    if response.status_code != 200:                                            #response.status_code回傳值為200表示正常
        print('Invalid url:', response.url)
        return None
    else:
        return response.text
    
def pages_article_crawler(content,pages_counter):
    output_all_articles = open("all_articles.txt", "a",encoding = 'utf8')
    output_all_popular = open("all_popular.txt", "a",encoding = 'utf8')
    soup = BeautifulSoup(content, 'html.parser')
    pages = soup.find('div', 'btn-group btn-group-paging')
    all_article_in_page = soup.find_all('div', 'r-ent')
    next_page = pages.find_all('a')[2]['href']
    end = 0
    ptt_url='https://www.ptt.cc'
   
    for article_data in all_article_in_page:
        if article_data.find('a'):
            nrec = article_data.find('div','nrec').string
            href = ptt_url + article_data.find('a')['href']
            title = article_data.find('a').string
            dates = int(article_data.find("div", {"class": "date"}).string.strip().replace('/',''))
            if  "[公告]" not in title and href != None and title != None and dates != None:
                if pages_counter == 0:
                    if dates < 1231:
                        output_all_articles.write(str(dates) + ","+str(title) + "," + str(href) + "\n")
                        if nrec == "爆" and nrec != None:
                            output_all_popular.write(str(dates) + "," + str(title) + "," + str(href) + "\n")
                elif dates < 102 and pages_counter > 350:
                    end = 1
                    return end,None
                else:
                    output_all_articles.write(str(dates) + ","+str(title)+"," + str(href) + "\n")
                    if nrec == "爆" and nrec != None:
                        output_all_popular.write(str(dates) + ","+str(title) + "," + str(href) + "\n")
    output_all_articles.close()
    return end, ptt_url+next_page
sofar_userID_like = {}
sofar_userID_boo = {}
def like_boo_counter(content):
    likes = 0
    boos = 0
    soup = BeautifulSoup(content,'html.parser')
    if soup.select("#main-content"):
        main_content = soup.select("#main-content")[0].get_text()
    else:
        main_content = []
    if "※ 發信站" in main_content:
        all_article_in_page = soup.find_all('div','push')
        for article_data in all_article_in_page:
            if article_data.find('span','push-userid') and article_data.find('span', 'push-tag'):
                tag = article_data.find('span', 'push-tag').string.strip(' \t\n\r')
                userid = article_data.find('span','push-userid').string.strip(' \t\n\r')
                current_item = []
                if tag == "推":
                    likes += 1
                    if userid not in sofar_userID_like:
                        sofar_userID_like[userid] = 1
                    else:
                        sofar_userID_like[userid] += 1
                        
                elif tag == "噓":
                    boos += 1
                    current_item.append(userid)
                    current_item.append("boo")
                    if userid not in sofar_userID_boo:
                        sofar_userID_boo[userid] = 1
                    else:
                        sofar_userID_boo[userid] += 1
    return likes, boos

sofar_image_url = []
def get_image_url(content):
    soup = BeautifulSoup(content,'html.parser')
    file_type = re.compile("^(http).*((\.jpg)|(\.jpeg)|(\.png)|(\.gif))$")
    if soup.select("#main-content"):
        main_content = soup.select("#main-content")[0].get_text()
    else:
        main_content = []
    if "※ 發信站" in main_content:
        all_article_in_page = soup.find_all('a')
        for article_data in all_article_in_page:
            image_url = article_data.string
            if image_url != None:
                match_flag = file_type.match(image_url)
                if match_flag:
                    sofar_image_url.append(image_url)

sofar_keyword_image_url = []
def check_keyword(content,keyword):
    test_keyword=0
    file_type = re.compile("^(http).*((\.jpg)|(\.jpeg)|(\.png)|(\.gif))$")
    soup = BeautifulSoup(content,'html.parser')
    if soup.select("#main-content"):
        main_content = soup.select("#main-content")[0].get_text()
    else:
        main_content = []
    if "※ 發信站" in main_content:
        test_content = main_content.split('※ 發信站')[0]
        if '--' in test_content:
            test_content = main_content.split('※ 發信站')[0].split('--')[:-1]
        for every_string in test_content:
            if keyword in every_string:
                test_keyword = 1
        if test_keyword:
            all_article_in_page = soup.find_all('a')
            for article_data in all_article_in_page:
                keyword_image_url = article_data.string
                if keyword_image_url != None:
                    match_flag = file_type.match(keyword_image_url)               
                    if match_flag:
                        sofar_keyword_image_url.append(keyword_image_url)

if __name__=='__main__':
    if len(sys.argv) < 2:
        print("invalid")
    input = sys.argv[1]
    if input == "crawl":
        tStart = time.time()
        if os.path.exists("all_articles.txt"):
            os.remove("all_articles.txt")
        if os.path.exists("all_popular.txt"):
            os.remove("all_popular.txt")
        start_url = 'https://www.ptt.cc/bbs/Beauty/index2748.html'             #2748至3143
        response = get_ptt_page_url(start_url)
        end_flag = 0
        pages_counter = 0
        if response != None:
            content = response
            if content != None:
                end_flag, next_page = pages_article_crawler(content, pages_counter)
                pages_counter += 1
                while next_page != None and end_flag == 0:
                    response = get_ptt_page_url(next_page)
                    content = response
                    end_flag, next_page = pages_article_crawler(content, pages_counter)
                    pages_counter += 1
        tEnd = time.time()
        print(tEnd-tStart)
    elif input == "push":
        tStart = time.time()
        if len(sys.argv) < 4:
            print("invlid")
        start_date = int(sys.argv[2])
        end_date = int(sys.argv[3])
        file_name = "push["+str(start_date) + "-" + str(end_date) + "].txt"
        if os.path.exists(file_name):
            os.remove(file_name)
        
        output_result = open(file_name, "a", encoding = 'utf8')
        
        with open("all_articles.txt",encoding='utf8') as f:
            content = f.readlines()
        start_flag = 0
        end_flag = 0
        start_index = -1
        end_index = -1
        all_url = []
        all_title = []
        all_date = []
        all_like = 0
        all_boo = 0    
        for i in range(0,len(content)):
            temp_line = content[i].split(',')
            all_date.append(temp_line[0])
            all_title.append(temp_line[1])
            if len(temp_line) == 3:
                all_url.append(temp_line[2].replace('\n',''))
            else:
                all_url.append(temp_line[3].replace('\n',''))
        for i in range(0,len(content)):
            if start_flag == 0 and int(all_date[i]) >= start_date:
                start_index = i
                start_flag = 1
            if int(all_date[i]) == end_date:
                end_index = i
            if end_flag == 0 and end_index == -1 and int(all_date[i]) > end_date:
                end_index = i-1
                end_flag = 1
        
        for i in range(start_index, end_index+1):
            response = get_ptt_page_url(all_url[i])
            if response != None:
                article_content = response
                likes, boos = like_boo_counter(article_content)
                all_like += likes
                all_boo += boos

    
        sofar_userID_like = sorted(sofar_userID_like.items(), key = lambda kv: kv[0])
        sofar_userID_boo = sorted(sofar_userID_boo.items(), key = lambda kv: kv[0])
        sofar_userID_like = sorted(sofar_userID_like, key = lambda kv: kv[1],reverse = True)
        sofar_userID_boo = sorted(sofar_userID_boo, key = lambda kv: kv[1],reverse = True)


        output_result.write("all like: " + str(all_like) + "\n")
        output_result.write("all boo: " + str(all_boo) + "\n")
        
        for i in range(0,10):
            output_result.write("like #"+str(i+1)+": "+str(sofar_userID_like[i][0])+" "+str(sofar_userID_like[i][1])+"\n")

        for i in range(0,10):
            output_result.write("boo #"+str(i+1)+": "+str(sofar_userID_boo[i][0])+" "+str(sofar_userID_boo[i][1])+"\n")
        
        output_result.close()
        tEnd = time.time()
        print(tEnd-tStart)
    elif input == "popular":
        tStart = time.time()
        if len(sys.argv)<4:
            print("invalid")
        start_date = int(sys.argv[2])
        end_date = int(sys.argv[3])

        file_name = "popular[" + str(start_date) + "-" + str(end_date) + "].txt"
        
        if os.path.exists(file_name):
            os.remove(file_name)

        output_result = open(file_name,"a", encoding = 'utf8')
        
        with open("all_popular.txt", encoding='utf8') as f:
            content = f.readlines()
        
        start_flag = 0
        end_flag = 0
        start_index = -1
        end_index = -1    
        all_url = []
        all_title = []
        all_date = []
        all_popular = 0
            
        for i in range(0,len(content)):
            temp_line = content[i].split(',')
            all_date.append(temp_line[0])
            all_title.append(temp_line[1])
            if len(temp_line) == 3:
                all_url.append(temp_line[2].replace('\n',''))
            else:
                all_url.append(temp_line[3].replace('\n',''))
        for i in range(0,len(content)):
            if start_flag == 0 and int(all_date[i]) >= start_date:
                start_index = i
                start_flag = 1
            if int(all_date[i]) <= end_date:
                end_index = i
            if  end_flag == 0 and end_index == -1 and int(all_date[i]) > end_date:
                end_index = i-1
                end_flag = 1
        
        for i in range(start_index, end_index+1):
            response = get_ptt_page_url(all_url[i])
            if response != None:
                article_content = response
                get_image_url(article_content)
        all_popular = end_index - start_index + 1
        output_result.write("number of popular articles: " + str(all_popular) + "\n")
        for i in range(0,len(sofar_image_url)):
            output_result.write(sofar_image_url[i] + "\n")
        output_result.close()
        tEnd = time.time()
        print(tEnd-tStart)
    elif input == "keyword":
        tStart = time.time()
        if len(sys.argv) < 5:
            print("invalid")
        keyword = sys.argv[2]
        start_date = int(sys.argv[3])
        end_date = int(sys.argv[4])

        file_name = "keyword(" + keyword + ")[" + str(start_date) + "-" + str(end_date) + "].txt"
        
        if os.path.exists(file_name):
            os.remove(file_name)

        output_result = open(file_name,"a", encoding = 'utf8')
        
        with open("all_articles.txt", encoding = 'utf8') as f:
            content = f.readlines()

        start_flag = 0
        end_flag = 0
        start_index = -1
        end_index = -1    
        all_url = []
        all_title = []
        all_date = []
            
        for i in range(0, len(content)):
            temp_line = content[i].split(',')
            all_date.append(temp_line[0])
            all_title.append(temp_line[1])
            if len(temp_line) == 3:
                all_url.append(temp_line[2].replace('\n',''))
            else:
                all_url.append(temp_line[3].replace('\n',''))

        for i in range(0, len(content)):
            if start_flag == 0 and int(all_date[i]) >= start_date:
                start_index = i
                start_flag = 1
            if int(all_date[i]) <= end_date:
                end_index = i
            if end_flag == 0 and end_index == -1 and int(all_date[i]) > end_date:
                end_index = i-1
                end_flag = 1

        for i in range(start_index, end_index+1):
            response = get_ptt_page_url(all_url[i])
            if response != None:
                article_content = response
                check_keyword(article_content, keyword)


        for i in range(0, len(sofar_keyword_image_url)):
            output_result.write(sofar_keyword_image_url[i] + "\n")
        output_result.close()
        tEnd = time.time()
        print(tEnd-tStart)
