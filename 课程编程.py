# ======================================================
# 反应釜数据分析系统
# 姓名：杨浩
# 学号：2024211357
# ======================================================

# 导入必要的模块
import math  # 用于数学计算，如平方根
import copy  # 用于深拷贝数据，避免修改原数据
import matplotlib.pyplot as plt  # 用于绘制数据可视化图表

# ======================================================
# 原始数据：反应釜采样记录列表，每个记录包含时间、温度(T)、压力(P)、流量(F)、转化率(conv)、杂质(imp)
# ======================================================

records = [
    {"time": 0,   "T": 72,   "P": 1.05, "F": 9.8,  "conv": 0.10, "imp": 0.76},
    {"time": 10,  "T": 78,   "P": 1.12, "F": 10.1, "conv": 0.18, "imp": 0.70},
    {"time": 20,  "T": 86,   "P": 1.25, "F": 10.4, "conv": 0.31, "imp": 0.63},
    {"time": 30,  "T": 95,   "P": 1.38, "F": 10.8, "conv": 0.46, "imp": 0.58},
    {"time": 40,  "T": 108,  "P": 1.60, "F": 11.1, "conv": 0.60, "imp": 0.51},
    {"time": 50,  "T": 122,  "P": 1.88, "F": 11.3, "conv": 0.70, "imp": 0.49},
    {"time": 60,  "T": 118,  "P": 2.12, "F": 11.6, "conv": 0.77, "imp": 0.92},
    {"time": 70,  "T": 115,  "P": 1.90, "F": 10.9, "conv": 0.81, "imp": 0.46},
    {"time": 80,  "T": None, "P": 1.72, "F": 10.5, "conv": 0.84, "imp": 0.44},
    {"time": 90,  "T": 126,  "P": 1.55, "F": None, "conv": 0.85, "imp": 0.43},
    {"time": 100, "T": 119,  "P": None, "F": 9.9,  "conv": 0.86, "imp": 0.42},
    {"time": 110, "T": 114,  "P": 1.32, "F": 9.5,  "conv": 0.87, "imp": 0.41}
]


# ======================================================
# 任务一：检查缺失值
# ======================================================


def check_missing_values(records):
    """检查数据记录中的缺失值"""
    # 定义需要检查的变量列表
    variables = ["T", "P", "F", "conv", "imp"]

    print("\n========== 缺失值检查 ==========")

    # 提取所有时间点用于显示
    times = [record["time"] for record in records]
    print("所有采样时间点：")
    print(times)

    # 遍历每个变量进行检查
    for var in variables:
        valid_count = 0
        missing_count = 0
        missing_times = []

        for record in records:
            if record[var] is None:
                missing_count += 1
                missing_times.append(record["time"])
            else:
                valid_count += 1

        print(f"\n变量 {var}：")
        print(f"有效数据个数：{valid_count}")
        print(f"缺失值个数：{missing_count}")

        if missing_count > 0:
            print(f"缺失时间点：{missing_times}")


# ======================================================
# 任务二：缺失值填补
# ======================================================


def fill_missing(records, variable):
    """填补指定变量的缺失值，使用前后值的平均或最近值"""
    # 深拷贝原数据，避免修改
    new_records = copy.deepcopy(records)

    for i in range(len(new_records)):

        if new_records[i][variable] is None:

            prev_value = None
            next_value = None

            # 向前查找有效值
            for j in range(i - 1, -1, -1):
                if new_records[j][variable] is not None:
                    prev_value = new_records[j][variable]
                    prev_time = new_records[j]["time"]
                    break

            # 向后查找有效值
            for j in range(i + 1, len(new_records)):
                if new_records[j][variable] is not None:
                    next_value = new_records[j][variable]
                    next_time = new_records[j]["time"]
                    break

            # 如果前后都有值，取平均
            if prev_value is not None and next_value is not None:
                fill_value = (prev_value + next_value) / 2

                print(
                    f"{variable} 在 {new_records[i]['time']} min 处缺失，"
                    f"已用 {prev_time} min 和 {next_time} min 的平均值 {fill_value:.3f} 填补"
                )

            # 如果是开头缺失，用下一个值
            elif prev_value is None:
                fill_value = next_value
                print(
                    f"{variable} 在 {new_records[i]['time']} min 处缺失，"
                    f"已用最近有效值 {fill_value:.3f} 填补"
                )

            # 如果是结尾缺失，用上一个值
            elif next_value is None:
                fill_value = prev_value
                print(
                    f"{variable} 在 {new_records[i]['time']} min 处缺失，"
                    f"已用最近有效值 {fill_value:.3f} 填补"
                )

            new_records[i][variable] = fill_value

    return new_records


# ======================================================
# 任务三：安全状态判断
# ======================================================


def judge_status(record):
    """判断单条记录的安全状态"""
    T = record["T"]
    P = record["P"]
    F = record["F"]
    imp = record["imp"]

    # 检查是否有缺失值
    if T is None or P is None or F is None or imp is None:
        return "数据缺失，无法判断"

    abnormal = []

    # 检查温度是否在正常范围内
    if not (70 <= T <= 120):
        abnormal.append("温度")

    # 检查压力
    if not (1.0 <= P <= 2.0):
        abnormal.append("压力")

    # 检查流量
    if not (8.0 <= F <= 12.0):
        abnormal.append("流量")

    # 检查杂质
    if not (imp <= 0.80):
        abnormal.append("杂质")

    # 根据异常数量判断状态
    if len(abnormal) == 0:
        return "运行正常"
    elif len(abnormal) == 1:
        return abnormal[0] + "异常"
    else:
        return "多变量异常"



def show_all_status(records):
    """显示所有记录的安全状态"""
    print("\n========== 安全状态判断 ==========")

    for record in records:
        status = judge_status(record)
        print(f"time = {record['time']} min，状态：{status}")


# ======================================================
# 任务四：描述性统计分析
# ======================================================


def calculate_statistics(values):
    """计算数值列表的描述性统计指标"""
    # 过滤掉缺失值
    clean_values = []

    for value in values:
        if value is not None:
            clean_values.append(value)

    n = len(clean_values)

    # 计算平均值
    total = 0
    for value in clean_values:
        total += value

    mean = total / n

    # 排序用于中位数和极值
    sorted_values = sorted(clean_values)

    # 计算中位数
    if n % 2 == 1:
        median = sorted_values[n // 2]
    else:
        median = (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2

    # 最大最小值
    min_value = sorted_values[0]
    max_value = sorted_values[-1]

    # 极差
    range_value = max_value - min_value

    # 方差
    variance_sum = 0

    for value in clean_values:
        variance_sum += (value - mean) ** 2

    variance = variance_sum / n

    # 标准差
    std = math.sqrt(variance)

    return {
        "mean": round(mean, 3),
        "median": round(median, 3),
        "min": round(min_value, 3),
        "max": round(max_value, 3),
        "range": round(range_value, 3),
        "variance": round(variance, 3),
        "std": round(std, 3)
    }



def show_statistics(records):
    """显示所有变量的描述性统计结果"""
    variables = ["T", "P", "F", "conv", "imp"]

    print("\n========== 描述性统计 ==========")

    for var in variables:
        # 提取变量值列表
        values = []

        for record in records:
            values.append(record[var])

        stats = calculate_statistics(values)

        print(f"\n变量 {var}：")

        for key, value in stats.items():
            print(f"{key} = {value}")


# ======================================================
# 任务五：异常值检测（IQR）
# ======================================================


def get_median(data):
    """计算列表的中位数"""
    n = len(data)

    if n % 2 == 1:
        return data[n // 2]
    else:
        return (data[n // 2 - 1] + data[n // 2]) / 2



def detect_outliers_iqr(values):
    """使用IQR方法检测异常值"""
    # 过滤缺失值
    clean_values = []

    for value in values:
        if value is not None:
            clean_values.append(value)

    sorted_values = sorted(clean_values)

    n = len(sorted_values)

    # 分割为上下半部分计算Q1和Q3
    if n % 2 == 0:
        lower_half = sorted_values[:n // 2]
        upper_half = sorted_values[n // 2:]
    else:
        lower_half = sorted_values[:n // 2]
        upper_half = sorted_values[n // 2 + 1:]

    Q1 = get_median(lower_half)
    Q3 = get_median(upper_half)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = []

    for value in sorted_values:
        if value < lower_bound or value > upper_bound:
            outliers.append(value)

    return {
        "Q1": round(Q1, 3),
        "Q3": round(Q3, 3),
        "IQR": round(IQR, 3),
        "lower_bound": round(lower_bound, 3),
        "upper_bound": round(upper_bound, 3),
        "outliers": outliers
    }



def show_outliers(records):
    """显示异常值检测结果"""
    variables = ["T", "P", "F", "imp"]

    print("\n========== 异常值检测 ==========")

    for var in variables:
        # 提取变量值
        values = []

        for record in records:
            values.append(record[var])

        result = detect_outliers_iqr(values)

        print(f"\n变量 {var}：")
        print(f"Q1 = {result['Q1']}")
        print(f"Q3 = {result['Q3']}")
        print(f"IQR = {result['IQR']}")
        print(f"下限 = {result['lower_bound']}")
        print(f"上限 = {result['upper_bound']}")

        if len(result['outliers']) == 0:
            print("无异常值")
        else:
            print("异常值如下：")

            for outlier in result['outliers']:
                for record in records:
                    if record[var] == outlier:
                        print(
                            f"时间：{record['time']} min，"
                            f"异常值：{outlier}"
                        )


# ======================================================
# 任务六：相关性分析
# ======================================================


def pearson_corr(x, y):
    """计算两列表的皮尔逊相关系数"""
    # 过滤缺失值对
    clean_x = []
    clean_y = []

    for i in range(len(x)):
        if x[i] is not None and y[i] is not None:
            clean_x.append(x[i])
            clean_y.append(y[i])

    n = len(clean_x)

    mean_x = sum(clean_x) / n
    mean_y = sum(clean_y) / n

    numerator = 0
    sum_x = 0
    sum_y = 0

    for i in range(n):
        numerator += (clean_x[i] - mean_x) * (clean_y[i] - mean_y)
        sum_x += (clean_x[i] - mean_x) ** 2
        sum_y += (clean_y[i] - mean_y) ** 2

    denominator = math.sqrt(sum_x * sum_y)

    r = numerator / denominator

    return round(r, 3)



def correlation_level(r):
    """根据相关系数判断相关性强度"""
    if r >= 0.8:
        return "强正相关"
    elif 0.4 <= r < 0.8:
        return "中等正相关"
    elif -0.4 < r < 0.4:
        return "弱相关"
    elif -0.8 < r <= -0.4:
        return "中等负相关"
    else:
        return "强负相关"



def show_correlations(records):
    """显示变量间的相关性分析结果"""
    # 提取各变量列表
    T = [r["T"] for r in records]
    P = [r["P"] for r in records]
    F = [r["F"] for r in records]
    conv = [r["conv"] for r in records]
    imp = [r["imp"] for r in records]

    print("\n========== 相关性分析 ==========")

    # 定义要分析的变量对
    pairs = [
        ("T 与 conv", T, conv),
        ("T 与 P", T, P),
        ("conv 与 imp", conv, imp),
        ("F 与 conv", F, conv)
    ]

    for name, x, y in pairs:
        r = pearson_corr(x, y)

        print(f"\n{name}")
        print(f"相关系数 r = {r}")
        print(f"相关性判断：{correlation_level(r)}")


# ======================================================
# 任务七：报警等级设计
# ======================================================


def alarm_level(record):
    """根据记录判断报警等级"""
    T = record["T"]
    P = record["P"]
    F = record["F"]
    imp = record["imp"]

    if T is None or P is None or F is None or imp is None:
        return "数据缺失"

    severe_count = 0
    mild_count = 0

    # 检查温度报警
    if T < 60 or T > 130:
        severe_count += 1
    elif T < 70 or T > 120:
        mild_count += 1

    # 检查压力报警
    if P < 0.8 or P > 2.3:
        severe_count += 1
    elif P < 1.0 or P > 2.0:
        mild_count += 1

    # 检查流量报警
    if F < 7.0 or F > 13.0:
        severe_count += 1
    elif F < 8.0 or F > 12.0:
        mild_count += 1

    # 检查杂质报警
    if imp > 1.0:
        severe_count += 1
    elif imp > 0.80:
        mild_count += 1

    # 根据严重程度判断等级
    if severe_count >= 2:
        return "3级：危险"
    elif severe_count == 1:
        return "2级：警告"
    elif mild_count >= 1:
        return "1级：注意"
    else:
        return "0级：正常"



def show_alarm_statistics(records):
    """显示报警等级统计"""
    level_count = {
        "0级：正常": 0,
        "1级：注意": 0,
        "2级：警告": 0,
        "3级：危险": 0
    }

    print("\n========== 报警等级 ==========")

    for record in records:
        level = alarm_level(record)
        print(f"time = {record['time']} min，报警等级：{level}")

        if level in level_count:
            level_count[level] += 1

    print("\n报警等级统计：")

    for key, value in level_count.items():
        print(f"{key}：{value} 次")


# ======================================================
# 加分项：数据可视化
# ======================================================


def draw_charts(records):
    """绘制数据可视化图表"""
    import matplotlib
    matplotlib.use('Agg')  # 设置非GUI后端
    times = [r["time"] for r in records]

    T = [r["T"] for r in records]
    P = [r["P"] for r in records]
    conv = [r["conv"] for r in records]
    imp = [r["imp"] for r in records]

    # 绘制温度随时间变化图
    plt.figure(figsize=(8, 5))
    plt.plot(times, T, marker='o')
    plt.title("Temperature vs Time")
    plt.xlabel("Time(min)")
    plt.ylabel("Temperature(℃)")
    plt.grid(True)
    plt.savefig('temperature.png')  # 保存为文件
    plt.close()
    print("温度图已保存为 temperature.png")

    # 绘制压力随时间变化图
    plt.figure(figsize=(8, 5))
    plt.plot(times, P, marker='s')
    plt.title("Pressure vs Time")
    plt.xlabel("Time(min)")
    plt.ylabel("Pressure(MPa)")
    plt.grid(True)
    plt.savefig('pressure.png')  # 保存为文件
    plt.close()
    print("压力图已保存为 pressure.png")

    # 绘制转化率与温度散点图
    valid_T = []
    valid_conv = []

    for i in range(len(T)):
        if T[i] is not None:
            valid_T.append(T[i])
            valid_conv.append(conv[i])

    plt.figure(figsize=(8, 5))
    plt.scatter(valid_T, valid_conv)
    plt.title("Conversion vs Temperature")
    plt.xlabel("Temperature(℃)")
    plt.ylabel("Conversion")
    plt.grid(True)
    plt.savefig('conversion.png')  # 保存为文件
    plt.close()
    print("转化率图已保存为 conversion.png")

    # 绘制杂质随时间变化图
    plt.figure(figsize=(8, 5))
    plt.plot(times, imp, marker='^')
    plt.title("Impurity vs Time")
    plt.xlabel("Time(min)")
    plt.ylabel("Impurity")
    plt.grid(True)
    plt.savefig('impurity.png')  # 保存为文件
    plt.close()
    print("杂质图已保存为 impurity.png")


# ======================================================
# 查看原始数据
# ======================================================


def show_records(records):
    """显示所有原始数据记录"""
    print("\n========== 原始数据 ==========")

    for record in records:
        print(record)


# ======================================================
# 主菜单
# ======================================================


def main_menu():
    """主菜单函数，提供用户交互界面"""
    while True:
        print("\n========== 反应釜数据分析系统 ==========")
        print("1. 查看原始数据")
        print("2. 检查缺失值")
        print("3. 填补缺失值")
        print("4. 判断安全状态")
        print("5. 计算描述性统计指标")
        print("6. 检测异常值")
        print("7. 计算相关系数")
        print("8. 查看报警等级统计")
        print("9. 绘制可视化图形")
        print("0. 退出系统")

        choice = input("请输入功能编号：")

        if choice == "1":
            show_records(records)

        elif choice == "2":
            check_missing_values(records)

        elif choice == "3":
            print("\n========== 缺失值填补 ==========")

            filled_records = fill_missing(records, "T")
            filled_records = fill_missing(filled_records, "P")
            filled_records = fill_missing(filled_records, "F")

            print("\n填补完成后的数据：")

            for record in filled_records:
                print(record)

        elif choice == "4":
            show_all_status(records)

        elif choice == "5":
            show_statistics(records)

        elif choice == "6":
            show_outliers(records)

        elif choice == "7":
            show_correlations(records)

        elif choice == "8":
            show_alarm_statistics(records)

        elif choice == "9":
            draw_charts(records)

        elif choice == "0":
            print("系统已退出！")
            break

        else:
            print("输入有误，请重新输入！")


# ======================================================
# 程序入口
# ======================================================

main_menu()  # 启动主菜单
