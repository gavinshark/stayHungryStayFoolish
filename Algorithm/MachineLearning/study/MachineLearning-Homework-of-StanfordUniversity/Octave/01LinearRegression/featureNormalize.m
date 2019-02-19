function [X mu sigma] = featureNormalize(X)
  mu = mean(X)';
  sigma = std(X);
  X = (X-ones(size(X))*diag(mu))*(diag(1./sigma));  
end