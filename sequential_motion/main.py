'''
该演示展示了基于Lcm的MR813运动控制板的通信接口
- robot_control_cmd_lcmt.py
- cyberdog2_ctrl.toml
'''
import lcm
import toml
import sys
import os
import time

from robot_control_cmd_lcmt import robot_control_cmd_lcmt

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f

def main():
    base = './'
    num = 0
    filelist = []
    for i in findAllFile(base):
        filelist.append(i)
        print(f"{num},{filelist[num]}")
        num += 1
    print('输入一个TOML控制文件编号:')
    numInput = int(input())

    lc = lcm.LCM("udpm://239.255.76.67:7671?ttl=255")
    msg = robot_control_cmd_lcmt()
    file = os.path.join(base, filelist[numInput])
    print(f"加载文件={file}\n")
    try:
        steps = toml.load(file)
        for step in steps['step']:
            msg.mode = step['mode']
            msg.value = step['value']
            msg.contact = step['contact']
            msg.gait_id = step['gait_id']
            msg.duration = step['duration']
            msg.life_count += 1
            for i in range(3):
                msg.vel_des[i] = step['vel_des'][i]
                msg.rpy_des[i] = step['rpy_des'][i]
                msg.pos_des[i] = step['pos_des'][i]
                msg.acc_des[i] = step['acc_des'][i]
                msg.acc_des[i + 3] = step['acc_des'][i + 3]
                msg.foot_pose[i] = step['foot_pose'][i]
                msg.ctrl_point[i] = step['ctrl_point'][i]
            for i in range(2):
                msg.step_height[i] = step['step_height'][i]

            lc.publish("robot_control_cmd", msg.encode())
            print(f'robot_control_cmd LCM发布模式: {msg.mode} 步态ID: {msg.gait_id} 持续时间: {msg.duration}')
            time.sleep(0.1)
        for _ in range(300):  # 60秒心跳，用于保持心跳以防止life count未更新
            lc.publish("robot_control_cmd", msg.encode())
            time.sleep(0.2)
    except KeyboardInterrupt:
        msg.mode = 7  # 纯阻尼模式
        msg.gait_id = 0
        msg.duration = 0
        msg.life_count += 1
        lc.publish("robot_control_cmd", msg.encode())
        pass
    sys.exit()

if __name__ == '__main__':
    main()
