import requests
import re
from config import BASE_URL
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Accept-Encoding':'gzip, deflate',
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
'Cookie':'_lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _lxsdk_cuid=16ab583b051c8-0d6120a069ed0c-b781636-1fa400-16ab583b052c8; __mta=107312829.1557823473175.1557823473175.1557823473175.1; client-id=2a3e9560-4ec7-4832-955f-4ab8d44b6b94; ci=197; rvct=197%2C1; mtcdn=K; lt=t1WaQyWIgq_t1WzCi7lkHJP_ZpAAAAAAZwgAAFy1TBfk6WMhgxxMiHXtY8_o4OwnuBCU3wKJS-BNa4iMW0itUOELYlwR604X_E9xaA; u=144324134; n=wang8911980; token2=t1WaQyWIgq_t1WzCi7lkHJP_ZpAAAAAAZwgAAFy1TBfk6WMhgxxMiHXtY8_o4OwnuBCU3wKJS-BNa4iMW0itUOELYlwR604X_E9xaA; uuid=96fbcd9c45d54206800c.1557823465.2.0.0; unc=wang8911980; _lxsdk_s=16ababdbf53-b8b-07f-901%7C%7C68'
}
base_url='http://bj.meituan.com/meishi/'
def parse_classify(base_url):
    response=requests.get(base_url,headers=DEFAULT_REQUEST_HEADERS).text
    compile=re.compile('http://bj.meituan.com/meishi/c(\d+)/')
    results=re.findall(compile,response)
    classify_set=set()
    for cateId in results:
        if cateId not in classify_set:
            originUrl='http://{cityname}.meituan.com/meishi/c{number}/'.format(cityname=BASE_URL.split('//')[-1].split('.')[0],number=cateId)
            classify_set.add(cateId)
            with open('./utils/labels.log', 'a') as f:
                f.write(cateId+'\t'+originUrl)
                f.write('\n')
if __name__=='__main__':
    parse_classify(base_url)
