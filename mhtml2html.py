from tqdm import *
import os

def mhtml_to_html(mhtml_name):
    """将MHTML转换为标准HTML"""
    from bs4 import BeautifulSoup
    import email
    from email import policy
    
    title=mhtml_name[:-5]
    
    with open(mhtml_name, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
    
    # 提取主要HTML内容
    html_content = None
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True)
            charset = part.get_content_charset('utf-8')
            html_content = html_content.decode(charset, errors='ignore')
            break
    
    if html_content:
        # 清理不需要的META标签
        soup = BeautifulSoup(html_content, 'html.parser')
        for meta in soup.select('meta[http-equiv="Content-Type"]'):
            meta.decompose()
        
        with open(title+'html', 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True
    return False


files = [f for f in os.listdir('./') if f.endswith('.mhtml')]

# 创建进度条
for file in tqdm(files):
    mhtml_to_html(file)