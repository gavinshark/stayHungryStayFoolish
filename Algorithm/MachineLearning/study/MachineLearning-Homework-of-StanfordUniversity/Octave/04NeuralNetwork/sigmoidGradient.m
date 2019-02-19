function y = sigmoidGradient(x)
  tmp = sigmoid(x);
  y = tmp.*(1-tmp);
  end