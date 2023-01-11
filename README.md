
# AWS DeepRacer Reward Function

I participated in the "Invent 2018" contest of DeepRacer Virtual Circuit.

It is a reward function at that time.
The lap time was about 8.464 seconds after repeated training.

## Environment simulation

- re:Invent 2018 Training

## Action space

| Action space                 | Value       |
|------------------------------|-------------|
| Maximum steering angle       | 30&deg;     |
| Maximum speed                | 2.4 m/s     |
| 0&deg;                       | 2.4 m/s     |
| 14&deg;                      | 1.6 m/s     |
| 20&deg;                      | 1.6 m/s     |
| 21&deg;                      | 1.7 m/s     |
| 25&deg;                      | 1.7 m/s     |
| 30&deg;                      | 1   m/s     |
| -10&deg;                     | 1.9 m/s     |
| -20&deg;                     | 1.5 m/s     |
| -30&deg;                     | 1.6 m/s     |

## Hyperparameters

| Hyperparameters                                                | Value           |
|----------------------------------------------------------------|-----------------|
| Gradient Descent Batch Size                                    | 32              |
| Entropy                                                        | 0.01            |
| Discount Factor                                                | 0.999           |
| Loss Type                                                      | Huber           |
| Learning Rate                                                  | 0.00006         |
| No# Experience Episodes between each policy-updating iteration | 20              |
| No# of Epochs                                                  | 3               |

## Stop conditions

- 30 or 60 mins

## Reference

- https://docs.aws.amazon.com/zh_tw/deepracer/latest/developerguide/deepracer-reward-function-input.html
- https://forums.aws.amazon.com/forum.jspa?forumID=318
- https://github.com/aws-samples/aws-deepracer-workshops
- https://github.com/sasasavic82/deeracer-reward
- https://qiita.com/kai_kou/items/8a45c687baca8c9465f6
- https://qiita.com/Alt_Shift_N/items/2c37fbb26d739b7f3046