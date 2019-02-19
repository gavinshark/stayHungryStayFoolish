function [pred] = predict(Theta1, Theta2, x)
  x = [ones(size(x,1),1) x];
  a2 = sigmoid(x*Theta1');
  a2 = [ones(size(a2,1),1) a2];
  a3 = sigmoid(a2*Theta2');
  [aa,pred]=max(a3,[],2);  
  end