function [J grad] = nnCostFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y, lambda)
 Theta1 = reshape(nn_params(1:hidden_layer_size*(input_layer_size + 1)), hidden_layer_size,[]);%25 * 401
 Theta2 = reshape(nn_params(1+hidden_layer_size*(input_layer_size + 1):end), num_labels,[]);% 10 * 26
 m = size(X, 1);
 
 Y = zeros(m, num_labels); % m* 10
 E = eye(num_labels);
 for i = 1:num_labels
   Y0 = find(y == i);
   Y(Y0,:) = repmat(E(i,:),size(Y0,1),1);
 end
  
 J=0;
 X = [ones(m, 1) X]; % m*401
 a2 = sigmoid(X * Theta1'); % m*25
 a2 = [ones(m, 1) a2]; %m * 26
 a3 = sigmoid(a2 * Theta2'); % m* 10
 
 J = sum(sum(-Y.*log(a3)-(1-Y).*log(1-a3)))/m;
 ThetaMetricWeight = lambda/m/2*(sum(sum(Theta1(:,2:end).^2)) + sum(sum(Theta2(:,2:end).^2)));
 J = J + ThetaMetricWeight;
 
 delta_1 = zeros(size(Theta1));
 delta_2 = zeros(size(Theta2));
 err_3 = zeros(num_labels,1);
 for t =1:m
   %step1
   a_1 = X(t,:)'; %1*401
   z_2 = Theta1*a_1;%25*1
   a_2 = [1;sigmoid(z_2)];%26*1
   z_3 = Theta2*a_2;%10*1
   a_3 = sigmoid(z_3);
   %step2
   for k = 1:num_labels
     err_3(k) = a_3(k) - (y(t)==k); %10*1
   end
   %step3
   err_2 = Theta2' * err_3; %26*1
   err_2 = err_2(2:end).*sigmoidGradient(z_2); %25*1
   %step4
   delta_2 = delta_2 + err_3 * a_2';  %10*26
   delta_1 = delta_1 + err_2 * a_1';  %25*401
  end
  
  Theta1_delta = delta_1/m + [zeros(hidden_layer_size,1) Theta1(:,2:end)]*lambda/m;
  Theta2_delta = delta_2/m + [zeros(num_labels,1) Theta2(:,2:end)]*lambda/m;
  
  grad = [Theta1_delta(:);Theta2_delta(:)]; 
 
end
