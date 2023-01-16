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
#                 node_det_dict['ps'] = 'icook.hk-%02.d' % nodes.index(node)
#                 node_det_dict['ps'] = '%02.d' % nodes.index(node)
                node_det_dict['ps'] = f'{y}/{m}/{d}-' + node_det_dict['ps']
#                 node_det_dict['add'] = 'guolicheng.cfd'
#                 node_det_dict['add'] = '104.16.245.116'
                node_det_dict['add'] = '172.66.43.109' 
                node_det_json = json.dumps(node_det_dict)
                node_mod = 'vmess://'+base64.b64encode(node_det_json.encode()).decode('UTF-8')
                nodes_mod_list.append(node_mod)
            else:
                # node_mod = re.sub(r'#(\S+)', '#%02.d' % nodes.index(node), node, 1, re.MULTILINE)
                node_mod = re.sub(r'#', f'#{y}-{m}-{d}-', node, 1, re.MULTILINE)
                nodes_mod_list.append(node_mod)
                # print(node_mod)
    return '\n'.join(nodes_mod_list)


def GenNodesFile(urls, flag):
    global d

    for url in urls:
        print(url)
        res = s.get(url, headers=headers, proxies=proxies)
        text = res.text
        d = '%d' % (int(d) - urls.index(url))
        if "<html" not in text:
            break

    if 'https://' == text[:8]:
        nodes = re.findall(r'url=(\S+)&insert=', unquote(text))[0].split('|')
        nodes_ori = base64.b64encode('\n'.join(nodes).encode(encoding='UTF-8')).decode('UTF-8')
    else:
        nodes = base64.b64decode(text).decode('UTF-8').split('\n')
        nodes_ori = text

    nodes_b64_en = base64.b64encode(modIP(nodes).encode(encoding='UTF-8'))
    nodes_b64_de = nodes_b64_en.decode('UTF-8')

    with open(f'{flag}_nodes_mod.txt', 'w', encoding='UTF-8') as w:
        w.write(nodes_b64_de)
    with open(f'{flag}_nodes_ori.txt', 'w', encoding='UTF-8') as w:
        w.write(nodes_ori)
        

if __name__ == "__main__":

    s = requests.session()

    y = time.strftime('%Y')
    m = time.strftime('%m')
    d = time.strftime('%d')

    clashnode_url = 'https://clashnode.com/wp-content/uploads/{}/{}/{}.txt'
    clashnode_urls = [clashnode_url.format(y, m, y+m+'%02d'%i) for i in range(int(d), 0, -1)]

    nodefree_url = 'https://nodefree.org/dy/{}/{}/{}.txt'
    nodefree_urls = [nodefree_url.format(y, m, y+m+'%02d'%i) for i in range(int(d), 0, -1)]
    
    other_urls = ['https://raw.iqiq.io/ermaozi/get_subscribe/main/subscribe/v2ray.txt']

    GenNodesFile(clashnode_urls, 'clashnode')
    GenNodesFile(nodefree_urls, 'nodefree')
#     GenNodesFile(other_urls, 'other')
