#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>
#include <stack>
#include <chrono>  
using namespace std;
using namespace std::chrono;  

const int MAXN = 1000005;
const int LOGN = 20;

int n, m;
vector<pair<int, int>> edges;
vector<int> tree[MAXN];
int parent[MAXN], depth[MAXN];
int fa[MAXN][LOGN];
int diff[MAXN];
int res = 0;
int comp_id[MAXN];
int curr_comp = 0;
bool visited[MAXN];
vector<int> comp_roots; // �洢ÿ����ͨ�����ĸ��ڵ�

int find(int x) {
    return parent[x] == x ? x : parent[x] = find(parent[x]);
}

void unionSet(int x, int y) {
    parent[find(x)] = find(y);
}

// �ǵݹ�DFS������ջ���
void dfs_iterative(int start) {
    stack<pair<int, int>> stk; // (node, parent)
    stk.push({start, -1});
    
    while (!stk.empty()) {
        auto [u, p] = stk.top();
        stk.pop();
        
        if (visited[u]) continue;
        
        visited[u] = true;
        comp_id[u] = curr_comp;
        
        fa[u][0] = p;
        depth[u] = (p == -1) ? 0 : depth[p] + 1;
        
        // Ԥ����������
        for (int i = 1; i < LOGN; ++i) {
            if (fa[u][i-1] == -1) {
                fa[u][i] = -1;
            } else {
                fa[u][i] = fa[fa[u][i - 1]][i - 1];
            }
        }
        
        // ���ӽڵ����ջ
        for (int v : tree[u]) {
            if (!visited[v]) {
                stk.push({v, u});
            }
        }
    }
}

int lca(int u, int v) {
    if (comp_id[u] != comp_id[v]) {
        cerr << "Error: LCA query for nodes in different components: " << u << " " << v << endl;
        return -1;
    }
    
    if (depth[u] < depth[v]) swap(u, v);
    
    // ��u��������v��ͬ�����
    for (int i = LOGN - 1; i >= 0; --i) {
        if (fa[u][i] != -1 && depth[fa[u][i]] >= depth[v]) {
            u = fa[u][i];
        }
    }
    
    if (u == v) return u;
    
    // ͬʱ������Ծ
    for (int i = LOGN - 1; i >= 0; --i) {
        if (fa[u][i] != -1 && fa[v][i] != -1 && fa[u][i] != fa[v][i]) {
            u = fa[u][i];
            v = fa[v][i];
        }
    }
    
    return fa[u][0];
}

// �ǵݹ�DFSͳ��
int dfsSum_iterative(int start) {
    stack<pair<int, pair<int, int>>> stk; // (node, (parent, phase))
    // phase: 0=�½�, 1=����
    vector<int> subtree_sum(n, 0);
    
    stk.push({start, {-1, 0}});
    
    while (!stk.empty()) {
        auto [u, info] = stk.top();
        auto [p, phase] = info;
        
        if (phase == 0) {
            // �½��׶�
            stk.top().second.second = 1; // ���Ϊ�����׶�
            subtree_sum[u] = diff[u];
            
            // ��������ӽڵ�
            for (int v : tree[u]) {
                if (v != p) {
                    stk.push({v, {u, 0}});
                }
            }
        } else {
            // �����׶�
            stk.pop();
            
            // ͳ��������
            for (int v : tree[u]) {
                if (v != p) {
                    if (subtree_sum[v] == 0) {
                        res++; // ��(u,v)����
                    }
                    subtree_sum[u] += subtree_sum[v];
                }
            }
        }
    }
    
    return subtree_sum[start];
}

int main() {
    // ��ʼ��
    memset(fa, -1, sizeof(fa));
    memset(visited, false, sizeof(visited));
    memset(diff, 0, sizeof(diff));
    
    freopen("smallG.txt", "r", stdin);
    // freopen("mediumDG.txt", "r", stdin);
    // freopen("largeG.txt", "r", stdin);
    
    if (!cin) {
        cerr << "�޷��������ļ�" << endl;
        return 1;
    }
    
    cin >> n >> m;
    cout << "��ȡ�� " << n << " ����� " << m << " ���ߡ�" << endl;
    
    edges.resize(m);
    for (int i = 0; i < n; i++) {
        parent[i] = i;
    }
    
    for (int i = 0; i < m; i++) {
        int u, v;
        if (!(cin >> u >> v)) {
            cerr << "��ȡ�� " << i << " ʱ����" << endl;
            return 1;
        }
        edges[i] = {u, v};
    }
    cout << "��ɶ�ȡ��." << endl;

    // ===================
    // ��ʼ��ʱ
    // ===================
    auto start_time = high_resolution_clock::now();
    cout << "��ʼ�㷨ִ�У���ʱ��ʼ..." << endl;

    vector<pair<int, int>> nonTreeEdges;

    // ��������ɭ��
    cout << "��������ɭ��..." << endl;
    for (auto [u, v] : edges) {
        if (find(u) != find(v)) {
            unionSet(u, v);
            tree[u].push_back(v);
            tree[v].push_back(u);
        } else {
            nonTreeEdges.push_back({u, v});
        }
    }
    cout << "����������: " << nonTreeEdges.size() << endl;

    // ��ÿ����ͨ��������LCAԤ����
    cout << "������ͨ����..." << endl;
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            curr_comp++;
            comp_roots.push_back(i);
            dfs_iterative(i);
        }
    }
    cout << "��ͨ��������: " << curr_comp << endl;

    // ���ϲ�ֱ��
    int valid_non_tree_edges = 0;
    cout << "���������..." << endl;
    for (auto [u, v] : nonTreeEdges) {
        if (comp_id[u] != comp_id[v]) {
            cout << "������ (" << u << ", " << v << ") ���Ӳ�ͬ�ķ���!" << endl;
            continue;
        }
        
        int anc = lca(u, v);
        if (anc == -1) {
            cout << "����: LCA ʧ�ܣ��� (" << u << ", " << v << ")" << endl;
            continue;
        }
        
        diff[u]++;
        diff[v]++;
        diff[anc] -= 2;
        valid_non_tree_edges++;
    }
    cout << "��Ч����������: " << valid_non_tree_edges << endl;

    // ͳ���ŵ�����
    res = 0;
    cout << "ͳ���ŵ�����..." << endl;
    for (int root : comp_roots) {
        dfsSum_iterative(root);
    }

    cout << "��������: " << res << endl;

    // ===================
    // ������ʱ
    // ===================
    auto end_time = high_resolution_clock::now();
    
    auto duration_ms = duration_cast<milliseconds>(end_time - start_time);
    cout << "�㷨ִ��ʱ��: " << duration_ms.count() << " ����" << endl;
    return 0;
}