function [cost, grad] = costFunction(theta, X, y)
  hX = sigmoid(X*theta);
  m=length(y);
  cost = -1/m*( y'*log(hX) + (1-y')*log(1-hX)); %1X1
  grad = 1/m*(hX-y)'*X;   %1XN
end