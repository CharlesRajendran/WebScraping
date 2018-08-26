import bs4
from urllib.request import urlopen

def read_html(url):
    # get the source html
    url = urlopen(url)
    html = url.read()
    url.close()

    # create beautiful soup object and parse the html so we can use bs methods
    bs = bs4.BeautifulSoup(html, 'html.parser')
    return bs

def scrape_home(bs):
    news_links = []
    
    home_html = bs.find_all('div', class_ = 'cb-col cb-col-100 cb-lst-itm cb-lst-itm-lg')
    #news_links = [link.a.get('href') for link in home_html]
    for link in home_html:
        news_links.append(link.a.get('href'))

    return news_links

def scrape_article(bs):
    head_line = bs.find_all('h1', class_='nws-dtl-hdln')
    content = head_line[0].getText() + '\n\n';
    for p in bs.find_all('section', class_='cb-nws-dtl-itms', itemprop='articleBody'):
        content = content + p.getText().strip() + '\n\n'
    
    return content

def write_file(filename, content):
    file = '{}.txt'.format(str(filename))
    f = open(file, 'w')
    f.write(content)
    f.close()
    

if __name__ == '__main__':
    base_url = 'http://www.cricbuzz.com/cricket-news'
    bs = read_html(base_url)
    link_list = scrape_home(bs)
    # count is just to name the file
    count = 0
    for link in link_list:
        count += 1
        url = 'http://www.cricbuzz.com' + link
        content = scrape_article(read_html(url))
        write_file(count, content)

