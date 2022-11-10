# peer-review-averages

This script uploads the average score to an assignment on Canvas.

```sh
python3 peer-grading/peer_review_average.py -t [CANVAS_AUTH_TOKEN] -c 1518980 -a 8475255
```

## Giving Credit For Doing Peer Reviews

Ensure the following are set -- use the above command:

```py
DRY_RUN = False
# Give students credit for completing per reviews
UPLOAD_SCORES_FOR_COMPLETION = True
completion_assignment_id = 8506682
POINTS_PER_REVIEW = 2
```
