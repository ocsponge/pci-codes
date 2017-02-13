1.第13页 if n==0: return 1 错误，英文原版为return 0
2.第17页 recommendations.getRecommendations(recommendations.critics,'Toby',similarity=sim_distance) 的计算结果有误，这里是因为书中源代码有误，
  sim_distance函数计算返回值 1/(1+sqrt(sum_of_squares) 源代码误写为 1/(1+sum_of_squares)
