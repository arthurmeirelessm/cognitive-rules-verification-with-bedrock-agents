resource "aws_ecs_task_definition" "flask_task" {
  family                   = "flask-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn 
  task_role_arn            = aws_iam_role.ecs_permissions_role.arn  

  container_definitions = jsonencode([
    {
      name      = "flask-app"
      image     = "552516487395.dkr.ecr.us-east-1.amazonaws.com/flask-fargate-app-repo:latest"
      cpu       = 256
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
        }
      ]
    }
  ])
}
