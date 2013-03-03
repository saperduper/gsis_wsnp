Code for http://gsis-wsnp.appspot.com, a simple client for the SOAP WS provided by GSIS (http://www.gsis.gr/wsnp.html)

---------

_Contains a slightly modified version of [suds](https://fedorahosted.org/suds) ((beta) R703-20101015)_

* suds/client.py
```
109c109
<         options.cache = ObjectCache(days=1)
---
>  #      options.cache = ObjectCache(days=1)
```

* suds/bindings/rpc.py
```
44,45c44,45
<         env.set('%s:encodingStyle' % envns[0], 
<                 'http://schemas.xmlsoap.org/soap/encoding/')
---
>  #       env.set('%s:encodingStyle' % envns[0], 
>  #               'http://schemas.xmlsoap.org/soap/encoding/')
```
