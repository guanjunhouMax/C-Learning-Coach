# C语言学习小教练 - 本地知识库

import re

KNOWLEDGE_BASE = {
    "基础语法": {
        "keywords": ["printf", "scanf", "变量", "数据类型", "int", "char", "float", "double", "const", "sizeof", "输出", "输入", "注释"],
        "content": "## C语言基础语法\n\n### Hello World\n```c\n#include <stdio.h>\n\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}\n```\n\n### 基本数据类型\n| 类型 | 大小 | 范围 |\n|------|------|------|\n| char | 1字节 | -128 ~ 127 |\n| int | 4字节 | -2^31 ~ 2^31-1 |\n| float | 4字节 | 约6位精度 |\n| double | 8字节 | 约15位精度 |\n\n### 变量声明与赋值\n```c\nint age = 18;\nfloat pi = 3.14;\nchar grade = \"A\";\nconst int MAX = 100;  // 常量\n```\n\n### 输入输出\n```c\nint num;\nprintf(\"请输入一个数字: \");\nscanf(\"%d\", &num);\nprintf(\"你输入的是: %d\\n\", num);\n```\n\n### 格式化占位符\n- `%d` - 整数\n- `%f` - 浮点数\n- `%c` - 字符\n- `%s` - 字符串\n- `%p` - 指针\n- `%x` - 十六进制"
    },
    "控制流": {
        "keywords": ["if", "else", "switch", "case", "for", "while", "do", "循环", "条件", "判断", "break", "continue", "goto"],
        "content": "## C语言控制流\n\n### if-else 条件判断\n```c\nint score = 85;\nif (score >= 90) {\n    printf(\"优秀\");\n} else if (score >= 80) {\n    printf(\"良好\");\n} else if (score >= 60) {\n    printf(\"及格\");\n} else {\n    printf(\"不及格\");\n}\n```\n\n### switch 语句\n```c\nint option = 2;\nswitch (option) {\n    case 1:\n        printf(\"选项1\");\n        break;\n    case 2:\n        printf(\"选项2\");\n        break;\n    default:\n        printf(\"其他\");\n        break;\n}\n```\n\n### for 循环\n```c\nfor (int i = 0; i < 5; i++) {\n    printf(\"%d \", i);  // 0 1 2 3 4\n}\n```\n\n### while 循环\n```c\nint count = 0;\nwhile (count < 5) {\n    printf(\"%d \", count);\n    count++;\n}\n```\n\n### do-while 循环\n```c\nint i = 0;\ndo {\n    printf(\"%d \", i);\n    i++;\n} while (i < 5);\n```\n\n### break 和 continue\n```c\nfor (int i = 0; i < 10; i++) {\n    if (i == 3) continue;  // 跳过3\n    if (i == 7) break;     // 到7停止\n    printf(\"%d \", i);\n}\n// 输出: 0 1 2 4 5 6\n```"
    },
    "数组": {
        "keywords": ["数组", "array", "二维数组", "下标", "索引", "遍历"],
        "content": "## C语言数组\n\n### 一维数组\n```c\n// 声明和初始化\nint nums[5] = {1, 2, 3, 4, 5};\nint arr[] = {10, 20, 30};  // 自动推断大小\n\n// 访问和修改\nnums[0] = 100;  // 修改第一个元素\nprintf(\"%d\", nums[2]);  // 访问第三个元素\n\n// 遍历数组\nfor (int i = 0; i < 5; i++) {\n    printf(\"%d \", nums[i]);\n}\n```\n\n### 二维数组\n```c\nint matrix[2][3] = {\n    {1, 2, 3},\n    {4, 5, 6}\n};\n\n// 遍历\nfor (int i = 0; i < 2; i++) {\n    for (int j = 0; j < 3; j++) {\n        printf(\"%d \", matrix[i][j]);\n    }\n    printf(\"\\n\");\n}\n```\n\n### 数组作为函数参数\n```c\n// 数组传参时会退化为指针\nvoid printArray(int arr[], int size) {\n    for (int i = 0; i < size; i++) {\n        printf(\"%d \", arr[i]);\n    }\n}\n// 调用: printArray(nums, 5);\n```"
    },
    "指针": {
        "keywords": ["指针", "pointer", "*", "&", "NULL", "地址", "引用", "解引用", "野指针", "空指针", "malloc", "free"],
        "content": "## C语言指针\n\n### 指针基础\n```c\nint a = 10;\nint *p = &a;  // p 存放 a 的地址\n\nprintf(\"a的值: %d\\n\", a);      // 10\nprintf(\"a的地址: %p\\n\", &a);   // 地址\nprintf(\"p的值: %p\\n\", p);       // 同 &a\nprintf(\"p指向的值: %d\\n\", *p);  // 10（解引用）\n```\n\n### 指针运算\n```c\nint arr[5] = {10, 20, 30, 40, 50};\nint *p = arr;  // 指向数组首元素\n\nprintf(\"%d\\n\", *p);       // 10\nprintf(\"%d\\n\", *(p+1));   // 20\nprintf(\"%d\\n\", *(p+2));   // 30\n\n// 遍历数组\nfor (int i = 0; i < 5; i++) {\n    printf(\"%d \", *(p + i));\n}\n```\n\n### 指针与函数\n```c\n// 通过指针修改值\nvoid swap(int *a, int *b) {\n    int temp = *a;\n    *a = *b;\n    *b = temp;\n}\n\nint x = 5, y = 10;\nswap(&x, &y);  // 传地址\n// 现在 x=10, y=5\n```\n\n### 动态内存分配\n```c\n#include <stdlib.h>\n\nint *arr = (int*)malloc(5 * sizeof(int));\nif (arr == NULL) {\n    printf(\"内存分配失败\");\n    return 1;\n}\n// 使用 arr...\nfree(arr);  // 释放内存\n```\n\n### 常见错误\n- 野指针：未初始化的指针\n- 空指针：指向 NULL 的指针，解引用会崩溃\n- 内存泄漏：malloc 后忘记 free\n- 悬空指针：free 后继续使用"
    },
    "函数": {
        "keywords": ["函数", "function", "return", "参数", "传值", "传址", "递归", "声明", "定义", "调用", "void", "main"],
        "content": "## C语言函数\n\n### 函数定义\n```c\n// 返回类型 函数名(参数列表) {\n//     函数体\n// }\n\nint add(int a, int b) {\n    return a + b;\n}\n```\n\n### 函数声明（原型）\n```c\n// 如果函数定义在使用之后，需要先声明\nint add(int a, int b);  // 声明\n\nint main() {\n    int result = add(3, 5);\n    return 0;\n}\n\nint add(int a, int b) {  // 定义\n    return a + b;\n}\n```\n\n### 传值 vs 传址\n```c\n// 传值（不影响原变量）\nvoid changeValue(int x) {\n    x = 100;\n}\n\n// 传址（可以修改原变量）\nvoid changeRef(int *x) {\n    *x = 100;\n}\n\nint a = 10;\nchangeValue(a);   // a 仍然是 10\nchangeRef(&a);    // a 变成 100\n```\n\n### 递归\n```c\n// 阶乘\nint factorial(int n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}\n\n// 斐波那契数列\nint fib(int n) {\n    if (n <= 1) return n;\n    return fib(n-1) + fib(n-2);\n}\n```\n\n### main 函数参数\n```c\nint main(int argc, char *argv[]) {\n    printf(\"参数个数: %d\\n\", argc);\n    for (int i = 0; i < argc; i++) {\n        printf(\"argv[%d] = %s\\n\", i, argv[i]);\n    }\n    return 0;\n}\n```"
    },
    "字符串": {
        "keywords": ["字符串", "string", "strlen", "strcpy", "strcat", "strcmp", "gets", "puts", "字符数组", "char"],
        "content": "## C语言字符串\n\n### 字符串声明\n```c\n// 方式一：字符数组\nchar str1[] = \"Hello\";  // 自动加 \\0\nchar str2[20] = \"World\";\n\n// 方式二：字符指针\nchar *str3 = \"Hello\";  // 字符串常量，不可修改\n\n// 方式三：逐个赋值\nchar str4[] = {'H', 'e', 'l', 'l', 'o', '\\0'};\n```\n\n### 常用字符串函数（需包含 <string.h>）\n```c\n#include <string.h>\n\nchar s1[20] = \"Hello\";\nchar s2[] = \"World\";\n\nint len = strlen(s1);          // 长度: 5\nstrcpy(s1, s2);                // 复制: s1 = \"World\"\nstrcat(s1, s2);                // 拼接: s1 = \"HelloWorld\"\nint cmp = strcmp(s1, s2);      // 比较: 0相等, <0 s1<s2, >0 s1>s2\n```\n\n### 字符串输入输出\n```c\nchar name[50];\n\nprintf(\"请输入姓名: \");\nscanf(\"%s\", name);             // 读取（遇到空格停止）\nfgets(name, 50, stdin);         // 安全读取（包括空格）\nprintf(\"你好, %s\\n\", name);    // 输出\n```\n\n### 字符处理函数（需包含 <ctype.h>）\n```c\n#include <ctype.h>\nisalpha(c)  // 是否为字母\nisdigit(c)  // 是否为数字\nisupper(c)  // 是否为大写\nislower(c)  // 是否为小写\ntoupper(c)  // 转大写\ntolower(c)  // 转小写\n```"
    },
    "结构体联合体": {
        "keywords": ["struct", "结构体", "union", "联合体", "typedef", "enum", "枚举", "成员", "->"],
        "content": "## C语言结构体与联合体\n\n### 结构体定义\n```c\nstruct Student {\n    char name[50];\n    int age;\n    float score;\n};\n\n// 使用\nstruct Student stu1;\nstrcpy(stu1.name, \"小明\");\nstu1.age = 18;\nstu1.score = 95.5;\n\nprintf(\"%s %d %.1f\\n\", stu1.name, stu1.age, stu1.score);\n```\n\n### typedef 简化类型名\n```c\ntypedef struct {\n    char name[50];\n    int age;\n    float score;\n} Student;\n\nStudent stu = {\"小明\", 18, 95.5};  // 不用写 struct 关键字\n```\n\n### 结构体指针\n```c\nStudent stu = {\"小明\", 18, 95.5};\nStudent *p = &stu;\n\n// 两种访问方式\nprintf(\"%s\\n\", (*p).name);   // 需要括号\nprintf(\"%s\\n\", p->name);     // 推荐：箭头运算符\n```\n\n### 结构体嵌套\n```c\ntypedef struct {\n    int year;\n    int month;\n    int day;\n} Date;\n\ntypedef struct {\n    char name[50];\n    Date birth;\n} Person;\n```\n\n### 联合体（union）\n```c\nunion Data {\n    int i;\n    float f;\n    char str[20];\n};\n\nunion Data data;\ndata.i = 10;        // 占4字节\ndata.f = 3.14;      // 覆盖 i，也占4字节\n// 所有成员共享同一块内存\n```\n\n### 枚举（enum）\n```c\nenum Weekday { MON, TUE, WED, THU, FRI, SAT, SUN };\nenum Weekday today = WED;\nprintf(\"%d\\n\", today);  // 2（从0开始编号）\n```"
    },
    "文件操作": {
        "keywords": ["文件", "file", "fopen", "fclose", "fread", "fwrite", "fprintf", "fscanf", "fgets", "fputs", "fseek", "feof"],
        "content": "## C语言文件操作\n\n### 打开和关闭文件\n```c\n#include <stdio.h>\n\nFILE *fp = fopen(\"data.txt\", \"r\");\nif (fp == NULL) {\n    printf(\"文件打开失败\\n\");\n    return 1;\n}\n\n// 文件操作...\n\nfclose(fp);  // 关闭文件\n```\n\n### 文件打开模式\n| 模式 | 含义 |\n|------|------|\n| \"r\" | 读取（文件必须存在） |\n| \"w\" | 写入（覆盖，不存在则创建） |\n| \"a\" | 追加 |\n| \"r+\" | 读写 |\n| \"w+\" | 读写（覆盖） |\n| \"a+\" | 读写（追加） |\n| \"rb\" | 二进制读取 |\n| \"wb\" | 二进制写入 |\n\n### 读取文件\n```c\nchar buffer[256];\n\n// 逐行读取\nwhile (fgets(buffer, sizeof(buffer), fp)) {\n    printf(\"%s\", buffer);\n}\n\n// 格式化读取\nint num;\nfscanf(fp, \"%d\", &num);\n```\n\n### 写入文件\n```c\nfprintf(fp, \"姓名: %s, 年龄: %d\\n\", \"小明\", 18);\nfputs(\"Hello, World!\\n\", fp);\nfputc(\"A\", fp);\n```\n\n### 二进制文件读写\n```c\n// 写入\nint data[5] = {1, 2, 3, 4, 5};\nfwrite(data, sizeof(int), 5, fp);\n\n// 读取\nint buffer[5];\nfread(buffer, sizeof(int), 5, fp);\n```\n\n### 文件定位\n```c\nfseek(fp, 0, SEEK_SET);  // 从头偏移0字节\nfseek(fp, 10, SEEK_CUR); // 从当前位置偏移10\nfseek(fp, 0, SEEK_END);  // 移动到末尾\nlong pos = ftell(fp);    // 获取当前位置\nrewind(fp);              // 回到开头\n```"
    },
    "内存管理": {
        "keywords": ["malloc", "calloc", "realloc", "free", "内存", "动态分配", "堆", "栈", "内存泄漏"],
        "content": "## C语言内存管理\n\n### 栈 vs 堆\n- **栈（Stack）**：局部变量自动分配和释放，大小有限\n- **堆（Heap）**：程序员手动分配和释放，空间大但需要管理\n\n### malloc 分配内存\n```c\n#include <stdlib.h>\n\n// 分配5个int的空间\nint *arr = (int*)malloc(5 * sizeof(int));\nif (arr == NULL) {\n    printf(\"内存分配失败\\n\");\n    return 1;\n}\n\n// 使用\nfor (int i = 0; i < 5; i++) {\n    arr[i] = i * 10;\n}\n\n// 释放\nfree(arr);\narr = NULL;  // 避免悬空指针\n```\n\n### calloc 分配并初始化为0\n```c\nint *arr = (int*)calloc(5, sizeof(int));\n// 所有元素自动初始化为0\n```\n\n### realloc 重新分配\n```c\nint *arr = (int*)malloc(5 * sizeof(int));\n// 扩展为10个int的空间\nint *temp = (int*)realloc(arr, 10 * sizeof(int));\nif (temp != NULL) {\n    arr = temp;\n} else {\n    printf(\"重新分配失败\\n\");\n}\n```\n\n### 常见问题\n| 问题 | 说明 |\n|------|------|\n| 内存泄漏 | malloc 后忘记 free |\n| 悬空指针 | free 后还继续使用 |\n| 缓冲区溢出 | 写超过分配的空间 |\n| 野指针 | 未初始化的指针 |\n| 重复释放 | 对同一块内存 free 两次 |\n\n### 最佳实践\n1. 每次 malloc 后检查是否为 NULL\n2. 成对使用 malloc/free\n3. free 后将指针置为 NULL\n4. 避免在函数外返回局部变量的地址"
    },
    "预处理": {
        "keywords": ["#define", "#include", "宏", "预处理", "头文件", "条件编译", "ifdef", "ifndef", "pragma", "typedef"],
        "content": "## C语言预处理指令\n\n### #include 包含头文件\n```c\n#include <stdio.h>    // 标准库头文件\n#include \"myheader.h\"  // 自定义头文件\n```\n\n### #define 宏定义\n```c\n#define PI 3.14159\n#define MAX(a, b) ((a) > (b) ? (a) : (b))\n#define SQUARE(x) ((x) * (x))\n\nint area = PI * r * r;\nint max = MAX(10, 20);     // 展开: ((10) > (20) ? (10) : (20))\n```\n\n### 条件编译\n```c\n#define DEBUG\n\n#ifdef DEBUG\n    printf(\"调试模式\\n\");\n#endif\n\n#ifndef RELEASE\n    printf(\"非发布版本\\n\");\n#endif\n\n#if defined(WIN32)\n    printf(\"Windows系统\\n\");\n#elif defined(__linux__)\n    printf(\"Linux系统\\n\");\n#else\n    printf(\"其他系统\\n\");\n#endif\n```\n\n### 预定义宏\n```c\nprintf(\"文件: %s\\n\", __FILE__);     // 当前文件名\nprintf(\"行号: %d\\n\", __LINE__);     // 当前行号\nprintf(\"日期: %s\\n\", __DATE__);     // 编译日期\nprintf(\"时间: %s\\n\", __TIME__);     // 编译时间\nprintf(\"函数: %s\\n\", __func__);     // 当前函数名\n```\n\n### #pragma 指令\n```c\n#pragma once  // 防止头文件重复包含\n\n// 或者使用传统方式\n#ifndef MYHEADER_H\n#define MYHEADER_H\n// 头文件内容...\n#endif\n```\n\n### typedef vs #define\n```c\ntypedef int* IntPtr;     // 类型别名\n#define INT_PTR int*    // 文本替换\n\nIntPtr a, b;    // a和b都是int*\nINT_PTR c, d;   // c是int*, d是int（危险！）\n```"
    },
    "常见错误": {
        "keywords": ["错误", "报错", "bug", "调试", "debug", "segmentation fault", "段错误", "编译错误", "链接错误", "运行时错误"],
        "content": "## C语言常见错误及调试\n\n### 编译错误\n```c\n// 忘记分号\nint a = 10  // 错误: 缺少;\n\n// 括号不匹配\nif (a > 0 {   // 错误: 缺少)\n\n// 变量未声明\nprintf(\"%d\", x);  // 错误: x未定义\n```\n\n### 链接错误\n```c\n// 函数声明了但没定义\n// undefined reference to `myFunc'\n// 检查: 是否包含了正确的.c文件\n```\n\n### 运行时错误\n| 错误 | 常见原因 |\n|------|---------|\n| 段错误 (Segmentation Fault) | 访问非法内存（野指针、数组越界、栈溢出） |\n| 浮点异常 (Floating Point Exception) | 除0错误 |\n| 缓冲区溢出 | 字符串操作超出数组范围 |\n| 内存泄漏 | malloc/free 不配对 |\n| 死循环 | 循环条件永不结束 |\n\n### 调试技巧\n```c\n#include <stdio.h>\n#include <assert.h>\n\n// 1. 打印调试\nprintf(\"DEBUG: x = %d, line = %d\\n\", x, __LINE__);\n\n// 2. 使用断言\nassert(p != NULL);  // 条件不成立时中止\n\n// 3. 使用调试器（gdb）\n// gcc -g program.c -o program\n// gdb ./program\n// break main  （设断点）\n// run         （运行）\n// print x     （打印变量）\n// next        （单步执行）\n```\n\n### 常见错误代码\n```c\n// 1. 忘记取地址符\nscanf(\"%d\", num);   // 错误: 应该是 &num\n\n// 2. 数组越界\nint arr[5];\narr[5] = 100;        // 错误: 最大下标是4\n\n// 3. 字符串比较用 ==\nif (str == \"hello\")  // 错误: 比较的是地址, 要用 strcmp\n\n// 4. 忘记 break\nswitch (n) {\n    case 1:          // 如果没用break, 会继续执行case 2\n        printf(\"1\");\n    case 2:\n        printf(\"2\");  // n=1 时也会输出 \"12\"\n}\n```"
    }
}


def find_answer(question):
    """根据用户问题从知识库中查找最匹配的回答"""
    question_lower = question.lower()
    best_match = None
    max_score = 0

    for topic, data in KNOWLEDGE_BASE.items():
        score = 0
        for keyword in data["keywords"]:
            if keyword.lower() in question_lower:
                score += 1
        if score > max_score:
            max_score = score
            best_match = data["content"]

    if max_score > 0:
        return best_match
    return None


def format_response(content, question):
    if content is None:
        return None
    response = "C语言学习小教练\n\n"
    response += "关于【%s】的相关知识：\n\n" % question
    response += content
    response += "\n\n---\n提示：以上内容来自内置知识库。如需更深入的解释，建议配置API密钥使用AI模式。"
    return response
