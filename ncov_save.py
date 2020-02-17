import requests
import time
import re
import json
import urllib

def login(username, password):
    # step1 拉取https://app.ucas.ac.cn/uc/wap/login， 以获取eai-sess
    login_page = requests.get('https://app.ucas.ac.cn/uc/wap/login')
    sess = re.search(r'eai-sess=(.*?);',login_page.headers['Set-Cookie'])
    cookie = 'eai-sess='+sess.group(1)+'; '
    print('fetch login page done')
    # step2 调用https://app.ucas.ac.cn/uc/wap/login/check接口，以获取UUkey
    headers={}
    headers['Content-Type']='application/x-www-form-urlencoded'
    headers['Cookie'] = cookie
    form = {'username': username, 'password': password}
    login_response = requests.post('https://app.ucas.ac.cn/uc/wap/login/check', data=form, headers = headers)
    uukey = re.search(r'UUkey=(.*?);',login_response.headers['Set-Cookie'])
    cookie += 'UUkey='+uukey.group(1)+';'
    print('do login check, get cookie:' + cookie)
    return cookie
# 地址样例数据
# {
# 	"address": "内蒙古自治区通辽市科尔沁左翼中旗",
# 	"details": "XX街道XX家园",
# 	"province": {
# 		"label": "内蒙古自治区",
# 		"value": ""
# 	},
# 	"city": {
# 		"label": "通辽市",
# 		"value": ""
# 	},
# 	"area": {
# 		"label": "科尔沁左翼中旗",
# 		"value": ""
# 	}
# }
def composeFormData(realname, number, province, city, area, details):
    address_data = {
	    "address": province + city + area,
        "details":  details,
        "province": {
            "label": province,
            "value": ""
        },
        "city": {
            "label": city,
            "value": ""
        },
        "area": {
            "label": area,
            "value": ""
        }
    }
    # 正常的数据
    normal_fields = '''&szgj=&old_szgj=&old_sfzx=0&sfzx=0&szdd=国内&ismoved=1&tw=3&bztcyy=&sftjwh=0&sftjhb=0&sfcxtz=0&sfyyjc=&jcjgqr=&sfjcwhry=0&sfjchbry=0&sfjcbh=0&jcbhlx=&sfcyglq=0&gllx=&sfcxzysx=0&old_szdd=&old_city={"address":"","details":"","province":{"label":"","value":""},"city":{"label":"","value":""},"area":{"label":"","value":""}}&geo_api_infot={"area":{"label":"","value":""},"city":{"label":"","value":""},"address":"","details":"","province":{"label":"","value":""}}&fjsj=&jcbhrq=&glksrq=&fxyy=&jcjg=&jcjgt=&qksm=&remark=&jcjgqk=1&jcwhryfs=&jchbryfs=&app_id=ucas'''
    date = time.strftime('%Y-%m-%d' , time.localtime())
    normal_fields = 'realname=' + realname + '&number=' + number + normal_fields
    normal_fields += '&date='+date
    normal_fields += '&geo_api_info=' + json.dumps(address_data)
    # formdata = urllib.parse.quote(normal_fields)
    return normal_fields
    

def save_record(username, password, form_data):
    # 样例数据
    # form_str = "realname=%E6%97%B6%E5%BF%97%E8%BE%BE&number=2018E8009064014&szgj=&old_szgj=&old_sfzx=0&sfzx=0&szdd=%E5%9B%BD%E5%86%85&ismoved=1&tw=3&bztcyy=&sftjwh=0&sftjhb=0&sfcxtz=0&sfyyjc=&jcjgqr=&sfjcwhry=0&sfjchbry=0&sfjcbh=0&jcbhlx=&sfcyglq=0&gllx=&sfcxzysx=0&old_szdd=&geo_api_info=%7B%22address%22%3A%22%E5%86%85%E8%92%99%E5%8F%A4%E8%87%AA%E6%B2%BB%E5%8C%BA%E9%80%9A%E8%BE%BD%E5%B8%82%E7%A7%91%E5%B0%94%E6%B2%81%E5%B7%A6%E7%BF%BC%E4%B8%AD%E6%97%97%22%2C%22details%22%3A%22%E4%BF%9D%E5%BA%B7%E8%A1%97%E9%81%93%E9%A6%A8%E6%80%A1%E5%AE%B6%E5%9B%AD%22%2C%22province%22%3A%7B%22label%22%3A%22%E5%86%85%E8%92%99%E5%8F%A4%E8%87%AA%E6%B2%BB%E5%8C%BA%22%2C%22value%22%3A%22%22%7D%2C%22city%22%3A%7B%22label%22%3A%22%E9%80%9A%E8%BE%BD%E5%B8%82%22%2C%22value%22%3A%22%22%7D%2C%22area%22%3A%7B%22label%22%3A%22%E7%A7%91%E5%B0%94%E6%B2%81%E5%B7%A6%E7%BF%BC%E4%B8%AD%E6%97%97%22%2C%22value%22%3A%22%22%7D%7D&old_city=%7B%22address%22%3A%22%22%2C%22details%22%3A%22%22%2C%22province%22%3A%7B%22label%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22city%22%3A%7B%22label%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22area%22%3A%7B%22label%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D&geo_api_infot=%7B%22area%22%3A%7B%22label%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22city%22%3A%7B%22label%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22address%22%3A%22%22%2C%22details%22%3A%22%22%2C%22province%22%3A%7B%22label%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D&date=$DATE$&fjsj=&jcbhrq=&glksrq=&fxyy=&jcjg=&jcjgt=&qksm=&remark=&jcjgqk=1&jcwhryfs=&jchbryfs=&app_id=ucas"
    form_str = form_data.encode('utf-8')
    headers={}
    headers['Content-Type']='application/x-www-form-urlencoded'
    headers['Cookie'] = login(username, password)
    ncov_url = "https://app.ucas.ac.cn/ncov/api/default/save"
    res = requests.post(ncov_url, data=form_str, headers = headers) # 自动编码
    print(res.text)

if __name__ == '__main__':
    formData = composeFormData(u'姓名', '2018E80090xx000', u'省', u'市', u'县', u'街道小区')
    print(formData)
    save_record('username', 'password', formData)