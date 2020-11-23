RANDOM_SEED = 17521056
def init(num_values, search_domain, N = 32, random_seed = RANDOM_SEED):
    np.random.seed(random_seed)
    return np.random.uniform(search_domain[0],search_domain[1],(N,num_values))
def ring(num_values, function, search_domain, N = 32, random_seed = RANDOM_SEED, G = 50):
    count = 0
    particles = init(num_values, search_domain, N, random_seed)
    results = [particles.copy()]
    # vị trí tốt nhất mà phần tử đó đã đạt được trong quá khứ
    pBest = [None]*N
    yBest = np.zeros((N,num_values))
    
    # vị trí tốt nhất mà cả cụm đạt được trong quá khứ
    gBest = [1e+100]*N
    zBest = [None]*N
    
    # Khởi tạo vị trí trong lần lặp đầu tiên
    for i in range(N):
        count += 1
        pBest[i] = function(particles[i])
        yBest[i] = particles[i]
    
    # Tìm vị trí tôt nhất trong K phần tử lân cận
    for i in range(N - 1):
        
        # Tìm giá trị nhỏ nhất trong k phần tử
        local_min = min(pBest[i-1],pBest[i],pBest[i+1])
        
        if gBest[i] > local_min:
        
            # Lưu lại giá trị nhỏ nhất
            gBest[i] = local_min

            # Lưu lại vị trí tốt nhất
            min_id = np.argmin([pBest[i-1],pBest[i],pBest[i+1]]) - 1
            zBest[i] = yBest[i + min_id]
            
    # Phần tử cuối của mảng
    local_min = min(pBest[N-2],pBest[N-1],pBest[0])
    if gBest[-1] > local_min:
        gBest[-1] = local_min
        
        # Lấy min_id
        min_id = np.argmin([pBest[N-2],pBest[N-1],pBest[0]])
        zBest[-1] = yBest[-min_id]

    # Tìm vector hiện tại tốt nhất của mỗi particle: V[i] = pos[i] - pos_bestest_k[i]
    V = particles - np.array(zBest)
    if num_values == 2:
        repeat = 1
        while(repeat < G):
            for i in range(N):
                r1, r2 = np.random.uniform(0,1,(2, num_values))
                # cognitive component
                cogn = c1*r1*(yBest[i] - particles[i])
                # social component
                social = c2*r2*(zBest[i] - particles[i])
                # Update V[i]
                V[i] = w*V[i] + cogn + social
                # Update position
                particles[i] += V[i]

                # Check giá trị của mỗi vị trí trong search domain
                for j in range(num_values):
                    if particles[i][j] > search_domain[1]:
                        particles[i][j] = search_domain[1] - np.random.uniform(0,.01)
                    elif particles[i][j] < search_domain[0]:
                        particles[i][j] = search_domain[0] + np.random.uniform(0,.01)

            # Lặp
            for i in range(N):
                if function(particles[i]) < pBest[i]:
                    pBest[i] = function(particles[i])
                    yBest[i] = particles[i]

            # Tìm vị trí tôt nhất trong K phần tử lân cận

            for i in range(N - 1):
                # Tìm giá trị nhỏ nhất trong k phần tử
                local_min = min(pBest[i-1],pBest[i],pBest[i+1])
                if gBest[i] > local_min:

                    # Lưu lại giá trị nhỏ nhất
                    gBest[i] = local_min

                    # Lưu lại vị trí tốt nhất
                    min_id = np.argmin([pBest[i-1],pBest[i],pBest[i+1]]) - 1
                    zBest[i] = yBest[i + min_id]

            # Phần tử cuối của mảng
            local_min = min(pBest[N-2],pBest[N-1],pBest[0])
            if gBest[-1] > local_min:
                gBest[-1] = local_min

                # Lấy min_id
                min_id = np.argmin([pBest[N-2],pBest[N-1],pBest[0]])
                zBest[-1] = yBest[-min_id]
            repeat+=1
            results.append(particles.copy())
        else:
            while(count != 1000000):
                for i in range(N):
                    r1, r2 = np.random.uniform(0,1,(2, num_values))
                    # cognitive component
                    cogn = c1*r1*(yBest[i] - particles[i])
                    # social component
                    social = c2*r2*(zBest[i] - particles[i])
                    # Update V[i]
                    V[i] = w*V[i] + cogn + social
                    # Update position
                    particles[i] += V[i]

                    # Check giá trị của mỗi vị trí trong search domain
                    for j in range(num_values):
                        if particles[i][j] > search_domain[1]:
                            particles[i][j] = search_domain[1] - np.random.uniform(0,.01)
                        elif particles[i][j] < search_domain[0]:
                            particles[i][j] = search_domain[0] + np.random.uniform(0,.01)

                # Lặp
                for i in range(N):
                    if count == 1000000:
                        break
                    count += 1
                    if function(particles[i]) < pBest[i]:
                        pBest[i] = function(particles[i])
                        yBest[i] = particles[i]

                # Tìm vị trí tôt nhất trong K phần tử lân cận

                for i in range(N - 1):
                    # Tìm giá trị nhỏ nhất trong k phần tử
                    local_min = min(pBest[i-1],pBest[i],pBest[i+1])
                    if gBest[i] > local_min:

                        # Lưu lại giá trị nhỏ nhất
                        gBest[i] = local_min

                        # Lưu lại vị trí tốt nhất
                        min_id = np.argmin([pBest[i-1],pBest[i],pBest[i+1]]) - 1
                        zBest[i] = yBest[i + min_id]

                # Phần tử cuối của mảng
                local_min = min(pBest[N-2],pBest[N-1],pBest[0])
                if gBest[-1] > local_min:
                    gBest[-1] = local_min

                    # Lấy min_id
                    min_id = np.argmin([pBest[N-2],pBest[N-1],pBest[0]])
                    zBest[-1] = yBest[-min_id]
                results.append(particles.copy())
    index = np.argmin(gBest)
    return results, gBest[index], zBest[i]



def star(num_values, function, search_domain, N = 32, random_seed = RANDOM_SEED, G = 50):
    particles = init(num_values, search_domain, N, random_seed)
    results = [particles.copy()]
    # vị trí tốt nhất mà phần tử đó đã đạt được trong quá khứ
    pBest = [1e+100]*N
    yBest = np.zeros((N,num_values))

    # vị trí tốt nhất mà cả bầy đàn đã đạt được trong quá khứ
    gBest = 1e+100
    zBest = None

    # Khởi Tìm vị trí tốt nhất trong lần lặp đầu tiên
    count = 0
    for i, particle in enumerate(particles):
        count += 1
        if function(particle) < pBest[i]:
            pBest[i] = function(particle)
            yBest[i] = particle
            if pBest[i] < gBest:
                gBest = pBest[i]
                zBest = yBest[i]
    # Find the current velocity vector of particle i
    V = particles - zBest
    repeat = 1
    if num_values == 2:
        while(repeat <=50):
            for i in range(N):
                # random r1, r2
                r1, r2 = np.random.uniform(0, 1,(2, num_values))
                # cognitive component
                cogn = c1*r1*(yBest[i] - particles[i])
                # social component
                social = c2*r2*(zBest - particles[i])

                # update V[i]
                V[i] = w*V[i] + cogn + social
                # Update position
                particles[i] += V[i]
                for j in range(num_values):
                    if particles[i][j] > search_domain[1]:
                        particles[i][j] = search_domain[1] - np.random.uniform(0,0.01)

                    if particles[i][j] < search_domain[0]:
                        particles[i][j] = search_domain[0] + np.random.uniform(0,0.01)

            for i in range(N):
                if function(particles[i]) < pBest[i]:
                    pBest[i] = function(particles[i])
                    yBest[i] = particles[i]
                    if pBest[i] < gBest:
                        gBest = pBest[i]
                        zBest = yBest[i]
            repeat += 1
            temp = particles.copy()
            results.append(temp)
    else:
        while(count != 1000000):
            for i in range(N):
                # random r1, r2
                r1, r2 = np.random.uniform(0, 1,(2, num_values))
                # cognitive component
                cogn = c1*r1*(yBest[i] - particles[i])
                # social component
                social = c2*r2*(zBest - particles[i])

                # update V[i]
                V[i] = w*V[i] + cogn + social
                # Update position
                particles[i] += V[i]
                for j in range(num_values):
                    if particles[i][j] > search_domain[1]:
                        particles[i][j] = search_domain[1] - np.random.uniform(0,0.01)

                    if particles[i][j] < search_domain[0]:
                        particles[i][j] = search_domain[0] + np.random.uniform(0,0.01)

            for i in range(N):
                if count != 1000000:
                    count += 1
                break
                if function(particles[i]) < pBest[i]:
                    pBest[i] = function(particles[i])
                    yBest[i] = particles[i]
                    if pBest[i] < gBest:
                        gBest = pBest[i]
                        zBest = yBest[i]
            repeat += 1
            temp = particles.copy()
            results.append(temp)
                
    return results , gBest, zBest