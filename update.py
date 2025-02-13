JSS_URL = ""
CLIENT_ID = ""
CLIENT_TOKEN = ""
CONFIG_ID = 1

import re
import requests
import os

# 创建jamf_api_temp文件夹，如果不存在
temp_folder = 'jamf_api_temp'
os.makedirs(temp_folder, exist_ok=True)

auth_url = f'{JSS_URL}/api/oauth/token'
auth_headers = {'content-type': 'application/x-www-form-urlencoded'}
auth_body = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_TOKEN
}
auth_response = requests.post(auth_url, headers=auth_headers, data=auth_body)
bearer_token = auth_response.json()['access_token']

# 设置请求头
headers = {
    'Authorization': f'Bearer {bearer_token}'
}

# 请求的URL
get_url = f'{JSS_URL}/JSSResource/mobiledeviceconfigurationprofiles/id/{CONFIG_ID}/subset/General'

# 发送GET请求
get_response = requests.get(get_url, headers=headers)

# 检查请求是否成功
if get_response.status_code == 200:
    # 将响应内容保存到文件
    get_config_path = os.path.join(temp_folder, 'get_config.xml')
    with open(get_config_path, 'wb') as file:
        file.write(get_response.content)
    print("Oringin config has been saved to get_config.xml.")
else:
    print(f"GET request failed, HTTP code: {get_response.status_code}")
    print("Response Content:", get_response.text)


# 读取文件内容
with open(get_config_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# 使用正则表达式提取<payloads>标签之间的内容
payloads = re.findall(r'<payloads>(.*?)</payloads>', file_content, re.DOTALL)

if payloads:
    origin_payload = payloads[0]
    
    # 包名由用户输入
    package_name = input("Enter a bundle id: ")

    # 定义插入内容和定位字符串
    insert_string = f'&lt;string&gt;{package_name}&lt;/string&gt;'
    start_marker = '&lt;/array&gt;&lt;key&gt;whitelistedAppBundleIDs&lt;/key&gt;&lt;array&gt;'
    end_marker = '&lt;/array&gt;&lt;/dict&gt;&lt;/array&gt;&lt;/dict&gt;&lt;/plist&gt;'

    # 在指定位置插入包名
    updated_payload = origin_payload.replace(start_marker, insert_string + start_marker)
    updated_payload = updated_payload.replace(end_marker, insert_string + end_marker)

    # 将更新后的内容写回到文件
    updated_content = file_content.replace(origin_payload, updated_payload)

    updated_config_path = os.path.join(temp_folder, 'updated_config.xml')
    with open(updated_config_path, 'w', encoding='utf-8') as updated_file:
        updated_file.write(updated_content)

    print("Config has beed updated to updated_config.xml")
else:
    print("Cannot find <payloads> in get_config.xml。")

# 读取文件内容
with open(updated_config_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# 使用正则表达式提取<payloads>标签之间的内容
modified_payloads = re.findall(r'<payloads>(.*?)</payloads>', file_content, re.DOTALL)
modified_payloads = modified_payloads[0]

update_url = f'{JSS_URL}/JSSResource/mobiledeviceconfigurationprofiles/id/{CONFIG_ID}'

# 构建XML body
update_body = f'''
<configuration_profile>
    <general>
        <redeploy_on_update>All</redeploy_on_update>
        <payloads>{modified_payloads}</payloads>
    </general>
</configuration_profile>
'''

# 发送PUT请求
update_response = requests.put(update_url, headers=headers, data=update_body.encode('utf-8'))

# 检查请求是否成功
if update_response.status_code in [200, 201, 204]:
    print("PUT Request Success.")
    # 删除jamf_api_temp文件夹中的文件
    files_to_delete = [get_config_path, updated_config_path]
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"Temp file {file} has been deleted.")
        else:
            print(f"Temp file {file} not found.")
else:
    print(f"PUT request failed, HTTP code: {update_response.status_code}")
    print("Response Content:", update_response.text)
    print("Please debug by using temp files in jamf_api_temp folder.")