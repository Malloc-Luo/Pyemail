#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main(int argc, char** argv)
{
    const string filename = "C:\\Program Files\\pyemail\\target.~";
    const string tempfile = "\\temp.~";
    static string target;

    /*打开读取target文件找到路径*/
    try
    {
        ifstream in;
        in.open(filename, ios::in);
        in >> target;

        in.close();
    }
    catch (const char *msg)
    {
        cerr << "try to run setup.exe to slove this problem" << endl;
        exit(0);
    }


    try
    {
        ofstream out;

        out.open(target + tempfile, ios::out);

        /* 命令参数写入 temp.~ 分行*/
        /* 读取时候注意去掉换行符 */
        for (int i = 1; i < argc; i++)
        {
            out << argv[i] << endl;
        }

        out.close();
    }
    catch (const char *msg)
    {
        cerr << "try to run setup.exe to slove this problem" << endl;
        exit(0);
    }
    

/* 启动python脚本 */
#if defined (WIN32) || defined (WIN64)
    string cmd = "python " + target + "\\main.py";
    system(cmd.data());
#elif defined (__gnu_linux__)

    system("python3 main.py");
#endif

    return 0;
}

