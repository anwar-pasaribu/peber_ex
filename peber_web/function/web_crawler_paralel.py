# Web crawler dengan concurrent
# 12 Sept 2015


import sys, logging, re, threading, queue, requests, concurrent.futures

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

html_link_regex = \
	re.compile('<a\s(?:.*?\s)*?href=[\'"](.*?)[\'"].*?>')

urls = queue.Queue()
urls.put('http://www.cnnindonesia.com/teknologi/20150912144256-185-78250/sopir-ditangkap-uber-minta-dukungan-konsumen/')
urls.put('http://www.parallelpython.com/')

result_dict = {}

def group_urls_task(urls):
	try:
		url = urls.get(True, 0.05)
		result_dict[url] = None
		logger.info("[%s] putting url [%s] in dictionary..." % 
			(threading.current_thread().name, url))
	except queue.Empty:
		logging.error('Nothing to be done, queue is empty')

# Proses crawling
def crawl_task(url):
	links = []
	try:
		request_data = requests.get(url)
		logger.info("[%s] crawling url [%s] ..." % 
			(threading.current_thread().name, url))

		links = html_link_regex.findall(request_data.text)
	except:
		logger.error(sys.exc_info()[0])
		raise
	finally:
		return (url, links)

# max_workers untuk menentukan jumlah thread yang dijalankan 
# dalam sekali proses
MAX_WORKERS = 3

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as group_link_threads:
    for i in range(urls.qsize()):
        group_link_threads.submit(group_urls_task, urls)

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as crawler_link_threads:

    future_tasks = {crawler_link_threads.submit(crawl_task, url): url for url in result_dict.keys()}

    for future in concurrent.futures.as_completed(future_tasks):
        result_dict[future.result()[0]] = future.result()[1]


for url, links in result_dict.items():
	logger.info("[%s] with links : [%s...(%d more)]" % (url, links[0], len(links)))

