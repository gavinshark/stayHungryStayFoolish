function centroids = kMeansInitCentroids(X, K)
  %X-m*n
  %initial_centroids-K*n
  m = size(X,1);
  exist = 0;
  randidx = randperm(size(X, 1));
  centroids = X(randidx(1:K),:);
  
  end