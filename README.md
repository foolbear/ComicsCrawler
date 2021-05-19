# ComicsCrawler

## 目的
这个项目的目的是为了生成符合[ **“大笨熊漫画”**  App](https://apps.apple.com/us/app/) 需要格式化的 **“Foolbear Comics Book Package”** 而提供的 python 示例。您也可以使用其他语言和工具，只要生成“Foolbear Comics Book Package”格式即可。

## Foolbear Comics Book Package
这个格式是一个 Json 文件，其后缀是 **“.fcbp”** 。该文件可以通过类似 AirDrop 等方法导入到 **“大笨熊漫画”**  App 中，即可阅读漫画书。
其格式如下（[示例](https://github.com/foolbear/ComicsCrawler/blob/main/%E6%90%9E%E6%80%AA%E5%AE%B6%E5%BA%AD.fcbp)）：
```json
{
    "sourceUrl": "https://m.mhgui.com/comic/1062/", 
    "name": "搞怪家庭", 
    "author": "北条司", 
    "introduction": "        雅彦搬进舅舅的家后竟发现舅舅是女人，而舅母才是母亲的弟弟，在这个特殊家庭的内，雅彦逐渐对漂亮的表妹产生了感情，但是面对性别颠倒的舅母和舅舅，表妹的性别成了雅彦的一大疑问，在探求表妹身份的同时，\"雅彦\"也逐渐开始男扮女装成了大学影视剧俱乐部的大明星，并且得到了黑社会老大的爱慕！？突然又出现了个女扮男装的帅哥出来追求他，总之发生在这家人身上的故事就是那么不可思议！", 
    "coverUrl": "https://cf.hamreus.com/cpic/m/1062.jpg", 
    "chapters": [
        {
            "index": 0, 
            "sourceUrl": "https://m.mhgui.com//comic/1062/9334.html", 
            "name": "第01卷(P1)", 
            "pictures": [
                {
                    "index": 0, 
                    "slices": [
                        {
                            "index": 0, 
                            "sourceUrl": "https://i.hamreus.com/ps1/g/GGJT/01/seemh-001-c97c.jpg.webp?e=1622628243&m=N6DO5FLjRvnTt36Ges0umg"
                        }
                    ]
                }, 
                {
                    "index": 1, 
                    "slices": [
                        {
                            "index": 0, 
                            "sourceUrl": "https://i.hamreus.com/ps1/g/GGJT/01/seemh-002-c7fd.png.webp?e=1622628243&m=N6DO5FLjRvnTt36Ges0umg"
                        }
                    ]
                }, 
                {
                    "index": 2, 
                    "slices": [
                        {
                            "index": 0, 
                            "sourceUrl": "https://i.hamreus.com/ps1/g/GGJT/01/seemh-003-96a7b.png.webp?e=1622628243&m=N6DO5FLjRvnTt36Ges0umg"
                        }
                    ]
                }
            ]
        }
    ], 
    "sourceName": "看漫画", 
    "sourceUpdateAt": "2016-06-01"
}
```

## 使用方法
### 数据源
这个项目接受的数据源来自各大漫画网站。

### 使用前
安装 python，安装相关模块：getopt、user_agent、json、selenium、BeautifulSoup 等。

### 漫画网站
对于各大漫画网站，这里提供了示例：  
* CrawlerKMH.py:  [看漫画](https://www.mhgui.com)

使用方法是：  
```shell
FoolMBP:~ foolbear$ python ~/Crawler/CrawlerKMH.py --help
FoolMBP:~ foolbear$ python ~/Crawler/CrawlerKMH.py -u https://m.mhgui.com/comic/1062/ -o ~/Downloads/
```

* 对于这些示例网站，基本上可以直接使用即可。您也可以根据具体书籍格式（空行数不同，段首空格不同）做些微调。  
* 对于其他漫画网站，也可以在这些示例的基础上修改，这可能需要您稍微了解下 python 的编程（很简单，我也是现学的，可能够用不够好）。

### 使用技巧
* 在使用这里的工具时，可以先加上 “-m 1” 的参数，观察三个章节的输出格式是否满意。满意之后，去掉该参数，输出所有章节。

## 联系我（foolbear@foolbear.com）
* 如果有朋友想一起完善这个项目，类似提供不同漫画网站的支持，也可以联系我加入项目。  
* 如果有朋友玩不来 python，需要请求书籍或其他支持，也可以联系我，或者直接提交 issue 让大家一起帮助您。

