import requests
from lxml import html
from bs4 import BeautifulSoup
import os
import json

def update_mc_server_download_url(server_type=['vanilla']):
    if 'vanilla' in server_type:
        update_vanilla_server_download_url()

def update_vanilla_server_download_url():
    download_page_urls = get_vanilla_server_download_page_urls()
    download_urls = get_vanilla_server_download_urls(download_page_urls)
    configs_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../configs/'))
    with open(configs_path+'/vanilla_server_urls.json', 'w') as f:
         json.dump(download_urls, f, indent=2)
    return download_urls

def get_vanilla_server_download_page_urls(publish_type='stable'):
    response = requests.get('https://mcversions.net/')
    page = html.fromstring(str(BeautifulSoup(response.text, 'html.parser')))
    download_page_urls = []
    if publish_type == 'stable':
        stabe_releases_elements = page.xpath('/html/body/main/div/div[2]/div[1]')[0]
        stabe_releases_download_elements = stabe_releases_elements.findall('.//a')
        for stabe_releases_download_element in stabe_releases_download_elements:
            if 'download' in stabe_releases_download_element.get('href'):
                download_page_urls.append("https://mcversions.net/" + stabe_releases_download_element.get('href'))
        return download_page_urls

def get_vanilla_server_download_urls(download_page_urls=[]):
    download_urls = {}
    for download_page_url in download_page_urls:
        print(download_page_url)
        response = requests.get(download_page_url)
        page = html.fromstring(str(BeautifulSoup(response.text, 'html.parser')))
        try:
            download_element = page.xpath('/html/body/main/div/div[1]/div[2]/div[1]/a')[0]
            download_urls[download_element.get('download').removesuffix('.jar')] = download_element.get('href')
        except IndexError:
            print('no server_jar link found')
    return download_urls


if __name__=='__main__':
    update_mc_server_download_url()
