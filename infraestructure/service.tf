resource "aws_ecs_service" "flask_service" {
  name            = "flask-service"
  cluster         = aws_ecs_cluster.flask_cluster.id
  task_definition = aws_ecs_task_definition.flask_task.arn
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = ["subnet-031b0320f778b9b3f"] 
    security_groups = [aws_security_group.flask_sg.id]
    assign_public_ip = true
  }
  desired_count = 1
}
