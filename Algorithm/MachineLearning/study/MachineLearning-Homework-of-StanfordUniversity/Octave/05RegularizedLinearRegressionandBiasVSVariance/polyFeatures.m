function X_poly = polyFeatures(X, p)
  X_poly = zeros(size(X,1),p);
  for i = 1:p
    X_poly(:,i) = X.**i;
  end
  end