#!/bin/bash

TAG=$1
REPO=$2
AWS_REGION=$3
APP_NAME=$4
ECS_SERVICE=$5

ECS_CLUSTER="$APP_NAME-cluster"
TASK_FAMILY="$APP_NAME-task"
NEW_IMAGE="$REPO:$TAG"

# 1. Describe the current task definition to get the current container definition
CURRENT_TASK_DEFINITION=$(aws ecs describe-task-definition --task-definition "$TASK_FAMILY" --region "$AWS_REGION" --output json)

# 2. Extract the container definitions and replace the old image with the new image
TASK_DEFINITION_JSON=$(echo "$CURRENT_TASK_DEFINITION" | jq --arg NEW_IMAGE "$NEW_IMAGE" '.taskDefinition
    | .containerDefinitions[0].image=$NEW_IMAGE
    | del(
        .taskDefinitionArn,
        .revision,
        .status,
        .requiresAttributes,
        .compatibilities,
        .registeredAt,
        .registeredBy
    )')

# 3. Register a new revision of the task definition with the updated image - CREATE A NEW REVISION
NEW_TASK_DEFINITION=$(aws ecs register-task-definition --cli-input-json "$TASK_DEFINITION_JSON" --region "$AWS_REGION")

# 4. Extract the new task definition ARN
NEW_TASK_DEFINITION_ARN=$(echo "$NEW_TASK_DEFINITION" | jq -r '.taskDefinition.taskDefinitionArn')

# 5. Update the ECS service to use the new task definition revision
aws ecs update-service --cluster "$ECS_CLUSTER" --service "$ECS_SERVICE" --task-definition "$NEW_TASK_DEFINITION_ARN" --force-new-deployment --region "$AWS_REGION"
