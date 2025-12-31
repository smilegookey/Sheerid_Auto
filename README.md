# SheerID Verification Tool

ChatGPT Plus 身份验证工具

**作者: dy安心大油条**

## 功能说明

本工具用于自动化完成 ChatGPT Plus 的身份验证流程，通过 SheerID 进行验证。

## 环境要求

- Python 3.8+
- 可选：requests-go (支持 TLS 指纹模拟)

## 安装依赖

```bash
# 基础依赖
pip install requests

# 可选：TLS 指纹模拟 (推荐)
pip install requests-go
```

## 配置说明

### 1. 配置文件 (config.json)

复制 `config.example.json` 为 `config.json`，填写以下信息：

```json
{
    "accessToken": "你的 ChatGPT accessToken",
    "programId": "690415d58971e73ca187d8c9",
    "email": {
        "imap_server": "imap.gmail.com",
        "imap_port": 993,
        "email_address": "your_email@gmail.com",
        "email_password": "your_app_password",
        "use_ssl": true
    }
}
```

#### 获取 accessToken

1. 登录 https://chatgpt.com
2. 访问 https://chatgpt.com/api/auth/session
3. 页面会显示 JSON 数据，找到 `accessToken` 字段
4. 复制 `accessToken` 的值填入配置文件

#### 邮箱配置（二选一）

本工具支持两种邮箱接入方式，选择其中一种即可：

---

**方式一：IMAP（通用邮箱）**

适用于 Gmail、Outlook、QQ 邮箱等支持 IMAP 的邮箱服务。

```json
"email": {
    "type": "imap",
    "imap_server": "imap.gmail.com",
    "imap_port": 993,
    "email_address": "your_email@gmail.com",
    "email_password": "your_app_password",
    "use_ssl": true
}
```

常用 IMAP 服务器：
| 邮箱 | IMAP 服务器 | 端口 |
|------|-------------|------|
| Gmail | imap.gmail.com | 993 |
| Outlook | outlook.office365.com | 993 |
| QQ 邮箱 | imap.qq.com | 993 |
| 163 邮箱 | imap.163.com | 993 |

> 注意：Gmail 需要开启"应用专用密码"，QQ 邮箱需要使用授权码

---

**方式二：CloudMail API（临时邮箱服务）**

适用于自建的 CloudMail 临时邮箱服务，支持 API 方式收取邮件。

```json
"email": {
    "type": "cloudmail",
    "api_url": "https://your-cloudmail-api.com",
    "admin_email": "admin@example.com",
    "admin_password": "your_admin_password",
    "email_address": "receive@yourdomain.com"
}
```

CloudMail API 接口说明：
- `POST /api/public/genToken` - 获取访问 Token
- `POST /api/public/addUser` - 添加邮箱用户
- `POST /api/public/emailList` - 获取邮件列表

> 提示：CloudMail 适合批量验证场景，可使用自定义域名邮箱

### 2. 数据文件 (data.txt)

复制 `data.example.txt` 为 `data.txt`，填写验证数据：

```
# 格式: firstName|lastName|branch|birthDate|dischargeDate
JOHN MICHAEL|SMITH|Army|1990-05-15|2023-06-01
DAVID JAMES|JOHNSON|Marine Corps|1988-12-20|2022-03-15
```

**branch 可选值:**
- Army
- Air Force
- Navy
- Marine Corps
- Coast Guard
- Space Force
- Army National Guard
- Army Reserve
- Air National Guard
- Air Force Reserve
- Navy Reserve
- Marine Corps Forces Reserve
- Coast Guard Reserve

### 3. 代理配置 (proxy.txt) - 可选

复制 `proxy.example.txt` 为 `proxy.txt`，填写代理信息：

```
# 格式1: ip:port:username:password
192.168.1.100:1080:user123:pass456

# 格式2: ip:port
192.168.1.101:8080

# 格式3: URL 格式
socks5://user:pass@proxy.example.com:1080
```

### 4. TLS 指纹 (tls_json/) - 可选

创建 `tls_json` 目录，放入 Chrome TLS 指纹 JSON 文件，可增强反检测能力。

## 使用方法

```bash
python main.py
```

### 运行参数

支持通过参数自定义配置、数据及输出路径，或在成功后继续处理后续数据：

```bash
python main.py \
  --config ./config.json \
  --data ./data.txt \
  --proxy ./proxy.txt \
  --tls-json-dir ./tls_json \
  --result ./result.txt \
  --used ./used.txt \
  --continue-on-success
```

参数说明：

- `--config`：配置文件路径，默认 `config.json`
- `--data`：数据文件路径，默认 `data.txt`
- `--proxy`：代理配置文件路径，默认 `proxy.txt`
- `--tls-json-dir`：TLS 指纹目录，默认 `tls_json`
- `--result`：结果输出文件，默认 `result.txt`
- `--used`：已使用数据记录文件，默认 `used.txt`
- `--continue-on-success`：启用后，验证成功后不会立即退出，会继续处理剩余数据

## 输出文件

- `result.txt` - 验证结果日志
- `used.txt` - 已使用的数据记录

## 注意事项

1. 请确保使用真实有效的身份信息
2. 同一身份信息只能验证一次
3. 建议使用代理和 TLS 指纹模拟以降低被检测风险
4. accessToken 有效期有限，过期需重新获取

## 免责声明

本工具仅供学习研究使用，请遵守相关法律法规和服务条款。使用本工具所产生的任何后果由使用者自行承担。

## License

MIT License

## 运行截图

![运行截图](screenshot.png)
