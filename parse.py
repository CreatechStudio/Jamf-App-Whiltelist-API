import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# 读取XML文件
xml_file = 'updated_config.xml'
tree = ET.parse(xml_file)
root = tree.getroot()

# 定位到<general>/<payloads>节点
payloads = root.find('./general/payloads')

# 获取内容
raw_content = payloads.text

# 将XML内容美化
def prettify(xml_string):
    """返回美化后的XML字符串"""
    reparsed = minidom.parseString(xml_string)
    return reparsed.toprettyxml(indent="  ")

# 美化后的XML内容
pretty_xml = prettify(raw_content)

# 保存美化后的内容到文件
with open('parsed.xml', 'w', encoding='utf-8') as f:
    f.write(pretty_xml)

print("美化后的内容已保存至 parsed.xml 文件。")