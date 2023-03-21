from bs4 import BeautifulSoup

with open(r"bs4_test\test.html", "r",encoding='utf-8') as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')

div_node = soup.find("div",id="content")
links = div_node.find_all("a")
for link in links:
    print(link.name,link["href"],link.get_text())

img = div_node.find("img")
print(img)
print(img["src"])