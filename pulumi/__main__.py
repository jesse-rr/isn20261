import pulumi
import pulumi_aws as aws

queue = aws.sqs.Queue("isn20261")

pulumi.export("queue_name", queue.name)
pulumi.export("queue_url", queue.url)
pulumi.export("queue_arn", queue.arn)
