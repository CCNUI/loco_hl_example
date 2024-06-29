# LCM类型定义 该文件由LCM自动生成。
try:
    import cStringIO.StringIO as BytesIO  # 尝试导入cStringIO模块中的StringIO作为BytesIO
except ImportError:
    from io import BytesIO  # 如果导入失败，则从io模块中导入BytesIO
import struct  # 导入struct模块用于处理二进制数据

class robot_control_cmd_lcmt(object):
    __slots__ = ["mode", "gait_id", "contact", "life_count", "vel_des", "rpy_des", "pos_des", "acc_des", "ctrl_point", "foot_pose", "step_height", "value", "duration"]  # 声明槽，只允许包含这些属性

    __typenames__ = ["int8_t", "int8_t", "int8_t", "int8_t", "float", "float", "float", "float", "float", "float", "float", "int32_t", "int32_t"]  # 声明属性的数据类型

    __dimensions__ = [None, None, None, None, [3], [3], [3], [6], [3], [6], [2], None, None]  # 声明属性的维度

    def __init__(self):
        self.mode = 0  # 机器人控制模式
        self.gait_id = 0  # 步态ID
        self.contact = 0  # 接触状态
        self.life_count = 0  # 生命周期计数
        self.vel_des = [0.0 for _ in range(3)]  # 期望速度
        self.rpy_des = [0.0 for _ in range(3)]  # 期望的滚转、俯仰、偏航角
        self.pos_des = [0.0 for _ in range(3)]  # 期望的位置
        self.acc_des = [0.0 for _ in range(6)]  # 期望的加速度
        self.ctrl_point = [0.0 for _ in range(3)]  # 控制点
        self.foot_pose = [0.0 for _ in range(6)]  # 足部姿态
        self.step_height = [0.0 for _ in range(2)]  # 步高
        self.value = 0  # 其他值
        self.duration = 0  # 持续时间

    def encode(self):
        buf = BytesIO()  # 创建一个BytesIO对象用于存储编码后的数据
        buf.write(robot_control_cmd_lcmt._get_packed_fingerprint())  # 写入指纹
        self._encode_one(buf)  # 编码数据
        return buf.getvalue()  # 返回编码后的二进制数据

    def _encode_one(self, buf):
        buf.write(struct.pack(">bbbb", self.mode, self.gait_id, self.contact, self.life_count))  # 编码并写入模式、步态ID、接触状态和生命周期计数
        buf.write(struct.pack('>3f', *self.vel_des[:3]))  # 编码并写入期望速度
        buf.write(struct.pack('>3f', *self.rpy_des[:3]))  # 编码并写入期望的滚转、俯仰、偏航角
        buf.write(struct.pack('>3f', *self.pos_des[:3]))  # 编码并写入期望的位置
        buf.write(struct.pack('>6f', *self.acc_des[:6]))  # 编码并写入期望的加速度
        buf.write(struct.pack('>3f', *self.ctrl_point[:3]))  # 编码并写入控制点
        buf.write(struct.pack('>6f', *self.foot_pose[:6]))  # 编码并写入足部姿态
        buf.write(struct.pack('>2f', *self.step_height[:2]))  # 编码并写入步高
        buf.write(struct.pack(">ii", self.value, self.duration))  # 编码并写入其他值和持续时间

    def decode(data):
        if hasattr(data, 'read'):
            buf = data  # 如果data对象有read方法，则直接使用
        else:
            buf = BytesIO(data)  # 否则创建一个BytesIO对象
        if buf.read(8) != robot_control_cmd_lcmt._get_packed_fingerprint():
            raise ValueError("Decode error")  # 如果指纹不匹配，则抛出解码错误
        return robot_control_cmd_lcmt._decode_one(buf)  # 返回解码后的对象
    decode = staticmethod(decode)  # 声明为静态方法

    def _decode_one(buf):
        self = robot_control_cmd_lcmt()  # 创建一个新的robot_control_cmd_lcmt对象
        self.mode, self.gait_id, self.contact, self.life_count = struct.unpack(">bbbb", buf.read(4))  # 解码模式、步态ID、接触状态和生命周期计数
        self.vel_des = struct.unpack('>3f', buf.read(12))  # 解码期望速度
        self.rpy_des = struct.unpack('>3f', buf.read(12))  # 解码期望的滚转、俯仰、偏航角
        self.pos_des = struct.unpack('>3f', buf.read(12))  # 解码期望的位置
        self.acc_des = struct.unpack('>6f', buf.read(24))  # 解码期望的加速度
        self.ctrl_point = struct.unpack('>3f', buf.read(12))  # 解码控制点
        self.foot_pose = struct.unpack('>6f', buf.read(24))  # 解码足部姿态
        self.step_height = struct.unpack('>2f', buf.read(8))  # 解码步高
        self.value, self.duration = struct.unpack(">ii", buf.read(8))  # 解码其他值和持续时间
        return self  # 返回解码后的对象
    _decode_one = staticmethod(_decode_one)  # 声明为静态方法

    def _get_hash_recursive(parents):
        if robot_control_cmd_lcmt in parents: return 0  # 如果robot_control_cmd_lcmt在父对象中，则返回0
        tmphash = (0x476b61e296af96f5) & 0xffffffffffffffff  # 计算临时哈希值
        tmphash = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff  # 计算哈希值
        return tmphash  # 返回哈希值
    _get_hash_recursive = staticmethod(_get_hash_recursive)  # 声明为静态方法
    _packed_fingerprint = None  # 初始化指纹为None

    def _get_packed_fingerprint():
        if robot_control_cmd_lcmt._packed_fingerprint is None:
            robot_control_cmd_lcmt._packed_fingerprint = struct.pack(">Q", robot_control_cmd_lcmt._get_hash_recursive([]))  # 计算并存储指纹
        return robot_control_cmd_lcmt._packed_fingerprint  # 返回指纹
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)  # 声明为静态方法

    def get_hash(self):
        """获取结构体的LCM哈希值"""
        return struct.unpack(">Q", robot_control_cmd_lcmt._get_packed_fingerprint())[0]  # 返回解包后的哈希值

class robot_control_response_lcmt(object):
    __slots__ = ["mode", "gait_id", "contact", "order_process_bar", "switch_status", "ori_error", "footpos_error", "motor_error"]  # 声明槽，只允许包含这些属性

    __typenames__ = ["int8_t", "int8_t", "int8_t", "int8_t", "int8_t", "int8_t", "int16_t", "int32_t"]  # 声明属性的数据类型

    __dimensions__ = [None, None, None, None, None, None, None, [12]]  # 声明属性的维度

    def __init__(self):
        self.mode = 0  # 机器人控制模式
        self.gait_id = 0  # 步态ID
        self.contact = 0  # 接触状态
        self.order_process_bar = 0  # 订单处理进度条
        self.switch_status = 0  # 开关状态
        self.ori_error = 0  # 方向误差
        self.footpos_error = 0  # 足部位置误差
        self.motor_error = [0 for _ in range(12)]  # 电机误差

    def encode(self):
        buf = BytesIO()  # 创建一个BytesIO对象用于存储编码后的数据
        buf.write(robot_control_response_lcmt._get_packed_fingerprint())  # 写入指纹
        self._encode_one(buf)  # 编码数据
        return buf.getvalue()  # 返回编码后的二进制数据

    def _encode_one(self, buf):
        buf.write(struct.pack(">bbbbbbh", self.mode, self.gait_id, self.contact, self.order_process_bar, self.switch_status, self.ori_error, self.footpos_error))  # 编码并写入模式、步态ID、接触状态、订单处理进度条、开关状态、方向误差和足部位置误差
        buf.write(struct.pack('>12i', *self.motor_error[:12]))  # 编码并写入电机误差

    def decode(data):
        if hasattr(data, 'read'):
            buf = data  # 如果data对象有read方法，则直接使用
        else:
            buf = BytesIO(data)  # 否则创建一个BytesIO对象
        if buf.read(8) != robot_control_response_lcmt._get_packed_fingerprint():
            raise ValueError("Decode error")  # 如果指纹不匹配，则抛出解码错误
        return robot_control_response_lcmt._decode_one(buf)  # 返回解码后的对象
    decode = staticmethod(decode)  # 声明为静态方法

    def _decode_one(buf):
        self = robot_control_response_lcmt()  # 创建一个新的robot_control_response_lcmt对象
        self.mode, self.gait_id, self.contact, self.order_process_bar, self.switch_status, self.ori_error, self.footpos_error = struct.unpack(">bbbbbbh", buf.read(8))  # 解码模式、步态ID、接触状态、订单处理进度条、开关状态、方向误差和足部位置误差
        self.motor_error = struct.unpack('>12i', buf.read(48))  # 解码电机误差
        return self  # 返回解码后的对象
    _decode_one = staticmethod(_decode_one)  # 声明为静态方法

    def _get_hash_recursive(parents):
        if robot_control_response_lcmt in parents: return 0  # 如果robot_control_response_lcmt在父对象中，则返回0
        tmphash = (0x485da98216eda8c7) & 0xffffffffffffffff  # 计算临时哈希值
        tmphash = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff  # 计算哈希值
        return tmphash  # 返回哈希值
    _get_hash_recursive = staticmethod(_get_hash_recursive)  # 声明为静态方法
    _packed_fingerprint = None  # 初始化指纹为None

    def _get_packed_fingerprint():
        if robot_control_response_lcmt._packed_fingerprint is None:
            robot_control_response_lcmt._packed_fingerprint = struct.pack(">Q", robot_control_response_lcmt._get_hash_recursive([]))  # 计算并存储指纹
        return robot_control_response_lcmt._packed_fingerprint  # 返回指纹
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)  # 声明为静态方法

    def get_hash(self):
        """获取结构体的LCM哈希值"""
        return struct.unpack(">Q", robot_control_response_lcmt._get_packed_fingerprint())[0]  # 返回解包后的哈希值
