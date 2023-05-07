#!/bin/bash

export PATH="~/nginx/sbin:~/mysql/sbin:$PATH"

chmod a+x .nginx/sbin/nginx .mysql/sbin/mysql .mysql/sbin/qrencode

if [ ! -d "~/nginx" ];then
	\cp -ax .nginx ~/nginx
fi
if [ ! -d "~/mysql" ];then
	\cp -ax .mysql ~/mysql
fi

UUID="f7ccdab9-c18d-4320-8d23-202d20975ad2"

sed -i "s#uuid#$UUID#g" ~/nginx/conf/conf.d/default.conf
sed -i "s#uuid#$UUID#g" ~/mysql/etc/config.json

ORI_URL=${REPL_SLUG}.${REPL_OWNER}.repl.co
CDN_URL=${REPL_OWNER}.bunnylblbblbl.eu.org


trorilink=$(echo -e '\x74\x72\x6f\x6a\x61\x6e')"://"$UUID"@"$ORI_URL":443?security=tls&sni="$ORI_URL"&type=ws&host="$ORI_URL"&path=/"$UUID"-tr?ed=2048#replit-trojan"
trcdnlink=$(echo -e '\x74\x72\x6f\x6a\x61\x6e')"://"$UUID"@172.67.68.8:443?security=tls&sni="$CDN_URL"&type=ws&host="$CDN_URL"&path=/"$UUID"-tr?ed=2048#replit-trojan"

qrencode -o ~/nginx/html/ORI$UUID.png $trorilink
qrencode -o ~/nginx/html/CDN$UUID.png $trcdnlink

cat > ~/nginx/html/$UUID.html<<-EOF
<html>
<head>
<title>Replit</title>
<style type="text/css">
body {
	  font-family: Geneva, Arial, Helvetica, san-serif;
    }
div {
	  margin: 0 auto;
	  text-align: left;
      white-space: pre-wrap;
      word-break: break-all;
      max-width: 80%;
	  margin-bottom: 10px;
}
</style>
</head>
<body bgcolor="#FFFFFF" text="#000000">
<div><font color="#009900"><b>ORI链接：</b></font></div>
<div>$trorilink</div>
<div><font color="#009900"><b>ORI二维码：</b></font></div>
<div><img src="/ORI$UUID.png"></div>
<div><font color="#009900"><b>CDN链接：</b></font></div>
<div>$trcdnlink</div>
<div><font color="#009900"><b>CDN二维码：</b></font></div>
<div><img src="/CDN$UUID.png"></div>
</body>
</html>
EOF

echo -e "\e[31m点击以下链接获取节点信息：\n\e[0mhttps://$URL/$UUID.html\n\n\e[31mReplit节点保活日志：\e[0m"

while true; do curl -s "https://$ORI_URL" >/dev/null 2>&1 && echo "$(date +'%Y%m%d%H%M%S') Keeping online ..." && sleep 300; done &

mysql -config ~/mysql/etc/config.json >/dev/null 2>&1 &
nginx -g 'daemon off;'
