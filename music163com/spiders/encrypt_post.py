import base64
import codecs

from Crypto.Cipher import AES


# 法一：
class AESCipher:
    """AES 加密部分"""

    def __init__(self, key):
        self.key = key
        self.iv = "0102030405060708"  # 用来填充缺失内容，JavaScript 中已给出

    def pad(self, text):
        """加密内容必须为 16 字节的倍数，填充"""
        text_length = len(text.encode("utf-8"))  # 计算 encode 之后的长度，以应对 non-ascii 字符
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def encrypt(self, text):
        """加密函数"""
        text = self.pad(text)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(text)).decode("utf-8")


def RSA_encrypt(text, key, f):
    """RSA 加密部分"""
    text = bytes(text[::-1], "utf-8")  # 字符串逆序并转换成 byte 类型数据
    # RSA加密
    sec_key = int(codecs.encode(text, encoding="hex"), 16) ** int(key, 16) % int(f, 16)
    print(codecs.encode(text, encoding="hex"))
    print(int(codecs.encode(text, encoding="hex"), 16))
    print(int(key, 16))
    print(int(f, 16))

    return format(sec_key, "x").zfill(256)


def get_encrypt_text(post_data):
    # 后 3 个参数
    str1 = "010001"
    str2 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    str3 = "0CoJUm6Qyw8W8jud"

    # 随机数 i 直接人工指定
    i = "0000000000000000"

    temp = AESCipher(str3).encrypt(post_data)
    encText = AESCipher(i).encrypt(temp)
    encSecKey = RSA_encrypt(i, str1, str2)

    return {"params": encText, "encSecKey": encSecKey}


# 使用方式：get_encrypt_text(post_data)


# ----- 分隔符 -----


# 法二：
class Encrypt_music163com:
    def __init__(self):
        self.keys = ["0CoJUm6Qyw8W8jud", "0000000000000000"]

    def pad(self, text):
        """加密内容必须为 16 字节的倍数，填充"""
        text_length = len(text.encode("utf-8"))  # 计算 encode 之后的长度，以应对 non-ascii 字符
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def encrypt(self, post_data):
        """加密"""
        for key in self.keys:
            cipher = AES.new(key, AES.MODE_CBC, "0102030405060708")
            post_data = base64.b64encode(cipher.encrypt(self.pad(post_data))).decode(
                "utf-8"
            )
        # encSecKey 为 RSA_encrypt(i, str1, str2) 为常数，不用反复计算直接写出即可，此计算原本的开销巨大，直接写出可以大幅提升效率
        return {
            "params": post_data,
            "encSecKey": "babc57ca9e9ffb0a879ae290ac6cba6f60620aa9ae3b36a84585e23bbc73d73b13a2ebab4aa2ee80544d255727adc5a04db613d77d02a62a52b3a03134d16f191d54675f560f797c7f03e3a30c43df8b1b49878fd225b62f5f78041427debc3e95b93582f130618630702621da4eda9c71af91836cc39ab3b760b033643a1889",
        }


# 使用方式：Encrypt_music163com().encrypt(post_data)
