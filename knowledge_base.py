# C语言学习小教练 - 本地知识库（增强版）

import re
import difflib

KNOWLEDGE_BASE = {
    "基础语法": {
        "keywords": ["printf", "scanf", "变量", "数据类型", "int", "char", "float", "double",
                     "const", "sizeof", "输出", "输入", "注释", "常量", "标识符", "关键字"],
        "related": ["变量", "数据类型转换", "类型转换", "格式化", "转义"],
        "content": """## C语言基础语法

### Hello World
`c
#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}
`

### 基本数据类型
| 类型 | 大小 | 范围 | 格式化 |
|------|------|------|--------|
| char | 1字节 | -128 ~ 127 | %c |
| int | 4字节 | -2^31 ~ 2^31-1 | %d |
| unsigned int | 4字节 | 0 ~ 2^32-1 | %u |
| float | 4字节 | 约6位精度 | %f |
| double | 8字节 | 约15位精度 | %lf |
| long long | 8字节 | -2^63 ~ 2^63-1 | %lld |

### 变量声明与赋值
`c
int age = 18;
float pi = 3.14;
char grade = 'A';
const int MAX = 100;  // 常量不可修改
`

### 输入输出
`c
int num;
printf("请输入一个数字: ");
scanf("%d", &num);  // 注意 & 取地址符
printf("你输入的是: %d\\n", num);
`

**💡 常见错误**：scanf 忘记加 & 会导致段错误！
"""
    },
    "控制流": {
        "keywords": ["if", "else", "switch", "case", "for", "while", "do", "循环",
                     "条件", "判断", "break", "continue", "goto", "分支"],
        "related": ["三元运算符", "短路求值", "死循环"],
        "content": """## C语言控制流

### if-else
`c
int score = 85;
if (score >= 90) {
    printf("优秀\\n");
} else if (score >= 80) {
    printf("良好\\n");
} else if (score >= 60) {
    printf("及格\\n");
} else {
    printf("不及格\\n");
}
`

### switch（注意一定要 break!）
`c
int option = 2;
switch (option) {
    case 1: printf("选项1\\n"); break;
    case 2: printf("选项2\\n"); break;
    default: printf("其他\\n"); break;
}
// 忘记 break 会"穿透"执行下一个 case
`

### for 循环
`c
for (int i = 0; i < 5; i++) {
    printf("%d ", i);  // 0 1 2 3 4
}
`

### while 与 do-while
`c
// while: 先判断后执行
int i = 0;
while (i < 5) { printf("%d ", i); i++; }

// do-while: 至少执行一次
int j = 0;
do { printf("%d ", j); j++; } while (j < 5);
`

### break vs continue
| 关键字 | 作用 |
|--------|------|
| break | 立即跳出整个循环 |
| continue | 跳过本次循环剩余语句，进入下一次 |
"""
    },
    "数组": {
        "keywords": ["数组", "array", "二维数组", "多维数组", "下标", "索引", "遍历",
                     "变长数组", "VLA", "数组初始化"],
        "related": ["数组越界", "数组参数"],
        "content": """## C语言数组

### 一维数组
`c
int nums[5] = {1, 2, 3, 4, 5};  // 完全初始化
int arr[] = {10, 20, 30};        // 自动推断大小为3
int zeros[10] = {0};             // 全部初始化为0

nums[0] = 100;                    // 修改
printf("%d", nums[2]);           // 访问

// 遍历
for (int i = 0; i < 5; i++) {
    printf("%d ", nums[i]);
}
`

### 二维数组
`c
int matrix[2][3] = {
    {1, 2, 3},
    {4, 5, 6}
};

for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 3; j++) {
        printf("%d ", matrix[i][j]);
    }
    printf("\\n");
}
// 内存中实际是连续存储的
`

### 数组作为函数参数
`c
// 数组传参时会退化为指针！sizeof(arr) 会得到指针大小
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
}
// 调用: printArray(nums, 5);
`

**💡 关键区别**：
`c
int arr[5];
printf("%zu\\n", sizeof(arr));  // 20 (5 * 4)
void func(int arr[]) {
    printf("%zu\\n", sizeof(arr));  // 8 或 4（指针大小！）
}
`
"""
    },
    "指针": {
        "keywords": ["指针", "pointer", "*", "&", "NULL", "地址", "引用", "解引用",
                     "野指针", "空指针", "指针运算", "指针数组", "数组指针", "函数指针",
                     "二级指针", "void*", "const指针"],
        "related": ["指针和数组", "指针函数", "动态内存"],
        "content": """## C语言指针

### 指针基础
`c
int a = 10;
int *p = &a;   // p 存放 a 的地址

printf("a的值: %d\\n", a);      // 10
printf("a的地址: %p\\n", &a);
printf("p的值: %p\\n", p);       // 同 &a
printf("p指向的值: %d\\n", *p);  // 10（解引用）
`

### 指针与数组
`c
int arr[5] = {10, 20, 30, 40, 50};
int *p = arr;  // 数组名就是首地址

// 以下三种写法等价
printf("%d\\n", arr[2]);     // 30
printf("%d\\n", *(arr+2));   // 30
printf("%d\\n", *(p+2));     // 30
`

### 指针与 const
`c
const int *p;     // 指向常量的指针（不能改值，能改指向）
int * const p;    // 指针常量（能改值，不能改指向）
const int * const p; // 都不能改
`

### 函数指针
`c
int add(int a, int b) { return a + b; }
int (*func_ptr)(int, int) = add;
printf("%d\\n", func_ptr(3, 5));  // 8
`

### 常见错误
- **野指针**：未初始化的指针，指向随机地址
- **空指针**：p = NULL 后解引用会崩溃
- **悬空指针**：free 后没置 NULL，继续使用
- **内存泄漏**：malloc 后忘记 free
"""
    },
    "函数": {
        "keywords": ["函数", "function", "return", "参数", "传值", "传址", "递归",
                     "声明", "定义", "调用", "void", "main", "内联", "inline",
                     "static函数", "可变参数"],
        "related": ["递归", "函数指针", "栈帧"],
        "content": """## C语言函数

### 函数定义与声明
`c
// 函数定义
int add(int a, int b) {
    return a + b;
}

// 如果定义在使用之后，需要先声明（函数原型）
int add(int a, int b);

int main() {
    int result = add(3, 5);
    return 0;
}
`

### 传值 vs 传址
`c
void changeValue(int x) { x = 100; }   // 不影响原变量
void changeRef(int *x)  { *x = 100; }  // 可以修改

int a = 10;
changeValue(a);   // a 仍然是 10
changeRef(&a);    // a 变成 100
`

### static 函数
`c
// static 函数只在本文件可见，防止命名冲突
static void helper() {
    // 仅当前 .c 文件可用
}
`

### 递归
`c
// 阶乘
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// 递归注意：要有终止条件，避免栈溢出
`
"""
    },
    "字符串": {
        "keywords": ["字符串", "string", "strlen", "strcpy", "strcat", "strcmp",
                     "gets", "puts", "字符数组", "char", "sprintf", "sscanf",
                     "strtok", "strstr", "strchr", "strncpy"],
        "related": ["字符串字面量", "字符指针vs数组"],
        "content": """## C语言字符串

### 字符串声明方式
`c
char str1[] = "Hello";       // 可修改，栈上分配
char *str2 = "Hello";        // 字符串常量，不可修改！
char str3[20] = "World";
`

### 常用字符串函数（<string.h>）
`c
#include <string.h>

char s1[20] = "Hello";
char s2[] = "World";

strlen(s1);               // 长度: 5（不包含 \\0）
strcpy(s1, s2);           // 复制: s1 = "World"
strncpy(s1, s2, 5);       // 安全复制
strcat(s1, s2);           // 拼接: s1 = "HelloWorld"
strncat(s1, s2, 3);       // 安全拼接
strcmp(s1, s2);           // 比较: 0相等，<0 s1<s2
strstr(s1, "ello");       // 查找子串
`

### strlen vs sizeof
`c
char str[] = "Hello";
printf("%zu\\n", strlen(str));  // 5（字符个数）
printf("%zu\\n", sizeof(str));  // 6（包含 \\0）
`

**⚠️**：gets() 不安全（缓冲区溢出），用 gets() 代替：
`c
char buf[100];
fgets(buf, sizeof(buf), stdin);  // 安全！
`
"""
    },
    "结构体联合体": {
        "keywords": ["struct", "结构体", "union", "联合体", "typedef", "enum",
                     "枚举", "成员", "->", "位域", "对齐", "padding", "结构体指针"],
        "related": ["内存对齐", "位域", "结构体嵌套"],
        "content": """## C语言结构体与联合体

### 结构体定义和使用
`c
struct Student {
    char name[50];
    int age;
    float score;
};

struct Student stu1;
strcpy(stu1.name, "小明");
stu1.age = 18;
stu1.score = 95.5;
`

### typedef 简化
`c
typedef struct {
    char name[50];
    int age;
    float score;
} Student;

Student stu = {"小明", 18, 95.5};  // 不用写 struct
`

### 结构体指针
`c
Student stu = {"小明", 18, 95.5};
Student *p = &stu;
printf("%s\\n", (*p).name);  // 需要括号
printf("%s\\n", p->name);    // 推荐！
`

### 内存对齐（重要！）
`c
struct Example {
    char c;      // 1字节
    // 3字节 padding
    int i;       // 4字节
};
// sizeof(struct Example) = 8，不是 5！
`

### 联合体（union）— 所有成员共享内存
`c
union Data {
    int i;       // 4字节
    float f;     // 4字节
    char str[4]; // 4字节
};
// sizeof(union Data) = 4（最大成员的大小）
`

### 枚举
`c
enum Weekday { MON=1, TUE, WED, THU, FRI, SAT, SUN };
enum Weekday today = WED;
printf("%d\\n", today);  // 3
`
"""
    },
    "文件操作": {
        "keywords": ["文件", "file", "fopen", "fclose", "fread", "fwrite", "fprintf",
                     "fscanf", "fgets", "fputs", "fseek", "feof", "ferror", "ftell",
                     "rewind", "二进制", "文本", "FILE"],
        "related": ["文件指针", "错误处理"],
        "content": """## C语言文件操作

### 打开和关闭文件
`c
FILE *fp = fopen("data.txt", "r");
if (fp == NULL) {
    perror("文件打开失败");  // 打印具体错误原因
    return 1;
}
// 操作...
fclose(fp);
`

### 文件打开模式
| 模式 | 含义 | 文件不存在时 |
|------|------|------------|
| "r" | 读取 | 返回NULL |
| "w" | 写入（覆盖） | 创建 |
| "a" | 追加 | 创建 |
| "r+" | 读写 | 返回NULL |
| "w+" | 读写（覆盖） | 创建 |
| "rb"/"wb" | 二进制模式 | — |

### 逐行读取
`c
char buffer[256];
while (fgets(buffer, sizeof(buffer), fp)) {
    printf("%s", buffer);
}
`

### 写入文件
`c
fprintf(fp, "姓名: %s, 年龄: %d\\n", "小明", 18);
fputs("Hello, World!\\n", fp);
`

### 二进制文件
`c
int data[5] = {1, 2, 3, 4, 5};
fwrite(data, sizeof(int), 5, fp);  // 写入

int buffer[5];
fread(buffer, sizeof(int), 5, fp); // 读取
`

### 文件定位
`c
fseek(fp, 0, SEEK_SET);   // 移到开头
fseek(fp, 10, SEEK_CUR);  // 当前位置后移10字节
fseek(fp, 0, SEEK_END);   // 移到末尾
long pos = ftell(fp);      // 当前位置
rewind(fp);                // 回到开头
`
"""
    },
    "内存管理": {
        "keywords": ["malloc", "calloc", "realloc", "free", "内存", "动态分配",
                     "堆", "栈", "内存泄漏", "内存碎片", "aligned_alloc"],
        "related": ["内存池", "RAII", "智能指针(C++)"],
        "content": """## C语言内存管理

### 栈 vs 堆
| 特性 | 栈（Stack） | 堆（Heap） |
|------|------------|------------|
| 分配方式 | 自动 | 手动（malloc/free） |
| 速度 | 快 | 慢 |
| 大小 | 小（约1-8MB） | 大（可用内存） |
| 生命周期 | 函数结束自动释放 | 直到 free |

### malloc
`c
int *arr = (int*)malloc(5 * sizeof(int));
if (arr == NULL) {
    fprintf(stderr, "内存分配失败\\n");
    return 1;
}
// 使用...
free(arr);
arr = NULL;  // 避免悬空指针！
`

### calloc — 分配并清零
`c
int *arr = (int*)calloc(5, sizeof(int));
// 所有元素自动初始化为0，比 malloc + memset 更高效
`

### realloc — 重新分配
`c
int *arr = (int*)malloc(5 * sizeof(int));
int *temp = (int*)realloc(arr, 10 * sizeof(int));
if (temp != NULL) {
    arr = temp;  // 注意：要用临时变量，realloc失败返回NULL
} else {
    // 原内存仍然有效，arr 不能丢
    fprintf(stderr, "realloc失败\\n");
}
`

### 常见问题对照表
| 问题 | 原因 | 后果 |
|------|------|------|
| 内存泄漏 | malloc 后忘记 free | 内存耗尽 |
| 悬空指针 | free 后继续使用 | 数据损坏/崩溃 |
| 缓冲区溢出 | 写超过分配空间 | 安全漏洞 |
| 野指针 | 未初始化指针 | 段错误 |
| 重复释放 | double free | 程序崩溃 |
| 使用未分配内存 | 访问 NULL 指针 | 段错误 |

### 最佳实践
1. 每次 malloc 后**必须检查 NULL**
2. malloc/free **成对出现**
3. free 后立即置 NULL
4. 使用 algrind 检测内存泄漏
5. 避免在函数外返回局部变量地址
"""
    },
    "预处理": {
        "keywords": ["#define", "#include", "宏", "预处理", "头文件", "条件编译",
                     "ifdef", "ifndef", "pragma", "typedef", "宏函数", "##",
                     "#运算符", "可变参数宏", "内联函数"],
        "related": ["宏 vs 函数", "头文件守卫"],
        "content": """## C语言预处理指令

### #include
`c
#include <stdio.h>    // 标准库路径
#include "myheader.h"  // 当前目录
`

### #define 宏
`c
#define PI 3.14159
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define SQUARE(x) ((x) * (x))

int max = MAX(10, 20);  // 展开: ((10) > (20) ? (10) : (20))
`

**⚠️ 宏的陷阱**：
`c
#define BAD_SQUARE(x) x * x
BAD_SQUARE(1+2)  // 展开为 1+2*1+2 = 5，不是9！
// 正确: #define SQUARE(x) ((x) * (x))
`

### 条件编译
`c
#ifdef DEBUG
    printf("调试模式\\n");
#endif

#ifndef RELEASE
    printf("非发布版本\\n");
#endif

#if defined(WIN32)
    printf("Windows\\n");
#elif defined(__linux__)
    printf("Linux\\n");
#endif
`

### 预定义宏
`c
__FILE__   // 当前文件名
__LINE__   // 当前行号
__DATE__   // 编译日期
__TIME__   // 编译时间
__func__   // 当前函数名（C99）
`

### 头文件守卫
`c
#ifndef MYHEADER_H
#define MYHEADER_H
// 头文件内容...
#endif
// 或: #pragma once
`
"""
    },
    "常见错误": {
        "keywords": ["错误", "报错", "bug", "调试", "debug", "segmentation fault",
                     "段错误", "编译错误", "链接错误", "运行时错误", "assert",
                     "gdb", "valgrind", "core dump", "栈溢出"],
        "related": ["调试技巧", "防御性编程"],
        "content": """## C语言常见错误及调试

### 1. 段错误（Segmentation Fault）
最常见、最难排查的错误。原因：
- 解引用空指针或野指针
- 数组越界
- 栈溢出（递归太深）
- 修改字符串常量

### 2. 编译错误
`c
int a = 10    // 忘记分号
if (a > 0 {   // 括号不匹配
printf("%d", x);  // x 未声明
`

### 3. 链接错误
`
undefined reference to myFunc'
`
解决：检查是否：
- 包含了正确的 .c 文件
- 函数名拼写正确
- 链接了所需的库（-lm 数学库）

### 4. 运行时错误
| 错误 | 常见原因 |
|------|---------|
| 段错误 | 野指针、越界、栈溢出 |
| 浮点异常 | 除0、模0 |
| 断言失败 | assert() 条件为假 |
| 缓冲区溢出 | strcpy 写超数组范围 |

### 调试工具
`ash
# gcc 编译带调试信息
gcc -g -Wall -Wextra program.c -o program

# GDB 调试器
gdb ./program
  break main     # 设断点
  run            # 运行
  print x        # 打印变量
  backtrace      # 查看调用栈
  next / step    # 单步

# Valgrind 检测内存
valgrind --leak-check=full ./program
`

### 防御性编程习惯
1. 总是检查 malloc/fopen 返回值
2. 用 fgets 代替 gets
3. 用 strncpy 代替 strcpy
4. 初始化所有变量
5. 使用 assert 验证前提条件
6. 启用编译器警告：-Wall -Wextra -Werror
"""
    },
    "位运算": {
        "keywords": ["位运算", "按位与", "按位或", "按位异或", "按位取反", "左移",
                     "右移", "&", "|", "^", "~", "<<", ">>", "掩码", "bit"],
        "related": ["位域", "性能优化", "标志位"],
        "content": """## C语言位运算

### 基本位运算符
| 运算符 | 名称 | 示例 | 结果 |
|--------|------|------|------|
| & | 按位与 | 5 & 3 | 1 |
| \\| | 按位或 | 5 \\| 3 | 7 |
| ^ | 按位异或 | 5 ^ 3 | 6 |
| ~ | 按位取反 | ~5 | -6 |
| << | 左移 | 5 << 1 | 10 |
| >> | 右移 | 5 >> 1 | 2 |

### 常用技巧
`c
// 检查第n位是否为1
if (x & (1 << n)) { }

// 设置第n位为1
x |= (1 << n);

// 清除第n位
x &= ~(1 << n);

// 翻转第n位
x ^= (1 << n);

// 判断奇偶
if (x & 1) { /* 奇数 */ }

// 交换两个数（不用临时变量）
a ^= b; b ^= a; a ^= b;
`

### 用位运算表示标志位
`c
#define FLAG_READ   (1 << 0)  // 0001
#define FLAG_WRITE  (1 << 1)  // 0010
#define FLAG_EXEC   (1 << 2)  // 0100

int flags = FLAG_READ | FLAG_WRITE;  // 0011
if (flags & FLAG_READ) { /* 有读权限 */ }
`
"""
    },
    "链表": {
        "keywords": ["链表", "linked list", "list", "节点", "node", "遍历",
                     "插入", "删除", "单向链表", "双向链表", "循环链表"],
        "related": ["指针", "动态内存", "数据结构"],
        "content": """## C语言链表

### 单向链表节点定义
`c
typedef struct Node {
    int data;
    struct Node *next;
} Node;

// 创建节点
Node* create_node(int data) {
    Node *node = (Node*)malloc(sizeof(Node));
    if (!node) return NULL;
    node->data = data;
    node->next = NULL;
    return node;
}

// 遍历
void print_list(Node *head) {
    while (head) {
        printf("%d -> ", head->data);
        head = head->next;
    }
    printf("NULL\\n");
}
`

### 插入节点
`c
// 头部插入
void push_front(Node **head, int data) {
    Node *node = create_node(data);
    node->next = *head;
    *head = node;
}

// 尾部插入
void push_back(Node **head, int data) {
    Node *node = create_node(data);
    if (!*head) { *head = node; return; }
    Node *cur = *head;
    while (cur->next) cur = cur->next;
    cur->next = node;
}
`

### 删除节点
`c
void delete_node(Node **head, int data) {
    if (!*head) return;
    Node *cur = *head, *prev = NULL;
    while (cur && cur->data != data) {
        prev = cur;
        cur = cur->next;
    }
    if (!cur) return;  // 没找到
    if (!prev) *head = cur->next;  // 删头节点
    else prev->next = cur->next;
    free(cur);
}
`
"""
    }
}


def fuzzy_match_keyword(question, keyword):
    """模糊匹配：支持拼写错误和小变化"""
    q_lower = question.lower()
    k_lower = keyword.lower()
    # 直接包含
    if k_lower in q_lower:
        return True
    # 模糊匹配（对英语关键词）
    if len(k_lower) > 3 and k_lower.isascii():
        ratio = difflib.SequenceMatcher(None, k_lower, q_lower).ratio()
        if ratio > 0.8:
            return True
        # 检查关键词是否在问题中的某个词附近
        for word in q_lower.split():
            if difflib.SequenceMatcher(None, k_lower, word).ratio() > 0.75:
                return True
    return False


def score_topic(question, topic_data):
    """计算问题与某个主题的匹配得分"""
    q_lower = question.lower()
    score = 0

    # 关键词匹配
    for keyword in topic_data["keywords"]:
        if fuzzy_match_keyword(question, keyword):
            score += 3  # 关键词权重高

    # 相关词匹配
    for related in topic_data.get("related", []):
        if fuzzy_match_keyword(question, related):
            score += 1

    return score


def find_answer(question):
    """根据用户问题从知识库中查找最匹配的回答"""
    if not question:
        return None

    best_match = None
    max_score = 0

    for topic, data in KNOWLEDGE_BASE.items():
        score = score_topic(question, data)
        if score > max_score:
            max_score = score
            best_match = data["content"]

    if max_score >= 2:  # 至少匹配一个关键词
        return best_match
    return None


def get_suggestions(question):
    """根据问题推荐相关主题"""
    q_lower = question.lower()
    scores = []
    for topic, data in KNOWLEDGE_BASE.items():
        score = score_topic(question, data)
        if score > 0:
            scores.append((score, topic))
    scores.sort(reverse=True)
    return [t for _, t in scores[:3]]


def format_response(content, question):
    """格式化知识库回答"""
    if content is None:
        return None
    response = "📚 **来自本地知识库的回答**\n\n"
    response += content
    response += "\n\n---\n💡 *以上内容来自内置知识库。配置API密钥（推荐 DeepSeek）可解锁 AI 模式，获得更灵活深入的解释。*"
    return response