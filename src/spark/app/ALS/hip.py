from pyspark.mllib.recommendation import ALS
import math

num_iterations = 5
ranks = [8, 10, 12, 14]
reg_params = [0.001, 0.01, 0.05]

def generateBestModel(data_train, data_val) -> any:
  err_ = float('inf')
  rank_ = -1
  reg_ = 0
  model_ = None

  for rank in ranks:
    for reg in reg_params:
      tmp_model = ALS.train(
        ratings=data_train,
        iterations=num_iterations,
        rank=rank,
        lambda_=reg,
        seed=99
      )

      val_data = data_val.map(lambda p: [p[0], p[1]])
      predict = tmp_model.predictAll(
        val_data).map(lambda r: ((r[0], r[1]), r[2]))
      
      _pred = data_val.map(lambda r: ((r[0], r[1]), r[2])).join(predict)
      tmp_err_rmse = math.sqrt(_pred.map(lambda r: (r[1][0] - r[1][1]) ** 2).mean())
      print('RANK {}, REGULARIZATION {} RMSE {}'.format(rank, reg, tmp_err_rmse))
      if tmp_err_rmse < err_:
        err_ = tmp_err_rmse
        rank_ = rank
        reg_ = reg
        model_ = tmp_model

  print('\n BEST MODEL: RANK = {}, REG = {}'.format(rank_, reg_))
  return model_
        