import requests, time, os, sys, re, uuid

def dl(url):
    start = time.time()

    res = requests.get(url, stream=True)
    content_type = res.headers['content-type']
    if content_type:
        f_ex = "."+re.split("/", content_type)[1]
    f_name = os.path.basename(url)
    if f_name.endswith(f_ex) == False:
        f_name = str(uuid.uuid4())
    content_length = int(res.headers['content-length'])

    print("filename: ", f_name)
    with open(f_name, 'wb') as f:
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
    except Exception as e:
        print(e)

main()