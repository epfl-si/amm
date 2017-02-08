
To specify URL query string parameters, you need to use the key==value syntax:


$ http --verbose httpbin.org/get  tag==xxx  tag2==yyy
GET /get?tag=xxx&tag2=yyy HTTP/1.1


