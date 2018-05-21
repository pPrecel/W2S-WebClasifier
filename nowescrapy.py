import queue
import WebScrapper
import ReadExcel
import threading
import time

dicti = ReadExcel.read()

pages =  []
classes = []

flat = []

for key in dicti.keys():
    for link in dicti[key]:
        flat.append((key, link))

print('all:', len(flat))

q = queue.Queue(maxsize=0)

sum = len(flat)
num_theads = min(64, sum)

for i in range(len(flat)):
    q.put((i,flat[i]))

def crawl(q, resultPages, resultClasses):
    while not q.empty():
        work = q.get()
        category = work[1][0]
        url = work[1][1]
        data = WebScrapper.scrapPage(url)
        resultPages[work[0]] = data
        resultClasses[work[0]] = category
        q.task_done()


start = time.time()

resultPages = [0] * len(flat)
resultClasses = [0] * len(flat)
for i in range(num_theads):
    worker = threading.Thread(target=crawl, args=(q, resultPages, resultClasses))
    worker.setDaemon(True)
    worker.start()

q.join()


print('')
for i in range(len(resultPages)):
    print('klasa: ', resultClasses[i],', jest ',len(resultPages[i]), ' slowek')

end = time.time()
print(end - start)

exit()




