import cloudscraper
from bs4 import BeautifulSoup as parser

class Komik:
    def __init__(self,params):
        self.url = "https://komikstation.co/"
        self.session = cloudscraper.create_scraper()
        self.params = params
        
    def add_requests(self):
        response = parser(self.session.get(self.url+self.params).text, "html.parser")
        return response
        
    def latest(self):
        response = self.add_requests()
        komik = []
        for item in response.find_all("div",{"class":"utao"}):
            title = item.find("h4").text.strip()
            slug = item.find("a",{"class":"series"}).get("href").split("/")[4]
            cover = item.find("img").get("src").split(".jpg?")[0]
            type = "Manhwa" if item.find("ul",{"class":"Manhwa"}) else ("Manhua" if item.find("ul",{"class":"Manhua"}) else "Manga")
            chapter = item.find("ul",{"class": f"{type}"}).find_all("li")[0].find("a").text.replace("Ch.","")
            time = item.find("ul",{"class": f"{type}"}).find_all("li")[0].find("span").text
            komik.append({"title":title, "slug":slug, "cover":cover, "type":type, "chapter":chapter, "time":time})
        return komik
        
    def search(self):
        response = self.add_requests()
        komik = []
        for item in response.find_all("div",{"class":"bs"}):
            title = item.find("div",{"class":"tt"}).text.strip()
            slug = item.find("a").get("href").split("/")[4]
            cover = item.find("img").get("src").split(".jpg?")[0]
            type = "Manhwa" if item.find("span",{"class":"type Manhwa"}) else ("Manhua" if item.find("span",{"class":"type Manhua"}) else "Manga")
            chapter = item.find("a",{"class": "epxs"}).text.replace("Chapter","")
            komik.append({"title":title, "slug":slug, "cover":cover, "type":type, "chapter":chapter})
        data = {"komik":komik}
        try:
            if response.find("div",{"class":"hpage"}).find("a",{"class":"r"}):
                data.update({"nextPage": True})
        except:
            try:
                if response.find("div",{"class":"pagination"}).find("a",{"class":"next page-numbers"}):
                    data.update({"nextPage": True})
            except:
                data.update({"nextPage":False})
        return data
        
    def genrelist(self):
        response = self.add_requests()
        genre = []
        for item in response.find("ul",{"class":"dropdown-menu c4 genrez"}).find_all("li"):
            name = item.text.strip()
            slug = item.find("input").get("value")
            genre.append({"name":name, "slug":slug})
        return genre
        
    def detail(self):
        response = self.add_requests()
        title = response.find("div",{"class":"infox"}).find("h1",{"class":"entry-title"}).text.replace("Bahasa Indonesia","").strip()
        cover = response.find("div",{"class":"thumb"}).find("img").get("src")
        rating = response.find("div",{"class":"rating"}).find("div",{"class":"num"}).text
        following = response.find("div",{"class":"bmc"}).text.replace("Diikuti","").replace("orang","").strip()
        sinopsis = " ".join(response.find("div",{"class":"entry-content entry-content-single"}).text.split())
        status = response.find("div",{"class":"tsinfo"}).find_all("div",{"class":"imptdt"})[0].text.replace("Status","").strip()
        type = response.find("div",{"class":"tsinfo"}).find_all("div",{"class":"imptdt"})[1].text.replace("Tipe","").strip()
        release = response.find_all("div",{"class":"fmed"})[0].find("span").text.strip()
        author = response.find_all("div",{"class":"fmed"})[1].find("span").text.strip()
        artist = response.find_all("div",{"class":"fmed"})[2].find("span").text.strip()
        genre = ",".join(genre.text for genre in response.find("span",{"class":"mgen"}).find_all("a"))
        chapterList = []
        for item in response.find("div",{"id":"chapterlist"}).find_all("li"):
            slug = item.find("a").get("href").split("/")[3]
            chapter = item.find("span",{"class":"chapternum"}).text.strip()
            date = item.find("span",{"class":"chapterdate"}).text.strip()
            newdate = f"{date.split()[1].replace(',','')} {date.split()[0]} {date.split()[2]}"
            chapterList.append({"slug":slug, "chapter":chapter, "date":newdate})
        chapterFirst = "0" if response.find("span",{"class":"epcur epcurfirst"}).text.replace("Chapter","").strip()=="?" else "1"
        chapterLast = response.find("span",{"class":"epcur epcurlast"}).text.replace("Chapter","").strip()
        return {"title":title, "cover":cover, "chapterFirst":chapterFirst, "chapterLast":chapterLast, "genre":genre, "sinopsis":sinopsis, "status":status, "author":author, "artist":artist, "type":type, "release":release, "rating":rating, "following":following, "chapterList":chapterList}
        
    def viewchapter(self):
        response = self.add_requests()
        chapter = []
        for item in response.find("div",{"class":"rdminimal"}).find_all("img"):
            chapter.append(item.get("src"))
        return chapter
        
#print(Komik("?s=isekai").search())
