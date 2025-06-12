#include <iostream>
#include <vector>
#include <queue>
#include <set>
#include <tuple>
#include <chrono>
using namespace std;
using namespace std::chrono;  

// BFS������ͨ��������
int countComponents(int n, const vector<vector<int>>& adj, set<pair<int, int>> removedEdges) {
    vector<bool> visited(n, false);
    int components = 0;
    
    for (int start = 0; start < n; ++start) {
        if (!visited[start]) {
            components++;
            queue<int> q;
            q.push(start);
            visited[start] = true;

            while (!q.empty()) {
                int u = q.front(); q.pop();
                for (int v : adj[u]) {
                    // ������ɾ���ı�
                    if (removedEdges.count({u, v}) || removedEdges.count({v, u})) continue;

                    if (!visited[v]) {
                        visited[v] = true;
                        q.push(v);
                    }
                }
            }
        }
    }
    return components;
}

int main() {
    freopen("smallG.txt", "r", stdin);
    // freopen("mediumDG.txt", "r", stdin);
    // freopen("largeG.txt", "r", stdin);
    int n, m;
    cin >> n >> m; 

    vector<vector<int>> adj(n);
    vector<pair<int, int>> edges;

    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
        edges.push_back({u, v});
    }

    // ===================
    // ��ʼ��ʱ
    // ===================
    auto start_time = high_resolution_clock::now();
    cout << "��ʼ�㷨ִ�У���ʱ��ʼ..." << endl;

    // ԭͼ��ͨ��������
    int originalComponents = countComponents(n, adj, {});

    int bridgeCount = 0;

    for (auto [u, v] : edges) {
        set<pair<int, int>> removedEdges = {{u, v}};
        int newComponents = countComponents(n, adj, removedEdges);
        if (newComponents > originalComponents) {
            bridgeCount++;
        }
    }

    cout << "������: " << bridgeCount << endl;

    // ===================
    // ������ʱ
    // ===================
    auto end_time = high_resolution_clock::now();

    auto duration_ms = duration_cast<milliseconds>(end_time - start_time);  
    cout << "�㷨ִ��ʱ��: " << duration_ms.count() << " ����" << endl;
    return 0;
}
