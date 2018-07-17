import requests
from bs4 import BeautifulSoup
import time

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}



def fetch_results(search,num_results,language_code):
    assert isinstance(search,str)
    assert isinstance(num_results,int)
    modified_search=search.replace(' ','+')
    # print(modified_search)
    google_url = 'http://www.google.com/search?q={}&num{}&hl={}'.format(modified_search,num_results,language_code)
    response = requests.get(google_url,headers=USER_AGENT)
    plain_text = response.text
    return search,plain_text

def parse_results(html,keyword):
    soup = BeautifulSoup(html,"html.parser")
    req_content_level_top = soup.findAll('div',{'class':'g'})
    # print(req_content_level_top)
    result_list = []
    for content in req_content_level_top:
        link = content.find('a',href=True)
        title = content.find('h3',{'class':'r'})
        if link and title:
            link = link['href']
            title = title.get_text()
            if link!='#':
                result_list.append({'keyword':keyword,'title':title,'product_url':link})
    return result_list


def scrape_web(search,num_results,language_code):
    try:
        keyword , html =fetch_results(search,num_results,language_code)
        collected_urls = parse_results(html, keyword)
        return collected_urls
    except AssertionError:
        raise Exception('Incorrect Arguments passed to the function!')
    except requests.HTTPError:
        raise Exception("You are blocked by Google!")
    except requests.RequestException:
        raise Exception("Check your connection and try again!")

if __name__=='__main__':
    n = int(input('Number of Produts :'))
    keywords = []
    for i in range(0,n):
        key = input("Enter key:")
        keywords.append(key)
    # keywords = ['Serta Perfect Sleeper Harlington Plush Queen Eurotop Mattress']
    urls_list = []
    for keyword in keywords:
        try:
            collected_urls = scrape_web(keyword, 2, "en")
            for result in collected_urls:
                urls_list.append(result)
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)
    for x in urls_list:
        print(x)
    # print(urls_list)








