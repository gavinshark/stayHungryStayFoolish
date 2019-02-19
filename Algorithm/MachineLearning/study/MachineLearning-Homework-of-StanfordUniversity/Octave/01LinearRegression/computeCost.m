function cost = computeCost(X, y, theta)
  costArray = X*theta - y;
  cost = sum((costArray).^2)/length(y)/2;
  end