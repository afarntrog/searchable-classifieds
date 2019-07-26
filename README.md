## Problem: 
My local newspaper has local job classifieds. However, they are online only as a [flipbook](https://www.3dissue.com/flipbooks.html).
Since flipbooks are in pdf format they are not searchable. And it is too tedious to look through each one to find something in my interests.


## Solution: 

I created this Python Django app to scrape the classifieds pdf and then using tesseract OCR extracted the text. Then I displayed them in a nice format and added search to the app. So now you can easily find jobs with your desired keywords.


---
---
---
# Heroku, Django and tesseract

#### This doc will walk you through setting up tesseract on Heroku (i'm using django)


# Steps

##### 1) Add heroku-apt-buildpack using the command:
This is the stable version. See the source [repository](https://github.com/heroku/heroku-buildpack-apt)
```sh
$ heroku buildpacks:add --index 1 heroku-community/apt
```


##### 2) Add Aptfile to project directory
```sh
$ touch Aptfile
```

##### 3) Add the folowing to the Aptfile
tesseract-ocr-eng is the English language file for tesseract.
```sh
tesseract-ocr
tesseract-ocr-eng
```

##### 4) Get path to the data downloaded by the tesseract-ocr-eng package
We will use this path for the next step
```sh
$ heroku run bash
$ find -iname tessdata # this will give us the path we need
```
You can exit heroku shell now `exit`

##### 5) Now set a heroku config variable named TESSDATA_PREFIX to path
Set a heroku config variable named TESSDATA_PREFIX  to the path returned from `find -iname tessdata` cmnd above
```sh
$ heroku config:set TESSDATA_PREFIX=./.apt/usr/share/tesseract-ocr/4.00/tessdata
```
Now set heroku set a heroku config variable named TESSDATA_PREFIX  to the path returned from find -iname tessdata

##### 6) Push changes to heroku
Set a heroku config variable named TESSDATA_PREFIX  to the path returned from find -iname tessdata cmnd above
```sh
$ git push heroku master
```

I hope this helps. Let me know if it works for you.