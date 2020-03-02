import requests, time, os, sys

def dl(url):
    start = time.time()

    res = requests.get(url, stream=True)
    content_length = int(res.headers['content-length'])
    fname = os.path.basename(url)

    print(fname)
    with open(fname, 'wb') as f:
        if content_length is None: # no content length header(no body)
            f.write(res.content)
        else: #has body for download
            cbyt = 0
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk) ## write bytes
                
                #calculate MB/s
                cbyt += 1024 #chunk size = 1024
                avps = round(cbyt/(time.time()-start)/1000/1000, 2)
                print("{}/{}  {} MB/s".format(cbyt, content_length, avps), end="\r")

def main():
    try:
        dl(sys.argv[1])
    except:
        print("ERROR!")

main()