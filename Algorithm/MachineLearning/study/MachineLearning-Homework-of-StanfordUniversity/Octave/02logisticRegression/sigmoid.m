function [A] = sigmoid(X)
  A = 1./(exp(-X) + 1);
  end