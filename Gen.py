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

    u = f'https://clashnode.com/wp-content/uploads/{y}/{m}/{y+m+d}.txt'
    # u = f'https://nodefree.org/dy/{y+m}/{y+m+d}.txt'
    # u = f'https://raw.iqiq.io/ermaozi/get_subscribe/main/subscribe/v2ray.txt'

    # print(time.strftime('/%Y%m/%Y%m%d'),time.strftime('/%Y/%m/%Y%m%d'))

    res = s.get(u, headers=headers, proxies=proxies)

    text = res.text

    if 'https://' == text[:8]:
        nodes = re.findall(r'url=(\S+)&insert=', unquote(text))[0].split('|')
        nodes_ori = base64.b64encode('\n'.join(nodes).encode(encoding='UTF-8')).decode('UTF-8')
    else:
        nodes = base64.b64decode(text).decode('UTF-8').split('\n')
        nodes_ori = text

    nodes_b64_en = base64.b64encode(modIP(nodes).encode(encoding='UTF-8'))
    nodes_b64_de = nodes_b64_en.decode('UTF-8')

    with open('clashnode_nodes_mod', 'w', encoding='UTF-8') as w:
        w.write(nodes_b64_de)
    with open('clashnode_nodes_ori', 'w', encoding='UTF-8') as w:
        w.write(nodes_ori)
