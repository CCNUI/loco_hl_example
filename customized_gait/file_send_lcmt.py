"""LCM类型定义 该文件由LCM自动生成。
结构体 file_send_lcmt {
    string data;  # 数据字符串
}
"""
try:
    import cStringIO.StringIO as BytesIO  # 尝试导入cStringIO模块中的StringIO作为BytesIO
except ImportError:
    from io import BytesIO  # 如果导入失败，则从io模块中导入BytesIO
import struct  # 导入struct模块用于处理二进制数据

class file_send_lcmt(object):
    __slots__ = ["data"]  # 声明一个槽，只允许包含data属性

    __typenames__ = ["string"]  # 声明属性的数据类型为字符串

    __dimensions__ = [None]  # 声明属性的维度，无特定维度

    def __init__(self):
        self.data = ""  # 初始化data属性为空字符串

    def encode(self):
        buf = BytesIO()  # 创建一个BytesIO对象用于存储编码后的数据
        buf.write(file_send_lcmt._get_packed_fingerprint())  # 写入指纹
        self._encode_one(buf)  # 编码数据
        return buf.getvalue()  # 返回编码后的二进制数据

    def _encode_one(self, buf):
        __data_encoded = self.data.encode('utf-8')  # 将data属性编码为UTF-8格式
        buf.write(struct.pack('>I', len(__data_encoded)+1))  # 写入数据长度，加1用于结尾的空字节
        buf.write(__data_encoded)  # 写入编码后的数据
        buf.write(b"\0")  # 写入结尾的空字节

    def decode(data):
        if hasattr(data, 'read'):
            buf = data  # 如果data对象有read方法，则直接使用
        else:
            buf = BytesIO(data)  # 否则创建一个BytesIO对象
        if buf.read(8) != file_send_lcmt._get_packed_fingerprint():
            raise ValueError("Decode error")  # 如果指纹不匹配，则抛出解码错误
        return file_send_lcmt._decode_one(buf)  # 返回解码后的对象
    decode = staticmethod(decode)  # 声明为静态方法

    def _decode_one(buf):
        self = file_send_lcmt()  # 创建一个新的file_send_lcmt对象
        __data_len = struct.unpack('>I', buf.read(4))[0]  # 读取数据长度
        self.data = buf.read(__data_len)[:-1].decode('utf-8', 'replace')  # 读取数据并解码
        return self  # 返回解码后的对象
    _decode_one = staticmethod(_decode_one)  # 声明为静态方法

    def _get_hash_recursive(parents):
        if file_send_lcmt in parents: return 0  # 如果file_send_lcmt在父对象中，则返回0
        tmphash = (0x90df9b84cdceaf0a) & 0xffffffffffffffff  # 计算临时哈希值
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff  # 计算哈希值
        return tmphash  # 返回哈希值
    _get_hash_recursive = staticmethod(_get_hash_recursive)  # 声明为静态方法
    _packed_fingerprint = None  # 初始化指纹为None

    def _get_packed_fingerprint():
        if file_send_lcmt._packed_fingerprint is None:
            file_send_lcmt._packed_fingerprint = struct.pack(">Q", file_send_lcmt._get_hash_recursive([]))  # 计算并存储指纹
        return file_send_lcmt._packed_fingerprint  # 返回指纹
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)  # 声明为静态方法

    def get_hash(self):
        """获取结构体的LCM哈希值"""
        return struct.unpack(">Q", file_send_lcmt._get_packed_fingerprint())[0]  # 返回解包后的哈希值
