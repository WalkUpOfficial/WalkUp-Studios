#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>//windows编程头文件
#include <time.h>
#include <conio.h>//控制台输入输出头文件
#include <stdio.h>

// 获取控制台窗口大小
int CONSOLE_WIDTH, CONSOLE_HEIGHT;

// 初始化控制台大小
void initConsoleSize() {
    CONSOLE_SCREEN_BUFFER_INFO csbi;
    GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &csbi);
    CONSOLE_WIDTH = csbi.srWindow.Right - csbi.srWindow.Left + 1;
    CONSOLE_HEIGHT = csbi.srWindow.Bottom - csbi.srWindow.Top + 1;
}

#define SNAKESIZE 3000  //蛇的身体最大节数

#ifndef __cplusplus
typedef char bool;
#define false 0
#define true  1
#endif

//食物的坐标
struct {
    int x;
    int y;
}food;

//蛇的相关属性
struct {
    int speed;//蛇移动的速度
    int len;//蛇的长度
    int x[SNAKESIZE];//组成蛇身的每一个小方块中x的坐标
    int y[SNAKESIZE];//组成蛇身的每一个小方块中y的坐标
}snake;

//将光标移动到控制台的(x,y)坐标点处
void gotoxy(int x, int y) {
    COORD coord;
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

//绘制游戏边框
void drawMap();
//随机生成食物
void createFood();
//按键操作
void keyDown();
//蛇的状态
bool snakeStatus();

int key = 72;//表示蛇移动的方向，72为按下"↑"所代表的数字
int changeFlag = 0;
int score = 0;//记录玩家的得分
int i;

void drawMap() {
    // 初始化控制台大小
    initConsoleSize();
    
    // 计算游戏区域大小（留出边界）
    int GAME_WIDTH = CONSOLE_WIDTH - 8;  // 左右各留4个字符
    int GAME_HEIGHT = CONSOLE_HEIGHT - 4; // 上下各留2个字符
    
    // 确保宽度为偶数，方便蛇移动
    if (GAME_WIDTH % 2 != 0) GAME_WIDTH--;
    
    // 计算游戏区域起始位置（居中显示）
    int startX = 2;
    int startY = 2;
    
    // 打印上边框
    for (i = 0; i <= GAME_WIDTH; i++) {
        gotoxy(startX + i, startY);
        printf("8");
    }
    
    // 打印下边框
    for (i = 0; i <= GAME_WIDTH; i++) {
        gotoxy(startX + i, startY + GAME_HEIGHT);
        printf("8");
    }
    
    // 打印左边框
    for (i = 0; i < GAME_HEIGHT; i++) {
        gotoxy(startX, startY + i);
        printf("8");
    }
    
    // 打印右边框
    for (i = 0; i < GAME_HEIGHT; i++) {
        gotoxy(startX + GAME_WIDTH, startY + i);
        printf("8");
    }
    
    // 随机生成初始食物
    while (1) {
        srand((unsigned int)time(NULL));
        food.x = startX + rand() % (GAME_WIDTH - 4) + 2;
        food.y = startY + rand() % (GAME_HEIGHT - 2) + 1;
        if (food.x % 2 == 0)  // 确保横坐标为偶数
            break;
    }
    
    // 绘制食物
    gotoxy(food.x, food.y);
    printf("apple");
    
    // 初始化蛇的属性
    snake.len = 3;
    snake.speed = 150;
    
    // 在游戏区域中间生成蛇头
    snake.x[0] = startX + GAME_WIDTH / 2;
    snake.y[0] = startY + GAME_HEIGHT / 2;
    
    // 确保蛇头横坐标为偶数
    if (snake.x[0] % 2 != 0) snake.x[0]--;
    
    // 打印蛇头
    gotoxy(snake.x[0], snake.y[0]);
    printf("91");
    
    // 生成初始蛇身
    for (i = 1; i < snake.len; i++) {
        snake.x[i] = snake.x[i - 1] + 2;
        snake.y[i] = snake.y[i - 1];
        gotoxy(snake.x[i], snake.y[i]);
        printf("91");
    }
    
    // 显示得分
    gotoxy(2, 0);
    printf("得分: %d", score);
    gotoxy(CONSOLE_WIDTH - 20, 0);
    printf("按 Alt + F4 退出");
    
    return;
}

void keyDown() {
    int pre_key = key;
    
    if (_kbhit()) {
        int ch = _getch();
        if (ch == 224 || ch == 0) {  // 方向键
            ch = _getch();
            if (ch == 72 || ch == 80 || ch == 75 || ch == 77) {
                key = ch;
            }
        } else if (ch == 27) {  // ESC键退出
            exit(0);
        }
    }
    
    // 擦除蛇尾
    if (changeFlag == 0) {
        gotoxy(snake.x[snake.len - 1], snake.y[snake.len - 1]);
        printf("  ");
    }
    
    // 移动蛇身
    for (i = snake.len - 1; i > 0; i--) {
        snake.x[i] = snake.x[i - 1];
        snake.y[i] = snake.y[i - 1];
    }
    
    // 防止反向移动
    if ((pre_key == 72 && key == 80) || (pre_key == 80 && key == 72) ||
        (pre_key == 75 && key == 77) || (pre_key == 77 && key == 75)) {
        key = pre_key;
    }
    
    // 根据方向移动蛇头
    if (key == 75) {  // 左
        snake.x[0] -= 2;
    } else if (key == 77) {  // 右
        snake.x[0] += 2;
    } else if (key == 72) {  // 上
        snake.y[0]--;
    } else if (key == 80) {  // 下
        snake.y[0]++;
    }
    
    // 打印蛇头
    gotoxy(snake.x[0], snake.y[0]);
    
    
    
//    printf("ME");
//    printf("I-ME.have.9\78");
    time_t now = time(0);  // 获取当前时间
	struct tm *local = localtime(&now);  // 转换为本地时间结构
	    
	printf("[%02d : %02d : %02d]\n", 
	        local->tm_hour,  // 时 (0-23)
	        local->tm_min,   // 分 (0-59)
	        local->tm_sec);  // 秒 (0-61)
    
    
    changeFlag = 0;
    return;
}

void createFood() {
    initConsoleSize();
    int GAME_WIDTH = CONSOLE_WIDTH - 4;
    int GAME_HEIGHT = CONSOLE_HEIGHT - 4;
    int startX = 2;
    int startY = 2;
    
    if (snake.x[0] == food.x && snake.y[0] == food.y) {
        // 生成新食物
        while (1) {
            int flag = 1;
            srand((unsigned int)time(NULL));
            food.x = startX + rand() % (GAME_WIDTH - 4) + 2;
            food.y = startY + rand() % (GAME_HEIGHT - 2) + 1;
            
            // 食物不能在蛇身上
            for (i = 0; i < snake.len; i++) {
                if (snake.x[i] == food.x && snake.y[i] == food.y) {
                    flag = 0;
                    break;
                }
            }
            
            if (flag && food.x % 2 == 0)
                break;
        }
        
        // 绘制新食物
        gotoxy(food.x, food.y);
        printf("apple");
        
        // 增加长度和分数
        snake.len += 3;
        score += 10;
        
        // 更新得分显示
        gotoxy(2, 0);
        printf("得分: %d", score);
        
        changeFlag = 1;
    }
    return;
}

bool snakeStatus() {
    initConsoleSize();
    int GAME_WIDTH = CONSOLE_WIDTH - 4;
    int GAME_HEIGHT = CONSOLE_HEIGHT - 4;
    int startX = 2;
    int startY = 2;
    
    return true;
}

int main() {
    // 隐藏光标
    CONSOLE_CURSOR_INFO cursorInfo = {1, 0};
    SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursorInfo);
    
    // 设置窗口全屏
    system("mode con cols=120 lines=40");  // 可以根据需要调整大小
    system("title 贪吃蛇游戏");
    
    drawMap();
    
    while (1) {
        keyDown();
        if (!snakeStatus())
            break;
        createFood();
        Sleep(50);
    }
    
    // 游戏结束
    system("cls");
    gotoxy(40, 15);
    printf("游戏结束！");
    gotoxy(40, 16);
    printf("最终得分: %d", score);
    gotoxy(40, 18);
    printf("3秒后退出...");
    
    Sleep(3000);
    return 0;
}
