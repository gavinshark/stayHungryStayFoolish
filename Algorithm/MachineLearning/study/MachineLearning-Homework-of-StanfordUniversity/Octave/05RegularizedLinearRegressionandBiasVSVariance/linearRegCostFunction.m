function [J grad] = linearRegCostFunction(X, y, theta, lambda)
  %X-m*2
  %y-m*1
  %theta 2*1  
  m =  size(X,1);
  J=1/2/m*sum((X*theta-y).^2)+lambda/2/m*sum(theta(2:end).^2);
  
  grad = sum(diag(X*theta-y)*X/m,1)'; %1*2
  grad = grad + lambda/m*[0;theta(2:end)];
  end