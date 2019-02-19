function [J, grad] = lrCostFunction ( X, y, theta, lambda)
  % X : m*(20*20+1)
  % theta: (400+1)*1
  % y:m*1
  m = size(X,1);
  xtheta = X*theta;%m*1
  logXtheta = sigmoid(xtheta);%m*1
  minuslogXtheta = sigmoid(1-xtheta);%m*1
  J = -1/m*sum(y.*logXtheta .+ (1-y).*minuslogXtheta);
  J = J + lambda/m*(sum(theta(2:end).^2));%1*1
  beta = logXtheta - y;%m*1
  grad = X'*beta/m + lambda/m*[0;theta(2:end,1)];%400*1
 end