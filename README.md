# ucas-ncov-autoreport

## 国科大疫情上报每日自动化脚本

本程序仅限日常正常情况使用
大家一定要重视疫情，若有情况一定要及时手动上报！

## 使用方法：

根据代码填写自己的表格信息，包括姓名、学号，地址信息。
填写自己的sep账户的账号和密码
每日定时执行即可。每日早上九点、九点半两次提交的定时执行脚本：

修改位置为代码最底部执行的代码段
地理位置参考代码中的地理位置案例数据
```
if __name__ == '__main__':
    formData = composeFormData(u'姓名', '2018E80090xx000', u'省', u'市', u'县', u'街道小区')
    print(formData)
    save_record('username', 'password', formData)
```

`0,30 9 * * * python3 /path/to/ncov_save.py`
