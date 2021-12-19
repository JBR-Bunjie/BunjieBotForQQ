## Other Exception Error
### HTTPSConnectionPool(host='api.vc.bilibili.com', port=443): Max retries exceeded with url: /dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=0&host_uid=36081646&offset_dynamic_id=0&need_top=1&platform=web (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x000001F5ACC0B220>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
- 原因?

是因为在每次数据传输前客户端要和服务器建立TCP连接，为节省传输消耗，默认为keep-alive，即连接一次，传输多次，然而在多次访问后不能结束并回到连接池中，导致不能产生新的连接

- 解决办法

1. response.close()
2. headers = {'connection': 'close'}
