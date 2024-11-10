import cloudscraper
from bs4 import BeautifulSoup as parser

class Komik:
    def __init__(self,params,search):
        self.url = "https://bacakomik.net/"
        self.session = cloudscraper.create_scraper()
        self.params = params
        self.search = search
        
    def add_requests(self):
        response = parser(self.session.get(self.url+self.params).text, "html.parser")
        return response
        
    def main(self):
        response = self.add_requests()
        #soup = response.find("section",{"class":"whites"}) if "latest" in self.search else response.find("div",{"class":"arch-list"})
        komik = []
        for item in response.find_all("div",{"class":"animepost"}):
            data = self.latest(item) if "latest" in self.search else self.searching(item)
            komik.append(data)
        data = {"komik":komik}
        if response.find("div",{"class":"pagination"}).find("a",{"class":"next page-numbers"}):
            data.update({"nextPage": True})
        else:
            data.update({"nextPage":False})
        return data
        
    def latest(self,item):
        title = item.find("h4").text
        slug = item.find("a").get("href").split("/")[4]
        cover = item.find("img").get("data-lazy-src")
        chapter = item.find("div",{"class":"lsch"}).find("a").text.replace("Ch.","").replace("\t","").strip()
        time = item.find("span",{"class":"datech"}).text.strip()
        type = "Manhwa" if item.find("span",{"class":"typeflag Manhwa"}) else ("Manhua" if item.find("span",{"class":"typeflag Manhua"}) else "Manga")
        return {"title":title, "slug":slug, "cover":cover, "chapter":chapter, "time":time, "type":type}
        
    def searching(self,item):
        title = item.find("h4").text
        slug = item.find("a").get("href").split("/")[4]
        cover = item.find("img").get("src")
        rating = item.find("div",{"class":"rating"}).find("i").text
        type = "Manhwa" if item.find("span",{"class":"typeflag Manhwa"}) else ("Manhua" if item.find("span",{"class":"typeflag Manhua"}) else "Manga")
        return {"title":title, "slug":slug, "cover":cover, "rating":rating, "type":type}
        
    def genrelist(self):
        response = self.add_requests()
        data = []
        for item in response.find("ul",{"class":"genrelist"}).find_all("li"):
            name = item.text
            slug = item.find("a").get("href").split("/")[4]
            data.append({"name":name,"slug":slug})
        return data
        
    def detail(self):
        response = self.add_requests()
        data = {}
        body = response.find("div",{"class":"postbody"})
        title = body.find("img").get("title").strip()
        cover = body.find("img").get("data-lazy-src")
        chapterFirst = body.find_all("div",{"class":"epsbr"})[0].find("span",{"class":"barunew"}).text.replace("Chapter","").strip()
        chapterLast = body.find_all("div",{"class":"epsbr"})[1].find("span",{"class":"barunew"}).text.replace("Chapter","").strip()
        for item in body.find("div",{"class":"infox"}).find_all("span"):
            name = item.text.split(":")[0].replace(" ","").lower().strip()
            value = item.text.split(":")[1].strip()
            data.update({name:value})
        genre = ",".join(genre.text for genre in response.find("div",{"class":"genre-info"}).find_all("a"))
        description = " ".join(body.find("div",{"itemprop":"description"}).text.split())
        chapterList = []
        for item in body.find("div",{"id":"chapter_list"}).find_all("li"):
            slug = item.find("span",{"class":"lchx"}).find("a").get("href").split("/")[3]
            chapter = item.find("span",{"class":"lchx"}).find("chapter").text.strip()
            date = item.find("span",{"class":"dt"}).find("a").text.strip()
            chapterList.append({"slug":slug, "chapter":chapter, "date":date})
        data.update({"title":title, "cover":cover, "chapterFirst":chapterFirst, "chapterLast":chapterLast, "genre":genre, "description":description, "chapterList":chapterList})
        return data
        
    def viewchapter(self):
        response = self.add_requests()
        title = response.find("div",{"class":"dtlx"}).find("h1").text.replace("Komik","").strip()
        try:
            prevChapter = response.find("div",{"class":"nextprev"}).find("a",{"rel":"prev"}).get("href").split("/")[3]
        except:
            prevChapter = False
        try:
            nextChapter = response.find("div",{"class":"nextprev"}).find("a",{"rel":"next"}).get("href").split("/")[3]
        except:
            nextChapter = False
        image = []
        for item in response.find("div",{"id":"anjay_ini_id_kh"}).find_all("img"):
            if item.get("data-lazy-src"):
                image.append(item.get("data-lazy-src"))
        return {"title":title, "prevChapter":prevChapter, "nextChapter":nextChapter, "imageList":image}
        
#print(Komik("isekai-furin-ll-michibika-reshi-hitodzuma-tachi-to-bukiyo-tensei-yuusha-chapter-1/","").viewchapter())