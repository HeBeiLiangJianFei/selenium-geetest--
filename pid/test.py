#  PID控制一阶惯性系统测试程序

# *****************************************************************#
#                      增量式PID系统                              #
# *****************************************************************#
class IncrementalPID:
    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.PIDOutput = 0.0  # PID控制器输出
        self.SystemOutput = 0.0  # 系统输出值
        self.LastSystemOutput = 0.0  # 上次系统输出值

        self.Error = 0.0  # 输出值与输入值的偏差
        self.LastError = 0.0
        self.LastLastError = 0.0

    # 设置PID控制器参数
    def SetStepSignal(self, StepSignal):
        self.Error = StepSignal - self.SystemOutput
        IncrementValue = self.Kp * (self.Error - self.LastError) + self.Ki * self.Error + self.Kd * (
                    self.Error - 2 * self.LastError + self.LastLastError)
        self.PIDOutput += IncrementValue
        self.LastLastError = self.LastError
        self.LastError = self.Error

    # 设置一阶惯性环节系统  其中InertiaTime为惯性时间常数
    def SetInertiaTime(self, InertiaTime, SampleTime):
        self.SystemOutput = (InertiaTime * self.LastSystemOutput + SampleTime * self.PIDOutput) / (
                    SampleTime + InertiaTime)
        self.LastSystemOutput = self.SystemOutput


# *****************************************************************#
#                      位置式PID系统                              #
# *****************************************************************#
class PositionalPID:
    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.SystemOutput = 0.0
        self.ResultValueBack = 0.0
        self.PidOutput = 0.0
        self.PIDErrADD = 0.0
        self.ErrBack = 0.0

    def SetInertiaTime(self, InertiaTime, SampleTime):
        self.SystemOutput = (InertiaTime * self.ResultValueBack + SampleTime * self.PidOutput) / (
                    SampleTime + InertiaTime)
        self.ResultValueBack = self.SystemOutput

    def SetStepSignal(self, StepSignal):
        Err = StepSignal - self.SystemOutput
        KpWork = self.Kp * Err
        KiWork = self.Ki * self.PIDErrADD
        KdWork = self.Kd * (Err - self.ErrBack)
        self.PidOutput = KpWork + KiWork + KdWork
        # print(Err)
        self.PIDErrADD += Err
        self.ErrBack = Err





import matplotlib.pyplot as plt

plt.figure(1)  # 创建图表1
plt.figure(2)  # 创建图表2


# 测试PID程序
def TestPID(P, I, D, li):
    IncrementalPid = IncrementalPID(P, I, D)
    PositionalPid = PositionalPID(P, I, D)
    IncrementalXaxis = [0]
    IncrementalYaxis = [0]
    PositionalXaxis = [0]
    PositionalYaxis = [0]

    for i in range(1, 500):
        # 增量式
        IncrementalPid.SetStepSignal(li)
        IncrementalPid.SetInertiaTime(3, 0.1)
        IncrementalYaxis.append(IncrementalPid.SystemOutput)
        IncrementalXaxis.append(i)

        # 位置式
        # PositionalPid.SetStepSignal(100.2)
        # PositionalPid.SetInertiaTime(3, 0.1)
        # PositionalYaxis.append(PositionalPid.SystemOutput)
        # PositionalXaxis.append(i)
    # print(PositionalYaxis)
    l = []
    print("长度",len(PositionalYaxis))
    def f(lis):
        for i in range(len(lis) - 1):
            l.append(round(lis[i + 1] - lis[i]))
        print(l)
        return l
    f(PositionalYaxis)


    # # print(IncrementalYaxis)
    plt.figure(1)  # 选择图表1
    plt.plot(IncrementalXaxis, IncrementalYaxis, 'r')
    plt.xlim(0, 120)
    plt.ylim(0, 140)
    plt.title("IncrementalPID")
    #
    # plt.figure(2)  # 选择图表2
    # plt.plot(PositionalXaxis, PositionalYaxis, 'b')
    # plt.xlim(0, 120)
    # plt.ylim(0, 140)
    # plt.title("PositionalPID")

    plt.show()


if __name__ == "__main__":
    TestPID(4.5, 0.5, 0.1,88)



