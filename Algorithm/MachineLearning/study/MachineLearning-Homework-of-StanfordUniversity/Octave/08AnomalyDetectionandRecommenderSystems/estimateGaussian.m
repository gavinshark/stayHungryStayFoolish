function [mu sigma2] = estimateGaussian(X)
  %X-m*n; 
  mu = mean(X,1);
  m = size(X,1);
  sigma2 = zeros(size(X,2),1);
  for i = 1:size(X,2)
    x_tmp = X(:,i);
    sigma2(i) = 1/m*sum((x_tmp-mu(i)).^2);
  end
  end