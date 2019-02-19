function Theta = randInitializeWeights(Lin, Lout)
  epsilon_init = sqrt(6)/(sqrt(Lin+Lout)+ eps);
  Theta = rand(Lout, 1+Lin)*2*epsilon_init - epsilon_init;
  end