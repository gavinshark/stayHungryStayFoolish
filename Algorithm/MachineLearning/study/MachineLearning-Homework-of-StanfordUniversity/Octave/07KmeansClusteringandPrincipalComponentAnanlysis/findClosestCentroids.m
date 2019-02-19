function idx = findClosestCentroids(X, initial_centroids)
  %X-m*n
  %initial_centroids-k*n  
  m = size(X,1);
  k = size(initial_centroids, 1);
  idx = zeros(m,1);
  for i = 1:m
    x_array = X(i, :); %1*n
    X_matrix = repmat(x_array, k, 1); %k*n
    X_diff = sum((X_matrix-initial_centroids).^2, 2);%k*n
    [minval minidx] = min(X_diff);
    idx(i) = minidx;
    end
  end