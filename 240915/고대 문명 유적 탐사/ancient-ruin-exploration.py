from collections import deque

K, M = map(int, input().split())

graph = [list(map(int, input().split())) for i in range(5)]
wall = list(map(int, input().split()))

dxy = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상하좌우


def search_treasure(graph_param):  # 유물 개수 찾기
    visited = []
    q = deque()
    result = 0
    for i in range(5):
        for j in range(5):
            sum = 0
            if (i, j) not in visited:
                q.append((i, j))
                while q:
                    cx, cy = q.popleft()
                    num = graph_param[cx][cy]
                    for d in dxy:
                        nx, ny = cx + d[0], cy + d[1]
                        if 0 <= nx < 5 and 0 <= ny < 5:
                            if graph_param[nx][ny] == num and (nx, ny) not in visited:
                                q.append((nx, ny))
                                visited.append((nx, ny))
                                sum += 1
                if sum >= 3:
                    result += sum

    return result


def get_count_by_angle(ci, cj, angle):
    # (ci, cj) 기준으로 angle 만큼 회전하기. 3*3만 회전 해야 함
    si, sj = ci - 1, cj - 1
    mini_graph = []
    for i in range(3):
        tmp = []
        for j in range(3):
            tmp.append(graph[si + i][sj + j])
        mini_graph.append(tmp)

    if angle == 90:
        tmp_graph = list(map(list, zip(*mini_graph[::-1])))
    elif angle == 180:
        tmp_graph = [a[::-1] for a in mini_graph[::-1]]
    else:
        tmp_graph = [x[::-1] for x in list(map(list, zip(*mini_graph[::-1])))[::-1]]

    # 3*3인걸로 업데이트 하기

    # 주의 : 이렇게 하면 그래프의 값까지 바뀐다. new_graph = graph
    new_graph = [[0] * 5 for _ in range(5)]
    for x in range(5):
        for y in range(5):
            new_graph[x][y] = graph[x][y]

    for i in range(3):
        for j in range(3):
            new_graph[si + i][sj + j] = tmp_graph[i][j]

    count = search_treasure(new_graph)

    return (ci, cj, angle, count)
    # return 0

def rotate_graph(ci, cj, angle):
    # (ci, cj) 기준으로 angle 만큼 회전하기. 3*3만 회전 해야 함
    si, sj = ci - 1, cj - 1
    mini_graph = []
    for i in range(3):
        tmp = []
        for j in range(3):
            tmp.append(graph[si + i][sj + j])
        mini_graph.append(tmp)

    if angle == 90:
        tmp_graph = list(map(list, zip(*mini_graph[::-1])))
    elif angle == 180:
        tmp_graph = [a[::-1] for a in mini_graph[::-1]]
    else:
        tmp_graph = [x[::-1] for x in list(map(list, zip(*mini_graph[::-1])))[::-1]]

    # 3*3인걸로 업데이트 하기

    # 이렇게 하면 그래프의 값까지 바뀐다. new_graph = graph
    new_graph = [[0] * 5 for _ in range(5)]
    for x in range(5):
        for y in range(5):
            new_graph[x][y] = graph[x][y]

    for i in range(3):
        for j in range(3):
            new_graph[si + i][sj + j] = tmp_graph[i][j]

    return new_graph


def remove_treasure():
    treasure_spot =[]
    visited = []
    q = deque()
    result = 0
    for i in range(5):
        for j in range(5):
            sum = 0
            treasure = []
            if (i, j) not in visited:
                q.append((i, j))
                while q:
                    cx, cy = q.popleft()
                    num = graph[cx][cy]
                    for d in dxy:
                        nx, ny = cx + d[0], cy + d[1]
                        if 0 <= nx < 5 and 0 <= ny < 5:
                            if graph[nx][ny] == num and (nx, ny) not in visited:
                                q.append((nx, ny))
                                visited.append((nx, ny))
                                sum += 1
                                treasure.append((nx, ny))
                if sum >= 3:
                    result += sum
                    for t in treasure:
                        treasure_spot.append((t[0], t[1]))

    return treasure_spot


rs = []
# K 턴 마다 무조건 회전해야 함
for _ in range(K):  
    rsum = 0
    cases = []
    # 중심점(2,2) 하나로 함수를 테스트 : get_count_by_angle(2, 2, 90)

    for ci in range(1, 4):
        for cj in range(1, 4):
            # ci, cj 를 기준으로 회전하기
            cases.append(get_count_by_angle(ci, cj, 90))
            cases.append(get_count_by_angle(ci, cj, 180))
            cases.append(get_count_by_angle(ci, cj, 270))

    # 최대 케이스 찾기
    max_case = sorted(cases, key=lambda x: (-x[3], x[2], x[1], x[0]))[0]

    # 최대일 때 그래프
    graph = rotate_graph(max_case[0], max_case[1], max_case[2])
    
    # 유적 좌표 구하기
    treasure_spot = remove_treasure()
    # 유적 개수 더하기
    rsum += len(treasure_spot)
    # 유적 좌표에 벽 값 업데이트
    treasure_spot = sorted(treasure_spot, key=lambda x: (x[1], -x[0]))
    wq = deque(wall)
    for ts in treasure_spot:
        graph[ts[0]][ts[1]] = wq.popleft()
    wall = list(wq)

    # 연쇄 탐색하기
    while True:
        left_treasure_spot = remove_treasure()
        if len(left_treasure_spot) == 0:
            break
        left_treasure_spot = sorted(left_treasure_spot, key=lambda x: (x[1], -x[0]))
        wq = deque(wall)
        for ts in left_treasure_spot:
            graph[ts[0]][ts[1]] = wq.popleft()
        wall = list(wq)
        rsum += len(left_treasure_spot)
    if rsum == 0:
        break
    rs.append(rsum)
print(*rs)