#include <iostream>
#include <fstream>
#include <sstream>    
#include <vector>
#include <thread>
#include <mutex>
#include <chrono>
#include <functional> 
#include "algorithm.h"  
#include "algorithm.cpp"  

using namespace std;
using namespace std::chrono;

// 定义一个结构体用于保存结果
struct Result {
    string algorithm_name;
    bool success;
    long long duration_ms;
};

// 线程安全的全局结果存储
vector<Result> all_results;
mutex result_mutex;  // 保护共享数据

// 图读取函数（与之前一致）
bool readColFile(const string& filename, vector<vector<int>>& graph) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "无法打开文件: " << filename << endl;
        return false;
    }

    string line;
    int numNodes = 0;

    while (getline(file, line)) {
        istringstream iss(line);
        char type;
        iss >> type;

        if (type == 'c') continue;

        else if (type == 'p') {
            string dummy;
            iss >> dummy >> numNodes;
            if (dummy != "edge" && dummy != "edges") {
                cerr << "不支持的问题类型: " << dummy << endl;
                return false;
            }
            graph.assign(numNodes, vector<int>());
        }

        else if (type == 'e') {
            int u, v;
            iss >> u >> v;
            u -= 1; v -= 1;
            if (u >= 0 && u < numNodes && v >= 0 && v < numNodes) {
                graph[u].push_back(v);
                graph[v].push_back(u);
            }
        }
    }

    file.close();
    return true;
}

// 执行单个算法的线程函数
void runAlgorithm(
    const vector<vector<int>>& graph,
    int m,
    const string& algo_name,
    function<bool(const vector<vector<int>>&, int, vector<int>&, long long)> algo_func,
    long long time_limit_ms
) {
    vector<int> colors;
    auto start = high_resolution_clock::now();

    bool success = algo_func(graph, m, colors, time_limit_ms);

    auto end = high_resolution_clock::now();
    long long duration = duration_cast<milliseconds>(end - start).count();

    ostringstream filename;
    filename << "result_" << algo_name << ".txt";
    ofstream fout(filename.str());
    if (success) {
        fout << "Coloring successful. Time: " << duration << " ms\n";
        fout << "Color assignment:\n";
        for (size_t i = 0; i < colors.size(); ++i) {
            fout << "Node " << i << ": Color " << colors[i] << '\n';
        }
    } else {
        fout << "Coloring failed or timed out. Time: " << duration << " ms\n";
    }

    lock_guard<mutex> lock(result_mutex);
    all_results.push_back({algo_name, success, duration});
}

int main() {
    // string filename = ".\\map\\le450_15b.col";  //第二问
    // string filename = "rand_map_100_200.col";  // 第三问
    // string filename = "rand_map_150_300.col";  
    // string filename = "rand_map_200_400.col";
    // string filename = "rand_map_250_500.col";
    // string filename = "rand_map_300_600.col";
    // string filename = "rand_map_350_700.col";
    // string filename = "rand_map_400_800.col";
    // string filename = "rand_map_450_900.col";
    string filename = "rand_map_500_1000.col";
    int m = 4;                       // 指定颜色数
    // long long time_limit_ms =900000; // 15分钟
    long long time_limit_ms = 10000; // 10秒

    vector<vector<int>> graph;
    cout << "正在读取 .col 文件..." << endl;
    if (!readColFile(filename, graph)) {
        cerr << "读取文件失败，请检查文件路径或格式。" << endl;
        return 1;
    }

    int n = graph.size();
    cout << "图加载成功，共 " << n << " 个节点。" << endl;

    // 创建线程分别运行不同算法
    vector<thread> threads;
    // threads.emplace_back(runAlgorithm, ref(graph), m, "Simple Backtrack", simple_backtrack, time_limit_ms);
    // threads.emplace_back(runAlgorithm, ref(graph), m, "Min Conflict", min_conflict_backtrack, time_limit_ms);
    // threads.emplace_back(runAlgorithm, ref(graph), m, "Forward Checking", forward_checking_backtrack, time_limit_ms);
    threads.emplace_back(runAlgorithm, ref(graph), m, "Min Conflict + Forward Checking", min_conflict_forward_checking_backtrack, time_limit_ms);
    // threads.emplace_back(runAlgorithm, ref(graph), m, "MRV", mrv_backtrack, time_limit_ms);
    // threads.emplace_back(runAlgorithm, ref(graph), m, "MRV + Min Conflict", mrv_min_conflict_backtrack, time_limit_ms);
    // threads.emplace_back(runAlgorithm, ref(graph), m, "MRV + Forward Checking", mrv_forward_checking_backtrack, time_limit_ms);
    threads.emplace_back(runAlgorithm, ref(graph), m, "MRV + Min Conflict + Forward Checking", mrv_min_conflict_forward_checking_backtrack, time_limit_ms);
    // threads.emplace_back(runAlgorithm, ref(graph), m, "DH", dh_backtrack, time_limit_ms);
    // threads.emplace_back(runAlgorithm, ref(graph), m, "DH + Min Conflict", dh_min_conflict_backtrack, time_limit_ms);
    // threads.emplace_back(runAlgorithm, ref(graph), m, "DH + FC", dh_forward_checking_backtrack, time_limit_ms);
    threads.emplace_back(runAlgorithm, ref(graph), m, "DH + Min Conflict + FC", dh_min_conflict_forward_checking_backtrack, time_limit_ms);
    threads.emplace_back(runAlgorithm, ref(graph), m, "MRV + DH", mrv_dh_backtrack, time_limit_ms);
    threads.emplace_back(runAlgorithm, ref(graph), m, "MRV + DH + Forward Checking", mrv_dh_forward_checking_backtrack, time_limit_ms);
    threads.emplace_back(runAlgorithm, ref(graph), m, "MRV + DH + MC", mrv_dh_mc_backtrack, time_limit_ms);
    threads.emplace_back(runAlgorithm, ref(graph), m, "MRV + DH + MC + FC", mrv_dh_mc_fc_backtrack, time_limit_ms);


    // 等待所有线程完成
    for (auto& t : threads)
        if (t.joinable())
            t.join();

    // 输出结果到 CSV 文件
    string resultname = "results" + filename.substr(8, filename.find(".") - 8) + ".csv";
    ofstream csv(resultname);
    if (!csv) {
        cerr << "无法创建 CSV 文件！" << endl;
        return 1;
    }

    csv << "Algorithm,Success,Time(ms)" << endl;
    for (const auto& res : all_results) {
        csv << res.algorithm_name << ","
            << (res.success ? "Yes" : "No") << ","
            << res.duration_ms << endl;
    }

    cout << "\n所有算法执行完成，结果已写入 " << resultname << endl;
    for (const auto& res : all_results) {
        cout << res.algorithm_name << ": "
             << (res.success ? "成功" : "超时/无解")
             << "，耗时 " << res.duration_ms << " ms" << endl;
    }

    return 0;
}