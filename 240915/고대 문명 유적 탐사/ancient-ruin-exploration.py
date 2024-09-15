from collections import deque

# 입력 받기
K, M = map(int, input().split())

# 그래프 크기 상수로 정의
N = 5  
graph = [list(map(int, input().split())) for _ in range(N)]
wall = list(map(int, input().split()))

# 상하좌우 방향 벡터
dxy = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# 유물(클러스터)의 개수를 찾는 함수
def search_treasure(graph_param):  
    visited = set()  # 리스트 대신 set 사용으로 탐색 속도 개선
    q = deque()
    result = 0
    for i in range(N):
        for j in range(N):
            cluster_size = 0  # 변수명 sum을 cluster_size로 변경 (내장 함수와 충돌 방지)
            if (i, j) not in visited:
                q.append((i, j))
                while q:
                    cx, cy = q.popleft()
                    num = graph_param[cx][cy]
                    for d in dxy:
                        nx, ny = cx + d[0], cy + d[1]
                        if 0 <= nx < N and 0 <= ny < N:
                            if graph_param[nx][ny] == num and (nx, ny) not in visited:
                                q.append((nx, ny))
                                visited.add((nx, ny))  # set을 사용하여 O(1)로 방문 확인 및 추가
                                cluster_size += 1
                if cluster_size >= 3:
                    result += cluster_size  # 클러스터 크기가 3 이상일 때만 결과에 더함
    return result

# 회전 및 탐색하는 함수
def rotate_and_count(ci, cj, angle):
    # 3x3 영역 추출
    si, sj = ci - 1, cj - 1
    mini_graph = [row[sj:sj+3] for row in graph[si:si+3]]  # 3x3 부분 추출
    
    # 각도에 따라 회전 처리
    if angle == 90:
        mini_graph = list(map(list, zip(*mini_graph[::-1])))
    elif angle == 180:
        mini_graph = [row[::-1] for row in mini_graph[::-1]]
    elif angle == 270:
        mini_graph = list(map(list, zip(*mini_graph)))[::-1]
    
    # 회전한 부분을 그래프에 반영
    new_graph = [row[:] for row in graph]  # 깊은 복사로 기존 그래프를 유지
    for i in range(3):
        for j in range(3):
            new_graph[si + i][sj + j] = mini_graph[i][j]

    # 회전 후 유물 개수 계산
    count = search_treasure(new_graph)
    return (ci, cj, angle, count)

# 실제 그래프를 회전시키는 함수
def rotate_graph(ci, cj, angle):
    # 3x3 영역 추출 및 회전 처리
    si, sj = ci - 1, cj - 1
    mini_graph = [row[sj:sj+3] for row in graph[si:si+3]]
    
    # 각도에 따라 회전 처리
    if angle == 90:
        mini_graph = list(map(list, zip(*mini_graph[::-1])))
    elif angle == 180:
        mini_graph = [row[::-1] for row in mini_graph[::-1]]
    elif angle == 270:
        mini_graph = list(map(list, zip(*mini_graph)))[::-1]
    
    # 회전한 부분을 실제 그래프에 반영
    for i in range(3):
        for j in range(3):
            graph[si + i][sj + j] = mini_graph[i][j]

# 유물을 제거하는 함수
def remove_treasure():
    treasure_spot = []
    visited = set()  # 방문 여부 체크에 set 사용
    q = deque()
    
    for i in range(N):
        for j in range(N):
            cluster_size = 0
            treasure = []  # 클러스터 좌표 저장
            if (i, j) not in visited:
                q.append((i, j))
                while q:
                    cx, cy = q.popleft()
                    num = graph[cx][cy]
                    for d in dxy:
                        nx, ny = cx + d[0], cy + d[1]
                        if 0 <= nx < N and 0 <= ny < N:
                            if graph[nx][ny] == num and (nx, ny) not in visited:
                                q.append((nx, ny))
                                visited.add((nx, ny))  # set 사용으로 방문 처리
                                cluster_size += 1
                                treasure.append((nx, ny))  # 클러스터 좌표 저장
                if cluster_size >= 3:
                    treasure_spot.extend(treasure)  # 유물 좌표를 결과에 추가

    return treasure_spot  # 유물 좌표 반환

# 게임 진행 로직
rs = []
for _ in range(K):  
    rsum = 0  # 한 턴 동안 모은 유물 개수 합계
    cases = []
    
    # 3x3 회전 가능한 모든 중심점(ci, cj)에 대해 회전 처리
    for ci in range(1, 4):
        for cj in range(1, 4):
            cases.append(rotate_and_count(ci, cj, 90))
            cases.append(rotate_and_count(ci, cj, 180))
            cases.append(rotate_and_count(ci, cj, 270))
    
    # 회전 후 유물 개수가 최대인 경우 선택
    max_case = sorted(cases, key=lambda x: (-x[3], x[2], x[1], x[0]))[0]
    
    # 선택된 회전으로 실제 그래프 업데이트
    rotate_graph(max_case[0], max_case[1], max_case[2])
    
    # 유물 제거 후 유적 개수 더하기
    treasure_spot = remove_treasure()
    rsum += len(treasure_spot)
    
    # 유적 좌표에 벽 값 업데이트
    treasure_spot = sorted(treasure_spot, key=lambda x: (x[1], -x[0]))  # 좌표 정렬
    for ts in treasure_spot:
        graph[ts[0]][ts[1]] = wall.pop(0)  # 벽 값으로 유물 좌표 업데이트
    
    # 연쇄적으로 남은 유물 탐색 및 제거
    while True:
        left_treasure_spot = remove_treasure()
        if not left_treasure_spot:
            break
        left_treasure_spot = sorted(left_treasure_spot, key=lambda x: (x[1], -x[0]))
        for ts in left_treasure_spot:
            graph[ts[0]][ts[1]] = wall.pop(0)
        rsum += len(left_treasure_spot)
    
    if rsum == 0:  # 모은 유물이 없으면 종료
        break
    
    rs.append(rsum)  # 턴당 모은 유물 개수 저장

# 결과 출력
print(*rs)

'''
1. visited 리스트 대신 set 사용
visited를 리스트로 구현하면 확인할 때 O(n)의 시간이 걸리기 때문에, 이를 set으로 바꾸면 O(1)로 탐색 속도를 줄일 수 있습니다. set을 사용하면 중복 체크도 쉽게 처리할 수 있습니다.
visited = set()
그리고 visited.append() 대신 visited.add()로 수정하면 됩니다.

2. sum 변수 명 변경
sum은 파이썬의 내장 함수로도 사용되므로, 이를 다른 변수명으로 바꾸는 것이 좋습니다. 예를 들어 cluster_size처럼 의미를 더 잘 나타내는 변수명을 사용할 수 있습니다.
cluster_size = 0

3. DFS 또는 BFS 탐색 구조 개선
현재 BFS 구조가 잘 작동하고 있지만, 
탐색할 때마다 visited에 방문 여부를 여러 번 확인하고 추가하는 로직이 반복되고 있습니다. 
이를 하나의 함수로 분리하면 코드가 더 깔끔해질 수 있습니다. 
예를 들어, 유사한 논리가 반복되는 부분을 함수화하여 중복을 줄일 수 있습니다.

4. 벽 값 업데이트 로직 간소화
wall 리스트를 deque로 변환하고, 남은 벽들을 다시 리스트로 변환하는 부분을 좀 더 간결하게 할 수 있습니다. 
예를 들어, deque를 사용하는 부분을 최소화하고 리스트 슬라이싱 등을 활용할 수 있습니다.
for ts in treasure_spot:
    graph[ts[0]][ts[1]] = wall.pop(0)

5. 매직 넘버 5 제거
현재 5라는 숫자가 여러 곳에서 사용되고 있는데, 이 숫자를 상수로 정의하면 더 유연한 코드가 될 수 있습니다.
N = 5
graph = [list(map(int, input().split())) for _ in range(N)]

6. 불필요한 new_graph 생성 제거
rotate_graph 함수에서 new_graph를 계속 새로 생성하고 있는데, 이 부분을 기존 graph에 직접 변경하도록 바꿀 수 있습니다. 
불필요하게 새로운 그래프를 생성하는 것은 메모리와 성능 측면에서 비효율적일 수 있습니다.

7. 중복된 코드 제거
rotate_graph와 get_count_by_angle 함수에서 회전 로직이 중복되어 있습니다. 
이 부분을 하나의 함수로 통합하여 코드 중복을 줄일 수 있습니다.
'''