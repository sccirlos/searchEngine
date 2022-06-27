from urllib.parse import urlparse


# this will get the domain name for this instance the index that we need so index.html
def domain_name(url):
    try:
        results = sub_domain(url).split('.')
        print(results)
        return results[-2] + '.' + results[-1] + '/rhf'
    except:
        print("domain name failed.: ")
        return ''


# this will get any domain name for example anything else other than a www. so like name.hello.com
def sub_domain(url):
    try:
        print("url parse: ", urlparse(url).netloc)
        return urlparse(url).netloc
    except:
        print("sub domain didnt work")
        return ''


url = "https://mobile.www.netfunny.com/rhf/index.html"

print("this is my domain: ", url)

print("splitting url: ", url[0])
print(domain_name(url))
