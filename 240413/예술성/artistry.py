N=int(input())
arr=[list(map(int, input().split())) for _ in range(N)]
M=N//2

from collections import deque
def bfs(si,sj):
    q = deque()

    q.append((si,sj))
    v[si][sj]=1
    groups[-1].add((si,sj))     # 새 좌표를 그룹에 추가

    while q:
        ci,cj = q.popleft()
        for ni,nj in ((ci-1,cj),(ci+1,cj),(ci,cj-1),(ci,cj+1)):
            # 네방향, 범위내, 미방문, 조건: 같은 값이면
            if 0<=ni<N and 0<=nj<N and v[ni][nj]==0 and arr[ci][cj]==arr[ni][nj]:
                q.append((ni,nj))
                v[ni][nj]=1
                groups[-1].add((ni,nj))

ans=0
for k in range(4):
    # [1] 예술점수 구하기: 그룹나누고, 가능한 두 개 그룹의 점수 누적
    groups = []
    nums = []
    # [1-1] 미방문 숫자를 만나면 BFS(): 같은그룹 좌표를 set에 추가
    v = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if v[i][j]==0:  # 미방문
                groups.append(set())
                nums.append(arr[i][j])
                bfs(i,j)

    # [1-2] 각 그룹간 점수 계산(누적)
    CNT = len(nums)
    for i in range(0,CNT-1):
        for j in range(i+1, CNT):   # CNT개에서 2개 뽑는 가능한 모든 조합
            point = (len(groups[i])+len(groups[j]))*nums[i]*nums[j]  # 인접면 1개당 더해질 점수
            for ci,cj in groups[i]:
                for ni,nj in ((ci-1,cj),(ci+1,cj),(ci,cj-1),(ci,cj+1)):
                    if (ni,nj) in groups[j]:    # 인접한 좌표가 그룹j에 있다면 두 그룹은 인접
                        ans+=point

    if k==3:
        break
    # [2] 회전시키기: '+'반시계 회전, 부분사각형 시계방향
    narr = [[0]*N for _ in range(N)]
    for i in range(N):              # '+' 부분 시계
        narr[M][i]=arr[i][M]
    for j in range(N):
        narr[j][M]=arr[M][N-j-1]

    for (si,sj) in ((0,0),(0,M+1),(M+1,0),(M+1,M+1)):
        for i in range(M):
            for j in range(M):
                narr[si+i][sj+j]=arr[si+M-j-1][sj+i]
    arr = narr

print(ans)