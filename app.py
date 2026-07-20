from flask import Flask, request, jsonify
import asyncio, aiohttp, ssl, json, random, jwt, time
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Pb2 import MajoRLoGinrEq_pb2, MajoRLoGinrEs_pb2, PorTs_pb2
from protobuf_decoder.protobuf_decoder import Parser

app = Flask(__name__)

# ================== المفاتيح ==================
AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

# ================== دوال مساعدة ==================
def encPacket(hexStr, k, iv):
    return AES.new(k, AES.MODE_CBC, iv).encrypt(pad(bytes.fromhex(hexStr), 16)).hex()

def decPacket(hexStr, k, iv):
    return unpad(AES.new(k, AES.MODE_CBC, iv).decrypt(bytes.fromhex(hexStr)), 16).hex()

async def EnC_PacKeT(hexStr, key, iv):
    return encPacket(hexStr, key, iv)

def decodeHex(h):
    r = hex(h)[2:]
    return "0" + r if len(r) == 1 else r

async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

# ================== User Agent ==================
async def Ua():
    versions = ['4.0.18P6', '4.0.19P7', '4.0.20P1']
    models = ['SM-A125F', 'SM-A225F', 'SM-A325M', 'SM-A515F']
    android_versions = ['9', '10', '11', '12']
    languages = ['en-US', 'es-MX', 'pt-BR']
    countries = ['USA', 'MEX', 'BRA']
    return f"GarenaMSDK/{random.choice(versions)}({random.choice(models)};Android {random.choice(android_versions)};{random.choice(languages)};{random.choice(countries)};)"

# ================== دوال تسجيل الدخول ==================
async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": await Ua(),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status != 200:
                    return None, None
                data = await response.json()
                return data.get("open_id"), data.get("access_token")
    except:
        return None, None

async def EncRypTMajoRLoGin(open_id, access_token, platform_id=2):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = platform_id
    major_login.client_version = "1.126.1"
    major_login.system_software = "Android OS 9 / API-28"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019116753"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggpolarbear.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    headers = {
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': 'OB54',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-GA': 'v1 1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
        'Host': 'loginbp.ggpolarbear.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers, ssl=ssl_context) as response:
                if response.status == 200:
                    return await response.read()
                return None
    except:
        return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    headers = {
        'Expect': '100-continue',
        'Authorization': f'Bearer {token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB54',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
        'Host': 'clientbp.ggpolarbear.com',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers, ssl=ssl_context) as response:
                if response.status == 200:
                    return await response.read()
                return None
    except:
        return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    try:
        proto = MajoRLoGinrEs_pb2.MajorLoginRes()
        proto.ParseFromString(MajoRLoGinResPonsE)
        return proto
    except:
        return None

async def DecRypTLoGinDaTa(LoGinDaTa):
    try:
        proto = PorTs_pb2.GetLoginData()
        proto.ParseFromString(LoGinDaTa)
        return proto
    except:
        return None

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = hex(timestamp)[2:]
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9:
        headers = '0000000'
    elif uid_length == 8:
        headers = '00000000'
    elif uid_length == 10:
        headers = '000000'
    elif uid_length == 7:
        headers = '000000000'
    else:
        headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

# ================== دوال فك التشفير ==================
def fixParsed(parsed):
    d = {}
    for r in parsed:
        fd = {'wire_type': r.wire_type}
        if r.wire_type in ("varint", "string", "bytes"):
            fd['data'] = r.data
        elif r.wire_type == 'length_delimited':
            fd['data'] = fixParsed(r.data.results)
        d[r.field] = fd
    return d

def decodePacket(hexInput):
    try:
        parsed = Parser().parse(hexInput)
        return json.dumps(fixParsed(parsed))
    except Exception:
        return None

# ================== API تسجيل الدخول ==================
@app.route('/login', methods=['POST'])
def login_api():
    """API لتسجيل الدخول باستخدام Pb2"""
    try:
        data = request.get_json()
        uid = data.get('uid')
        password = data.get('password')
        connect_chat = data.get('connect_chat', True)  # افتراضي True
        
        if not uid or not password:
            return jsonify({
                "success": False,
                "message": "uid and password required"
            }), 400
        
        # تشغيل الدوال غير المتزامنة
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def do_login():
            # 1. الحصول على Access Token
            open_id, access_token = await GeNeRaTeAccEss(uid, password)
            if not open_id or not access_token:
                return None
            
            # 2. بناء Payload
            platform_id = 2
            payload = await EncRypTMajoRLoGin(open_id, access_token, platform_id)
            
            # 3. MajorLogin
            login_response = await MajorLogin(payload)
            if not login_response:
                return None
            
            # 4. فك MajorLogin
            login_data = await DecRypTMajoRLoGin(login_response)
            if not login_data:
                return None
            
            token = login_data.token
            key = login_data.key.hex()
            iv = login_data.iv.hex()
            timestamp = login_data.timestamp
            target = login_data.account_uid
            region = login_data.region
            url = login_data.url
            
            # 5. الحصول على البورتات
            ports_response = await GetLoginData(url, payload, token)
            if not ports_response:
                return None
            
            ports_data = await DecRypTLoGinDaTa(ports_response)
            online_ip, online_port = ports_data.Online_IP_Port.split(":")
            chat_ip, chat_port = ports_data.AccountIP_Port.split(":")
            account_name = ports_data.AccountName
            
            # 6. بناء Auth Token
            auth_token = await xAuThSTarTuP(int(target), token, int(timestamp), key, iv)
            
            return {
                "success": True,
                "uid": uid,
                "target": target,
                "account_name": account_name,
                "region": region,
                "url": url,
                "token": token,
                "key": key,
                "iv": iv,
                "auth_token": auth_token,
                "online_ip": online_ip,
                "online_port": online_port,
                "chat_ip": chat_ip,
                "chat_port": chat_port,
                "connect_chat": connect_chat
            }
        
        result = loop.run_until_complete(do_login())
        loop.close()
        
        if result:
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "message": "Login failed"
            }), 401
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# ================== API للتحقق من التوكن ==================
@app.route('/verify', methods=['POST'])
def verify_token():
    """API للتحقق من صحة التوكن"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({"success": False, "message": "token required"}), 400
        
        # فك التوكن
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        return jsonify({
            "success": True,
            "account_id": decoded.get('account_id'),
            "nickname": decoded.get('nickname'),
            "region": decoded.get('noti_region'),
            "exp": decoded.get('exp')
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "status": "online",
        "message": "Login API is running",
        "endpoints": {
            "/login": "POST - Login with uid and password",
            "/verify": "POST - Verify token"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)