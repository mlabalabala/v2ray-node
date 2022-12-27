# encoding=UTF-8

import base64, json, re, requests, time
from urllib.parse import unquote


requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}

# proxies = {"http": "http://127.0.0.1:10809","https": "https://127.0.0.1:10809",}
proxies = {"http": None,"https": None,}


def modIP(nodes):
    # nodes = base64.b64decode(s).decode('UTF-8').split('\n')
    nodes_mod_list = []
    for node in nodes:
        if (node):
            pro_type,node_det = node.split('://')
            if 'vmess' == pro_type:
                node_det_json = base64.b64decode(node_det).decode('UTF-8')
                node_det_dict = json.loads(node_det_json)
                # node_det_dict['ps'] = 'icook.hk-%02.d' % nodes.index(node)
                node_det_dict['ps'] = '%02.d' % nodes.index(node)
                # node_det_dict['add'] = 'uicdn.cf'
                # node_det_dict['add'] = 'icook.hk'
                node_det_dict['add'] = '104.16.155.47'
                node_det_json = json.dumps(node_det_dict)
                node_mod = 'vmess://'+base64.b64encode(node_det_json.encode()).decode('UTF-8')
                nodes_mod_list.append(node_mod)
            else:
                node_mod = re.sub(r'#(\S+)', '#%02.d' % nodes.index(node), node, 1, re.MULTILINE)
                nodes_mod_list.append(node_mod)
                # print(node_mod)
    return '\n'.join(nodes_mod_list)

if __name__ == "__main__":

    s = requests.session()

    y = time.strftime('%Y')
    m = time.strftime('%m')
    d = time.strftime('%d')
    
    try:
        u = f'https://clashnode.com/wp-content/uploads/{y}/{m}/{y+m+d}.txt'
        # u = f'https://nodefree.org/dy/{y+m}/{y+m+d}.txt'
        # u = f'https://raw.iqiq.io/ermaozi/get_subscribe/main/subscribe/v2ray.txt'
        # u = f'https://clashnode.com/wp-content/uploads/2022/12/20221224.txt'

        # print(time.strftime('/%Y%m/%Y%m%d'),time.strftime('/%Y/%m/%Y%m%d'))
        print(u)

        res = s.get(u, headers=headers, proxies=proxies)

        text = res.text

        if 'https://' == text[:8]:
            print('http')
            nodes = re.findall(r'url=(\S+)&insert=', unquote(text))[0].split('|')
            nodes_ori = base64.b64encode('\n'.join(nodes).encode(encoding='UTF-8')).decode('UTF-8')
        else:
            print('base64')
            nodes = base64.b64decode(text.encode(encoding='UTF-8')).decode('UTF-8').split('\n')
            nodes_ori = text
    except:
        print('except')
        # nodes = ['vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIjAyIiwNCiAgImFkZCI6ICIxMDQuMTYuMTU1LjQ3IiwNCiAgInBvcnQiOiAiNDQzIiwNCiAgImlkIjogImM2NzQ3ZGE0LWZiMmUtNGEyYS1iZGI3LTg2MTRiZGQ2YjBiMyIsDQogICJhaWQiOiAiMCIsDQogICJzY3kiOiAiYXV0byIsDQogICJuZXQiOiAid3MiLA0KICAidHlwZSI6ICJub25lIiwNCiAgImhvc3QiOiAic2czLXYycmF5LnNzaGtpdC5vcmciLA0KICAicGF0aCI6ICIvc3Noa2l0LzE3MzY5NjAxMTEvNjM4NTliYzE3N2EzMy8iLA0KICAidGxzIjogInRscyIsDQogICJzbmkiOiAic2czLXYycmF5LnNzaGtpdC5vcmciLA0KICAiYWxwbiI6ICIiDQp9']
        # nodes_ori = 'dm1lc3M6Ly9ldzBLSUNBaWRpSTZJQ0l5SWl3TkNpQWdJbkJ6SWpvZ0lqQXlJaXdOQ2lBZ0ltRmtaQ0k2SUNJeE1EUXVNVFl1TVRVMUxqUTNJaXdOQ2lBZ0luQnZjblFpT2lBaU5EUXpJaXdOQ2lBZ0ltbGtJam9nSW1NMk56UTNaR0UwTFdaaU1tVXROR0V5WVMxaVpHSTNMVGcyTVRSaVpHUTJZakJpTXlJc0RRb2dJQ0poYVdRaU9pQWlNQ0lzRFFvZ0lDSnpZM2tpT2lBaVlYVjBieUlzRFFvZ0lDSnVaWFFpT2lBaWQzTWlMQTBLSUNBaWRIbHdaU0k2SUNKdWIyNWxJaXdOQ2lBZ0ltaHZjM1FpT2lBaWMyY3pMWFl5Y21GNUxuTnphR3RwZEM1dmNtY2lMQTBLSUNBaWNHRjBhQ0k2SUNJdmMzTm9hMmwwTHpFM016WTVOakF4TVRFdk5qTTROVGxpWXpFM04yRXpNeThpTEEwS0lDQWlkR3h6SWpvZ0luUnNjeUlzRFFvZ0lDSnpibWtpT2lBaWMyY3pMWFl5Y21GNUxuTnphR3RwZEM1dmNtY2lMQTBLSUNBaVlXeHdiaUk2SUNJaURRcDk='
        d = '%d' % (int(d) - 1)
        u = f'https://clashnode.com/wp-content/uploads/{y}/{m}/{y+m+d}.txt'
        # u = f'https://nodefree.org/dy/{y+m}/{y+m+d}.txt'
        # u = f'https://raw.iqiq.io/ermaozi/get_subscribe/main/subscribe/v2ray.txt'

        # print(time.strftime('/%Y%m/%Y%m%d'),time.strftime('/%Y/%m/%Y%m%d'))
        print(u)

        res = s.get(u, headers=headers, proxies=proxies)

        text = res.text

        if 'https://' == text[:8]:
            print('http')
            nodes = re.findall(r'url=(\S+)&insert=', unquote(text))[0].split('|')
            nodes_ori = base64.b64encode('\n'.join(nodes).encode(encoding='UTF-8')).decode('UTF-8')
        else:
            print('base64')
            nodes = base64.b64decode(text.encode(encoding='UTF-8')).decode('UTF-8').split('\n')
            nodes_ori = text
            
    nodes_b64_en = base64.b64encode(modIP(nodes).encode(encoding='UTF-8'))
    nodes_b64_de = nodes_b64_en.decode('UTF-8')

    with open('clashnode_nodes_mod', 'w', encoding='UTF-8') as w:
        w.write(nodes_b64_de)
    with open('clashnode_nodes_ori', 'w', encoding='UTF-8') as w:
        w.write(nodes_ori)
