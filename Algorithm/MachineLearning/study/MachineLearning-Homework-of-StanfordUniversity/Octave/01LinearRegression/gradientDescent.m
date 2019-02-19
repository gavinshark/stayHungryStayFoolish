function [thetaest Jhistory] = gradientDescent(X, y, theta, alpha, iterations)
  Jhistory = zeros(1, iterations);
  for index = 1:1:iterations
    weightmatrix = X'*(X*theta - y);
    theta = theta - alpha./length(y).*(weightmatrix);
    Jhistory(index) = computeCost(X,y,theta);
  end    
    thetaest = theta;
end