'''
本演示展示了基于LCM的MR813运动控制板的通信接口。
依赖项：
- robot_control_cmd_lcmt.py
- robot_control_response_lcmt.py
'''
import lcm  # 导入LCM模块
import sys  # 导入系统模块
import os  # 导入操作系统模块
import time  # 导入时间模块
from threading import Thread, Lock  # 从线程模块导入线程和锁

from robot_control_cmd_lcmt import robot_control_cmd_lcmt  # 导入robot_control_cmd_lcmt类
from robot_control_response_lcmt import robot_control_response_lcmt  # 导入robot_control_response_lcmt类

def main():
    Ctrl = Robot_Ctrl()  # 创建Robot_Ctrl对象
    Ctrl.run()  # 启动控制
    msg = robot_control_cmd_lcmt()  # 创建robot_control_cmd_lcmt对象
    try:
        msg.mode = 12  # 恢复站立模式
        msg.gait_id = 0
        msg.life_count += 1  # 当life_count更新时，命令将生效
        Ctrl.Send_cmd(msg)  # 发送命令
        Ctrl.Wait_finish(12, 0)  # 等待命令完成

        msg.mode = 62  # 握手模式，基于位置插值控制
        msg.gait_id = 2
        msg.life_count += 1
        Ctrl.Send_cmd(msg)
        Ctrl.Wait_finish(62, 2)

        msg.mode = 64  # 两足站立模式
        msg.gait_id = 0
        msg.life_count += 1
        Ctrl.Send_cmd(msg)
        Ctrl.Wait_finish(64, 0)

        msg.mode = 21  # 位置插值控制
        msg.gait_id = 0
        msg.rpy_des = [0, 0.3, 0]  # 抬头
        msg.duration = 500  # 预期执行时间，0.5秒
        msg.life_count += 1
        Ctrl.Send_cmd(msg)
        time.sleep(0.5)

        msg.mode = 21  # 位置插值控制
        msg.gait_id = 0
        msg.rpy_des = [0, -0.3, 0]  # 低头
        msg.duration = 300
        msg.life_count += 1
        Ctrl.Send_cmd(msg)
        time.sleep(0.3)

        msg.mode = 21  # 位置插值控制
        msg.gait_id = 5
        msg.rpy_des = [0, 0, 0]
        msg.pos_des = [0, 0, 0.22]  # 设置身体高度
        msg.duration = 400
        msg.life_count += 1
        Ctrl.Send_cmd(msg)
        time.sleep(1)

        msg.mode = 11  # 运动控制
        msg.gait_id = 26  # 快速小跑：10 中速小跑：3 慢速小跑：27 自变频：26
        msg.vel_des = [0, 0, 0.5]  # 转向
        msg.duration = 0  # 持续时间为0表示连续运动，直到使用新命令
                         # 连续运动可以中断非零持续时间的插值运动
        msg.step_height = [0.06, 0.06]  # 摆动腿的地面间隙
        msg.life_count += 1
        Ctrl.Send_cmd(msg)
        time.sleep(5)

        msg.mode = 7  # 纯阻尼模式
        msg.gait_id = 0
        msg.life_count += 1
        Ctrl.Send_cmd(msg)
        Ctrl.Wait_finish(7, 0)

    except KeyboardInterrupt:  # 捕获键盘中断
        pass
    Ctrl.quit()  # 退出控制
    sys.exit()  # 退出系统


class Robot_Ctrl(object):
    def __init__(self):
        self.rec_thread = Thread(target=self.rec_responce)  # 创建接收响应的线程
        self.send_thread = Thread(target=self.send_publish)  # 创建发送发布的线程
        self.lc_r = lcm.LCM("udpm://239.255.76.67:7670?ttl=255")  # 创建LCM接收对象
        self.lc_s = lcm.LCM("udpm://239.255.76.67:7671?ttl=255")  # 创建LCM发送对象
        self.cmd_msg = robot_control_cmd_lcmt()  # 创建命令消息对象
        self.rec_msg = robot_control_response_lcmt()  # 创建响应消息对象
        self.send_lock = Lock()  # 创建锁对象
        self.delay_cnt = 0  # 初始化延迟计数器
        self.mode_ok = 0  # 初始化模式状态
        self.gait_ok = 0  # 初始化步态状态
        self.runing = 1  # 初始化运行状态

    def run(self):
        self.lc_r.subscribe("robot_control_response", self.msg_handler)  # 订阅机器人控制响应
        self.send_thread.start()  # 启动发送线程
        self.rec_thread.start()  # 启动接收线程

    def msg_handler(self, channel, data):
        self.rec_msg = robot_control_response_lcmt().decode(data)  # 解码接收到的数据
        if self.rec_msg.order_process_bar >= 95:
            self.mode_ok = self.rec_msg.mode  # 更新模式状态
        else:
            self.mode_ok = 0  # 重置模式状态

    def rec_responce(self):
        while self.runing:  # 运行状态
            self.lc_r.handle()  # 处理接收数据
            time.sleep(0.002)  # 延迟2毫秒

    def Wait_finish(self, mode, gait_id):
        count = 0
        while self.runing and count < 2000:  # 最多等待10秒
            if self.mode_ok == mode and self.gait_ok == gait_id:
                return True  # 命令完成
            else:
                time.sleep(0.005)  # 延迟5毫秒
                count += 1  # 增加计数

    def send_publish(self):
        while self.runing:
            self.send_lock.acquire()  # 获取锁
            if self.delay_cnt > 20:  # 心跳信号10HZ，用于在生命周期计数未更新时保持心跳
                self.lc_s.publish("robot_control_cmd", self.cmd_msg.encode())  # 发布命令
                self.delay_cnt = 0  # 重置延迟计数器
            self.delay_cnt += 1  # 增加延迟计数器
            self.send_lock.release()  # 释放锁
            time.sleep(0.005)  # 延迟5毫秒

    def Send_cmd(self, msg):
        self.send_lock.acquire()  # 获取锁
        self.delay_cnt = 50  # 设置延迟计数器
        self.cmd_msg = msg  # 设置命令消息
        self.send_lock.release()  # 释放锁

    def quit(self):
        self.runing = 0  # 停止运行
        self.rec_thread.join()  # 等待接收线程结束
        self.send_thread.join()  # 等待发送线程结束

# 主函数
if __name__ == '__main__':
    main()  # 运行主函数
