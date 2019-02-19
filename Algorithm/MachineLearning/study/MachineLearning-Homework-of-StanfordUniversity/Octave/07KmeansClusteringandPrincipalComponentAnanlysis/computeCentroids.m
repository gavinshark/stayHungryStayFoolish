function centroids = computeCentroids(X, idx, K)
  %X-m*n
  %idx-m*1
  %centroids-k*n
  centroids = zeros(K,size(X,2));
  for i = 1:K
    findarray = find(idx==i);
    centroids(i,:) = sum(X(findarray,:),1)/size(findarray,1);
    end
  end