"""
Python 技能树服务 —— 7 章 28 节点，每节点 3 或 5 道写死练习题
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

def _ex(title, desc, ex_in="无", ex_out=""):
    return {"title": title, "desc": desc, "ex_in": ex_in, "ex_out": ex_out}

S = [_ex] * 0  # placeholder shortcut

SKILL_TREE: List[Dict[str, Any]] = [
    # ========== 第1章：初生牛犊 ==========
    {"id":1,"name_cn":"初生牛犊","name_en":"Python 起步","nodes":[
        {"id":"variables","title":"变量与数据类型","icon":"type","gradient":"#2563eb,#60a5fa",
         "exercises":[
             _ex("变量赋值","创建三个变量：整数 a=10, 浮点数 b=3.14, 字符串 c=\"Hello\"。分别打印三个变量的值和类型（使用 type() 函数）。","无","10 <class 'int'>\n3.14 <class 'float'>\nHello <class 'str'>"),
             _ex("类型转换","创建字符串 s=\"123\"，转为整数后乘7打印。将整数456转字符串，拼接\"abc\"打印。","无","861\n456abc"),
             _ex("综合运算","用 input() 获取两个数字，分别转为 int 和 float，计算和、差、积、商并分行打印。","10 3.5","13.5\n6.5\n35.0\n2.857..."),
         ]},
        {"id":"operators","title":"运算符与表达式","icon":"settings","gradient":"#7c3aed,#a78bfa",
         "exercises":[
             _ex("算术运算符","给定 x=17, y=5，分别计算并打印 x+y, x-y, x*y, x/y, x//y, x%y, x**y，每行带说明。","无","加法:22\n减法:12\n乘法:85\n除法:3.4\n整除:3\n取余:2\n幂:1419857"),
             _ex("比较与逻辑","输入两个整数a,b。打印a>b, a==b, a>0 and b>0, a>10 or b>10 的结果。","15 8","True\nFalse\nTrue\nTrue"),
             _ex("优先级挑战","计算并打印：2+3*4, (2+3)*4, 10-2**3, 8/2**2, 5+3>7 and 4*2==8。最后用注释说明10-2**3的结果为何是2。","无","14\n20\n2\n2.0\nTrue"),
         ]},
        {"id":"io","title":"输入与输出","icon":"code","gradient":"#0891b2,#22d3ee",
         "exercises":[
             _ex("基本输入输出","用 input() 获取姓名和年龄，打印欢迎语，计算并打印出生年份（假设今年2026）。","张三 20","欢迎，张三！\n你大约出生于2006年"),
             _ex("f-string格式化","定义 name=\"Python\",version=3.13,year=2026。用 f-string 打印完整描述。再用 f-string 打印 pi=3.1415926 保留两位小数。","无","Python 3.13 发布于 2026 年\n圆周率约等于 3.14"),
             _ex("print高级用法","用end参数在一行打印1到5逗号分隔。用sep参数打印\"2026\"\"06\"\"21\"横线连接。用三引号打印一首唐诗。","无","1,2,3,4,5\n2026-06-21\n床前明月光..."),
             _ex("格式化对齐","打印购物清单表格：商品左对齐15字符，数量右对齐5，单价右对齐8（2位小数）。3行数据：苹果/3/5.5, 香蕉/5/2.8, 橙子/2/8.0。","无","商品            数量   单价\n苹果            3   5.50\n香蕉            5   2.80\n橙子            2   8.00"),
             _ex("交互计算器","编写交互式计算器：提示用户输入两个数字和一个运算符(+-*/)，根据运算符执行运算并打印结果。运算符非法则提示\"不支持的运算\"。","10 3 *","结果: 30"),
         ]},
        {"id":"strings","title":"字符串基础","icon":"text","gradient":"#059669,#34d399",
         "exercises":[
             _ex("字符串基本操作","创建 s=\"Hello Python World\"。打印长度、全部大写、空格替换为下划线、用切片取出\"Python\"并打印。","无","18\nHELLO PYTHON WORLD\nHello_Python_World\nPython"),
             _ex("字符串方法","创建 s=\"  Python is Fun!  \"。去除两端空格、统计字母'o'出现次数、判断是否以\"!\"结尾、查找\"Fun\"的位置并打印。","无","Python is Fun!\n1\nTrue\n12"),
             _ex("字符串遍历","用 for 循环遍历字符串 \"Python\"，打印每个字符及其ASCII码。再用 enumerate 打印每个字符的索引和值。","无","P:80\ny:121\n..."),
             _ex("字符串判断","输入一个字符串，判断：是否全是数字、是否全是字母、是否全是小写、是否以\"py\"开头（忽略大小写）。分别打印结果。","Python3","全是数字:False 全是字母:False 全是小写:False 以py开头:True"),
             _ex("凯撒密码","实现简易凯撒密码：输入一个字母字符串和偏移量n（1-25），每个字母向后偏移n位（z之后回到a），保留大小写。加密后打印。","abcXYZ 3","defABC"),
         ]},
    ]},
    # ========== 第2章：拨云见日 ==========
    {"id":2,"name_cn":"拨云见日","name_en":"控制流","nodes":[
        {"id":"conditionals","title":"条件判断","icon":"branch","gradient":"#2563eb,#60a5fa",
         "exercises":[
             _ex("成绩等级判定","输入0-100分数，输出等级：90-100=A,80-89=B,70-79=C,60-69=D,<60=F。用if-elif-else。非法输入提示错误。","85","等级: B"),
             _ex("闰年判断","输入一个年份，判断是否为闰年（能被4整除但不能被100整除，或能被400整除）。打印结果。","2024","2024年是闰年"),
             _ex("三角形判断","输入三条边长a,b,c，判断能否构成三角形（任意两边之和>第三边）。若能，判断是等边/等腰/普通三角形。","3 4 5","可以构成三角形: 普通三角形"),
         ]},
        {"id":"loops","title":"循环语句","icon":"refresh","gradient":"#f59e0b,#fbbf24",
         "exercises":[
             _ex("九九乘法表","用嵌套for循环打印九九乘法表（1x1=1到9x9=81），格式整齐，每行一个乘数。","无","1x1=1 1x2=2 ... 1x9=9\n...\n9x1=9 9x2=18 ... 9x9=81"),
             _ex("1到100求和","用while循环计算1到100所有整数之和并打印。再用for+range计算1到100所有偶数之和并打印。","无","5050\n2550"),
             _ex("质数判定","输入一个正整数n，判断n是否为质数（只能被1和自身整除）。用for循环从2试到sqrt(n)。优化：找到第一个因子后立刻break。","17","17是质数"),
         ]},
        {"id":"break_continue","title":"break / continue","icon":"skip","gradient":"#64748b,#94a3b8",
         "exercises":[
             _ex("猜数字游戏","预设 secret=42。用while循环让用户猜数：猜对break退出；猜负数continue跳过并提示；猜错提示\"太大/太小\"。","50 30 -1 42","太大了\n太小了\n请输入正数\n恭喜！猜对了，答案是42"),
             _ex("跳过3的倍数","用for循环打印1到30所有不能被3整除的数，用continue跳过能被3整除的数。","无","1 2 4 5 7 8 10 11 13 14 16 17 19 20 22 23 25 26 28 29"),
             _ex("第一个水仙花数","水仙花数：三位数每位数字的立方和等于自身（如153=1³+5³+3³）。用for+break找出100-999中第一个水仙花数并打印。","无","第一个水仙花数是: 153"),
             _ex("登录模拟","模拟登录：预设用户名\"admin\"密码\"123456\"。最多允许3次尝试，用while+break实现。每次提示剩余次数。登录成功/失败都打印相应信息。","admin wrong 123456","第1次: 用户名或密码错误，剩余2次\n第2次: 登录成功！"),
             _ex("筛选质数","用嵌套循环打印2到50之间的所有质数。内层循环用break优化：发现可被整除立即跳出。每行打印5个质数。","无","2 3 5 7 11\n13 17 19 23 29\n31 37 41 43 47"),
         ]},
    ]},
    # ========== 第3章：登堂入室 ==========
    {"id":3,"name_cn":"登堂入室","name_en":"函数","nodes":[
        {"id":"func_def","title":"函数定义与调用","icon":"edit","gradient":"#2563eb,#60a5fa",
         "exercises":[
             _ex("自定义计算函数","定义三个函数：calc_area(w,h)返回矩形面积；calc_circle(r)返回圆面积(π=3.14)；is_even(n)返回是否为偶数。分别调用并打印结果。","无","矩形面积:15\n圆面积:50.24\n7是偶数:False"),
             _ex("温度转换函数","定义c_to_f(c)将摄氏转华氏(F=C*9/5+32)；f_to_c(f)将华氏转摄氏(C=(F-32)*5/9)。调用两个函数分别转换25°C和98.6°F并打印。","无","25°C = 77.0°F\n98.6°F = 37.0°C"),
             _ex("计算器函数","定义函数calculator(a,b,op)：根据op的值(+-*/)返回计算结果，非法运算符返回None。主程序输入两个数和运算符，调用calculator并打印结果。","10 5 +","10 + 5 = 15"),
         ]},
        {"id":"params_return","title":"参数与返回值","icon":"link","gradient":"#7c3aed,#a78bfa",
         "exercises":[
             _ex("多参数与多返回值","定义stats(*args)接收任意个数，返回(总和,平均值,最大值,最小值)元组。调用stats(1,2,3,4,5)并用元组解包打印四个结果。","无","总和:15 平均:3.0 最大:5 最小:1"),
             _ex("默认参数","定义greet(name,greeting=\"你好\")。调用greet(\"张三\")和greet(\"李四\",\"早上好\")各一次并打印。","无","你好，张三\n早上好，李四"),
             _ex("关键字参数","定义函数describe_pet(name,species,age)。分别用位置参数和关键字参数两种方式调用，打印宠物描述。","无","Buddy是一只3岁的狗\nMimi是一只2岁的猫"),
         ]},
        {"id":"scope","title":"作用域与闭包","icon":"eye","gradient":"#0891b2,#22d3ee",
         "exercises":[
             _ex("全局变量","定义全局变量total=100。定义add_to_total(n)用global声明后加n。调用两次add_to_total(50)，每次打印total。","无","total=150\ntotal=200"),
             _ex("嵌套函数","定义outer(x)内部定义inner(y)返回x+y。调用outer(10)(5)并打印结果。解释为什么要用闭包。","无","15"),
             _ex("nonlocal练习","定义outer2()：内部有count=0和inner2()，inner用nonlocal count使其+1并打印。调用三次inner2()观察count变化。","无","count=1\ncount=2\ncount=3"),
         ]},
        {"id":"recursion","title":"递归函数","icon":"clock","gradient":"#059669,#34d399",
         "exercises":[
             _ex("阶乘","定义递归函数factorial(n)。打印factorial(5)和factorial(10)的结果。思考为什么递归比循环慢。","无","120\n3628800"),
             _ex("斐波那契","定义fib(n)返回第n个斐波那契数(fib(1)=1,fib(2)=1)。打印fib(1)到fib(15)的数列。用注释解释直接递归为何效率低。","无","1 1 2 3 5 8 13 21 34 55 89 144 233 377 610"),
             _ex("汉诺塔","用递归实现汉诺塔问题：定义hanoi(n,src,aux,dst)打印移动步骤。调用hanoi(3,'A','B','C')打印将3个盘子从A移到C的步骤。","无","A->C\nA->B\nC->B\nA->C\nB->A\nB->C\nA->C"),
         ]},
    ]},
    # ========== 第4章：胸有成竹 ==========
    {"id":4,"name_cn":"胸有成竹","name_en":"数据结构","nodes":[
        {"id":"list_tuple","title":"列表与元组","icon":"list","gradient":"#2563eb,#60a5fa",
         "exercises":[
             _ex("列表基本操作","创建nums=[3,1,4,1,5,9,2,6]。排序打印、末尾加0开头插7打印、删所有1打印、切片取前三和后三打印。","无","排序后:[1,1,2,3,4,5,6,9]\n[7,3,4,5,9,2,6,0]\n...\n前3:[7,3,4] 后3:[2,6,0]"),
             _ex("列表去重","输入一串数字（空格分隔），转为列表后去重（保留顺序），排序并打印。提示：用循环+not in判断，不用set。","4 2 1 2 4 3","去重后: [1,2,3,4]"),
             _ex("元组不可变","创建元组t=(1,2,3)。尝试t[0]=9并用try-except捕获TypeError，打印\"元组不可修改\"。再展示元组解包a,b,c=t。","无","元组不可修改\na=1 b=2 c=3"),
         ]},
        {"id":"dict_set","title":"字典与集合","icon":"grid","gradient":"#7c3aed,#a78bfa",
         "exercises":[
             _ex("学生成绩管理","创建字典scores={\"张三\":85,\"李四\":92,\"王五\":78,\"赵六\":95}。遍历打印、添加\"孙七\"=88、计算平均分、找出最高分学生。","无","张三:85 ...\n平均:87.6\n最高分:赵六(95)"),
             _ex("词频统计","输入一句话，用字典统计每个单词出现的次数（忽略大小写，去掉标点）。按出现次数降序打印。","hello world hello python","hello:2\nworld:1\npython:1"),
             _ex("集合运算","创建两个集合s1={1,2,3,4,5}, s2={4,5,6,7,8}。打印交集、并集、差集(s1-s2)、对称差集。","无","交集:{4,5}\n并集:{1-8}\n差集:{1,2,3}\n对称差:{1,2,3,6,7,8}"),
         ]},
        {"id":"comprehension","title":"列表推导式","icon":"zap","gradient":"#f59e0b,#fbbf24",
         "exercises":[
             _ex("推导式基础","用列表推导式生成：1-20偶数平方、从['apple','banana','cherry','date']筛选len>=5的单词转大写、1-5的立方字典。分别打印。","无","[4,16,36,...]\n['APPLE','BANANA','CHERRY']\n{1:1,2:8,3:27,4:64,5:125}"),
             _ex("过滤推导式","用列表推导式从1到100中筛选能被3或5整除但不能被15整除的数。计算个数并打印前10个。","无","个数:... 前10:[3,5,6,9,10,12,18,20,21,24]"),
             _ex("嵌套推导式","用嵌套列表推导式生成一个5x5的乘法表（二维列表）。外层for i(1-5)内层for j(1-5)，每个元素为i*j。格式化打印为矩阵。","无","1 2 3 4 5\n2 4 6 8 10\n3 6 9 12 15\n4 8 12 16 20\n5 10 15 20 25"),
         ]},
        {"id":"sort_algo","title":"排序与常用算法","icon":"bar-chart","gradient":"#0891b2,#22d3ee",
         "exercises":[
             _ex("冒泡排序","实现bubble_sort(arr)升序排序，每轮打印过程。测试[64,34,25,12,22,11,90]，打印排序前后。不能使用sorted()。","无","第1轮:[34,25,12,22,11,64,90]\n...\n排序后:[11,12,22,25,34,64,90]"),
             _ex("二分查找","实现binary_search(arr,target)返回目标索引（未找到返回-1）。在已排序列表[11,12,22,25,34,64,90]中查找25和100并打印结果。","无","查找25: 索引3\n查找100: -1（未找到）"),
             _ex("选择排序","实现selection_sort(arr)。与冒泡排序不同：每次从未排序部分选最小的放到已排序末尾。测试同一数组，打印每轮结果。","无","第1轮:[11,34,25,12,22,64,90]\n...\n排序后:[11,12,22,25,34,64,90]"),
         ]},
    ]},
    # ========== 第5章：运斤成风 ==========
    {"id":5,"name_cn":"运斤成风","name_en":"面向对象","nodes":[
        {"id":"class_instance","title":"类与实例","icon":"box","gradient":"#2563eb,#60a5fa",
         "exercises":[
             _ex("宠物类设计","设计Pet类：__init__(self,name,species,age)；describe()返回\"{name}是一只{age}岁的{species}\"；celebrate_birthday()让age+1。创建dog和cat实例测试全部方法。","无","Buddy是一只3岁的狗\nBuddy过生日了！现在4岁"),
             _ex("银行账户类","设计BankAccount类：__init__(self,owner,balance=0)；deposit(amount)；withdraw(amount)余额不足时提示；__str__返回账户信息。创建实例测试存取操作。","无","张三的账户余额: 1000\n存入500, 余额: 1500\n取款300, 余额: 1200"),
             _ex("学生类","设计Student类：属性name, scores(列表)；add_score(score)添加成绩；average()返回平均分；best()返回最高分。创建实例添加3次成绩后打印统计。","无","平均分: 85.0\n最高分: 92"),
         ]},
        {"id":"inheritance","title":"继承与多态","icon":"git-branch","gradient":"#7c3aed,#a78bfa",
         "exercises":[
             _ex("动物继承","设计基类Animal(name)，方法make_sound()返回\"...\"。子类Dog重写返回\"汪汪\"，Cat返回\"喵喵\"。定义animal_sound(animal)调用sound。创建实例演示多态。","无","汪汪\n喵喵"),
             _ex("图形继承","设计基类Shape，方法area()返回0。子类Rectangle(w,h)重写area()；Circle(r)重写area()(π=3.14)。创建矩形和圆形实例打印面积。","无","矩形面积: 15\n圆的面积: 50.24"),
             _ex("员工继承","设计基类Employee(name,salary)。子类Manager多一个bonus属性，重写get_total()返回salary+bonus。子类Intern固定salary=3000。创建实例打印总薪资。","无","张经理总薪资: 18000\n李实习生总薪资: 3000"),
         ]},
        {"id":"magic_methods","title":"魔术方法","icon":"sparkle","gradient":"#f59e0b,#fbbf24",
         "exercises":[
             _ex("向量类","设计Vector2D类：__init__(x,y)；__add__支持向量加法；__str__返回\"Vector2D(x,y)\"；__eq__判断相等。创建v1=(1,2),v2=(3,4)，打印v1+v2和v1==v2。","无","Vector2D(4,6)\nFalse"),
             _ex("分数类","设计Fraction类：__init__(num,den)；__str__返回\"num/den\"；__mul__支持分数相乘（分子乘分子、分母乘分母）。创建f1=(1,2),f2=(3,4)打印乘积。","无","1/2 * 3/4 = 3/8"),
             _ex("可比较学生类","设计Student2类：__init__(name,score)；__lt__按成绩比较；__eq__成绩相等。创建三个实例用sorted()排序并打印。","无","王五(78) < 张三(85) < 李四(92)"),
         ]},
        {"id":"property_decorator","title":"属性装饰器","icon":"at-sign","gradient":"#0891b2,#22d3ee",
         "exercises":[
             _ex("温度类","设计Temperature类：@property celsius；@property fahrenheit自动计算(F=C*9/5+32)；@celsius.setter限制>= -273.15。创建实例测试读、写、非法值。","无","25°C = 77.0°F\n错误:温度不能低于绝对零度(-273.15°C)"),
             _ex("圆形类","设计Circle类：@property radius；@property diameter(自动=radius*2)；@property area(自动=π*r²)；@radius.setter限制>0。创建r=5的圆打印直径和面积。","无","半径:5 直径:10 面积:78.5"),
             _ex("只读属性","设计Person类：__init__(name,birth_year)；@property age自动计算年龄(2026-birth_year)，没有setter（只读）。尝试修改age并捕获异常。","无","张三年龄:26\n无法修改年龄(只读属性)"),
         ]},
    ]},
    # ========== 第6章：融会贯通 ==========
    {"id":6,"name_cn":"融会贯通","name_en":"模块与异常","nodes":[
        {"id":"modules","title":"模块导入与包","icon":"package","gradient":"#2563eb,#60a5fa",
         "exercises":[
             _ex("标准库导入","导入math模块：打印sqrt(16),pi,sin(pi/2)。导入random：生成5个1-100随机整数。导入datetime：打印当前日期时间。","无","4.0 3.14159... 1.0\n[42,17,93,8,65]\n2026-06-21 xx:xx:xx"),
             _ex("os模块","导入os模块：打印当前工作目录、操作系统名称、列出当前目录下所有.py文件。使用os.path检查某个文件是否存在。","无","当前目录: D:\\...\n系统: nt\n.py文件: [...]"),
             _ex("自定义模块","（模拟）在自己的代码中创建一个简单的my_math.py文件，定义add(a,b)和multiply(a,b)函数。然后在主程序from my_math import add, multiply并调用。","无","add(3,5)=8\nmultiply(3,5)=15"),
         ]},
        {"id":"file_io","title":"文件读写","icon":"file","gradient":"#7c3aed,#a78bfa",
         "exercises":[
             _ex("基本文件读写","用with语句创建test.txt，写入三行内容。关闭后重新打开读取全部内容并打印。用readlines()逐行打印带行号的内容。","无","第1行:Hello\n第2行:Python\n第3行:文件操作"),
             _ex("日志追加","创建log.txt（用'a'追加模式），写入三条带时间戳的日志（用datetime.now()）。然后读取并打印全部日志。","无","[2026-06-21 10:00:00] 程序启动\n[10:00:01] 执行任务\n[10:00:02] 任务完成"),
             _ex("CSV处理","创建一个data.csv文件，写入表头\"姓名,年龄,成绩\"和三行数据。用csv模块或手动split读取，计算平均年龄和平均成绩并打印。","无","平均年龄:21.3\n平均成绩:85.0"),
         ]},
        {"id":"exceptions","title":"异常处理","icon":"alert","gradient":"#f59e0b,#fbbf24",
         "exercises":[
             _ex("安全除法","用try-except实现安全除法：捕获ValueError(非数字)、ZeroDivisionError(除数0)、用finally打印\"计算结束\"。输入q退出循环。","10 0","除数不能为零！\n计算结束\n程序退出"),
             _ex("文件异常","尝试用open()打开一个不存在的文件，捕获FileNotFoundError并打印友好提示，然后创建该文件并写入默认内容。","无","文件不存在，已自动创建默认文件"),
             _ex("自定义异常","定义InvalidAgeError(Exception)。编写函数check_age(age)，若age<0或>150抛出InvalidAgeError。测试正常值和非法值。","25","年龄有效:25\n错误:年龄0无效(必须>0)"),
         ]},
    ]},
    # ========== 第7章：大展身手 ==========
    {"id":7,"name_cn":"大展身手","name_en":"综合实战","nodes":[
        {"id":"cli_project","title":"命令行工具项目","icon":"terminal","gradient":"#2563eb,#60a5fa",
         "exercises":[
             _ex("待办事项管理器","编写命令行待办管理器：列表存{id,title,done}字典。while循环菜单：1添加2查看3标记完成4删除5退出。添加自增id，查看显示序号标题状态(✅/⬜)。","1 学习Python","已添加:[1]学习Python\n[1]学习Python ✅\n再见！"),
             _ex("通讯录管理系统","编写通讯录程序：字典存{name:phone}。菜单：1添加2查找3删除4显示全部5退出。查找支持部分匹配（如输入\"张\"显示所有姓张的）。","1 张三 13800138000","已添加:张三\n查找\"张\": 张三 13800138000"),
             _ex("简易计算器","编写命令行计算器：支持连续运算。输入格式\"数字 运算符 数字\"如\"10 + 5\"。支持+-*/和history命令查看历史记录。输入q退出。","10 + 5 * 3","15\n45"),
         ]},
        {"id":"data_project","title":"数据处理脚本","icon":"database","gradient":"#7c3aed,#a78bfa",
         "exercises":[
             _ex("学生成绩分析","给定列表[{\"name\":\"A\",\"math\":85,\"eng\":90},{\"name\":\"B\",\"math\":72,\"eng\":88},{\"name\":\"C\",\"math\":95,\"eng\":76}]。计算每人总分平均分、按总分排序、全班各科平均分、最高分学生。","无","排名:1.C(171) 2.A(175) 3.B(160)\n数学平均:84.0 英语:84.67\n最高分:A"),
             _ex("文本统计","读取一段文本（英文），统计：总字符数、单词数、句子数（以.?!分割）、最高频单词及其次数。忽略大小写。","Hello world. Hello Python!","总字符:26 单词数:4 句子数:2\n最高频词:hello(2次)"),
             _ex("数据可视化模拟","不用第三方库，用print模拟柱状图。给定数据{\"Python\":85,\"Java\":70,\"JS\":65,\"C++\":50}，打印横向柱状图（每个=代表5分）。","无","Python | ================ 85\nJava   | ============== 70\nJS     | ============= 65\nC++    | ========== 50"),
         ]},
    ]},
]

SKILL_TREE_RAW = SKILL_TREE  # 保留引用用于测试


class SkillTreeService:
    def __init__(self, db, llm_service=None):
        self.db = db
        self.llm_service = llm_service

    # ---- 主视图 ----

    def build_tree_response(self, student_id: str) -> dict:
        raw = self.db.get_skill_tree_progress(student_id)
        progress = self.calc_chapter_progress(raw)
        chapters = []
        for ch in SKILL_TREE:
            cp = progress.get(ch["id"], 0.0)
            unlocked = self.is_chapter_unlocked(ch["id"], progress)
            chapters.append({
                "id": ch["id"], "name_cn": ch["name_cn"], "name_en": ch["name_en"],
                "progress": round(cp, 1), "unlocked": unlocked,
                "node_count": len(ch["nodes"]),
                "nodes": [self._format_node(n, ch["id"], raw) for n in ch["nodes"]],
            })
        return {"chapters": chapters, "progress": progress}

    def calc_chapter_progress(self, raw_progress: dict) -> Dict[int, float]:
        result = {}
        for ch in SKILL_TREE:
            cid = ch["id"]
            total = 0
            earned = 0
            for node in ch["nodes"]:
                if "exercises" in node:
                    total += len(node["exercises"])
                    for ei in range(len(node["exercises"])):
                        key = f"{cid}-{node['id']}-{ei}"
                        p = raw_progress.get(key, {})
                        if p.get("l3_status") == "completed":
                            earned += 1
            result[cid] = round(earned / max(total, 1) * 100, 1)
        return result

    def is_chapter_unlocked(self, chapter_id: int, progress: dict) -> bool:
        if chapter_id == 1:
            return True
        return progress.get(chapter_id - 1, 0) >= 70.0

    # ---- 章节详情 ----

    def get_chapter_detail(self, student_id: str, chapter_id: int) -> dict:
        raw = self.db.get_skill_tree_progress(student_id)
        progress = self.calc_chapter_progress(raw)
        ch = self._find_chapter(chapter_id)
        if not ch:
            raise ValueError(f"章节不存在: {chapter_id}")
        unlocked = self.is_chapter_unlocked(chapter_id, progress)
        nodes = [self._format_node(n, chapter_id, raw) for n in ch["nodes"]]
        return {
            "id": ch["id"], "name_cn": ch["name_cn"], "name_en": ch["name_en"],
            "progress": round(progress.get(chapter_id, 0.0), 1),
            "unlocked": unlocked, "node_count": len(nodes),
            "nodes": nodes,
        }

    def _format_node(self, node: dict, chapter_id: int, raw_progress: dict) -> dict:
        exercises = node.get("exercises", [])
        total_ex = len(exercises)
        done_count = 0
        ex_statuses = []
        for ei in range(total_ex):
            key = f"{chapter_id}-{node['id']}-{ei}"
            p = raw_progress.get(key, {})
            status = p.get("l3_status", "locked")
            score = p.get("l3_score", 0)
            if status == "completed":
                done_count += 1
            ex_statuses.append({"index": ei, "status": status, "score": score})
        done = total_ex > 0 and done_count == total_ex
        return {
            "id": node["id"], "title": node["title"],
            "icon": node.get("icon", "book"),
            "gradient": node.get("gradient", "#64748b,#94a3b8"),
            "done": done,
            "progress_pct": round(done_count / max(total_ex, 1) * 100),
            "status": "completed" if done else ("in_progress" if done_count > 0 else "locked"),
            "exercise_count": total_ex,
            "done_count": done_count,
            "exercises": ex_statuses,
        }

    # ---- 练习 ----

    def generate_exercise(self, student_id: str, chapter_id: int, node_id: str,
                          level: str, exercise_index: int = 0) -> dict:
        node = self._find_node(chapter_id, node_id)
        if not node:
            raise ValueError(f"节点不存在: {chapter_id}/{node_id}")
        exs = node.get("exercises", [])
        if exercise_index >= len(exs):
            raise ValueError(f"题目索引无效: {exercise_index}")
        ex = exs[exercise_index]
        key = f"{chapter_id}-{node_id}-{exercise_index}"
        self.db.save_skill_tree_progress(student_id, chapter_id, node_id, "l3", "in_progress")
        # 存储 exercise_index 到 l3_score 以便后续区分
        conn = __import__("sqlite3").connect(str(__import__("settings").DB_PATH))
        conn.execute("UPDATE skill_tree_progress SET l3_score=? WHERE student_id=? AND chapter_id=? AND node_id=?",
                     (exercise_index, student_id, chapter_id, node_id))
        conn.commit()
        conn.close()
        return {"chapter_id": chapter_id, "node_id": node_id, "level": "l3",
                "exercise_index": exercise_index, "total_exercises": len(exs),
                "exercise": {"title": ex["title"], "description": ex["desc"],
                             "example_input": ex.get("ex_in", ""),
                             "example_output": ex.get("ex_out", "")}}

    def submit_answer(self, student_id: str, chapter_id: int, node_id: str, level: str,
                      user_answer: str, exercise_data: dict, exercise_index: int = 0) -> dict:
        if not self.llm_service:
            raise RuntimeError("LLM 服务未配置")
        node = self._find_node(chapter_id, node_id)
        if not node:
            raise ValueError(f"节点不存在: {chapter_id}/{node_id}")
        prompt = f"""你是 Python 编程教学专家，负责评判学生代码。

知识点：{node['title']}
题目：{exercise_data}

学生提交的代码：
```python
{user_answer}
```

请判断代码是否正确实现了题目要求。返回 JSON：{{"correct": true/false, "score": 1-5, "feedback": "详细评语"}}"""
        result = self.llm_service.chat_json(
            system_prompt="你是严格的 Python 编程评判专家。只返回 JSON。",
            user_message=prompt,
        )
        if isinstance(result, dict) and result.get("correct"):
            self.db.save_skill_tree_progress(student_id, chapter_id, node_id, "l3",
                                              "completed", score=result.get("score", 5))
        return {"correct": result.get("correct", False) if isinstance(result, dict) else False,
                "score": result.get("score", 0) if isinstance(result, dict) else 0,
                "feedback": result.get("feedback", "") if isinstance(result, dict) else str(result)}

    # ---- 工具 ----

    def _find_chapter(self, chapter_id: int) -> dict | None:
        for ch in SKILL_TREE:
            if ch["id"] == chapter_id:
                return ch
        return None

    def _find_node(self, chapter_id: int, node_id: str) -> dict | None:
        ch = self._find_chapter(chapter_id)
        if not ch: return None
        for n in ch["nodes"]:
            if n["id"] == node_id: return n
        return None
