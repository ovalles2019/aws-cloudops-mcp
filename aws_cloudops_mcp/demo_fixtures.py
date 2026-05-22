"""Synthetic AWS inventory for public portfolio demos (no boto3 calls)."""

from __future__ import annotations

from typing import Any


def dashboard_payload() -> dict[str, Any]:
    whoami = {
        "ok": True,
        "region": "us-east-1",
        "account": "111122223333",
        "arn": "arn:aws:iam::111122223333:role/demo-cloudops-readonly",
        "user_id": "AROAEXAMPLE:demo-cloudops-readonly",
        "demo": True,
    }
    instances = [
        {
            "InstanceId": "i-0a1b2c3d4e5f67890",
            "InstanceType": "t3.medium",
            "State": "running",
            "AvailabilityZone": "us-east-1a",
            "PrivateIpAddress": "10.0.1.42",
            "PublicIpAddress": None,
            "LaunchTime": "2026-03-12T14:22:11+00:00",
            "Tags": {"Name": "api-prod-1", "Environment": "production", "Team": "platform"},
        },
        {
            "InstanceId": "i-0fedcba9876543210",
            "InstanceType": "t3.small",
            "State": "running",
            "AvailabilityZone": "us-east-1b",
            "PrivateIpAddress": "10.0.2.18",
            "PublicIpAddress": None,
            "LaunchTime": "2026-03-12T14:25:03+00:00",
            "Tags": {"Name": "api-prod-2", "Environment": "production", "Team": "platform"},
        },
        {
            "InstanceId": "i-0123456789abcdef0",
            "InstanceType": "t3.large",
            "State": "stopped",
            "AvailabilityZone": "us-east-1a",
            "PrivateIpAddress": "10.0.3.7",
            "PublicIpAddress": None,
            "LaunchTime": "2026-01-08T09:10:00+00:00",
            "Tags": {"Name": "batch-worker", "Environment": "staging", "Team": "data"},
        },
    ]
    alarms = [
        {
            "AlarmName": "api-prod-cpu-high",
            "StateValue": "ALARM",
            "MetricName": "CPUUtilization",
            "Namespace": "AWS/EC2",
            "Statistic": "Average",
            "Threshold": 80.0,
            "ComparisonOperator": "GreaterThanThreshold",
        },
        {
            "AlarmName": "alb-5xx-rate",
            "StateValue": "ALARM",
            "MetricName": "HTTPCode_Target_5XX_Count",
            "Namespace": "AWS/ApplicationELB",
            "Statistic": "Sum",
            "Threshold": 10.0,
            "ComparisonOperator": "GreaterThanThreshold",
        },
        {
            "AlarmName": "lambda-errors-daily",
            "StateValue": "OK",
            "MetricName": "Errors",
            "Namespace": "AWS/Lambda",
            "Statistic": "Sum",
            "Threshold": 5.0,
            "ComparisonOperator": "GreaterThanThreshold",
        },
        {
            "AlarmName": "rds-free-storage",
            "StateValue": "INSUFFICIENT_DATA",
            "MetricName": "FreeStorageSpace",
            "Namespace": "AWS/RDS",
            "Statistic": "Average",
            "Threshold": 5_000_000_000.0,
            "ComparisonOperator": "LessThanThreshold",
        },
    ]
    load_balancers = [
        {
            "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:111122223333:loadbalancer/app/api-prod-alb/abc123",
            "DNSName": "api-prod-alb-1234567890.us-east-1.elb.amazonaws.com",
            "Type": "application",
            "Scheme": "internet-facing",
            "VpcId": "vpc-0example111",
            "State": "active",
        },
    ]
    functions = [
        {
            "FunctionName": "orders-webhook",
            "Runtime": "python3.12",
            "MemorySize": 512,
            "LastModified": "2026-05-10T18:44:12.000+0000",
            "Timeout": 30,
        },
        {
            "FunctionName": "image-resize",
            "Runtime": "python3.12",
            "MemorySize": 1024,
            "LastModified": "2026-04-22T11:02:55.000+0000",
            "Timeout": 60,
        },
    ]
    buckets = [
        {"Name": "acme-prod-assets-111122223333", "CreationDate": "2025-11-01T12:00:00+00:00"},
        {"Name": "acme-logs-archive-111122223333", "CreationDate": "2025-11-01T12:05:00+00:00"},
        {"Name": "acme-terraform-state-111122223333", "CreationDate": "2024-06-15T08:30:00+00:00"},
    ]
    security_groups = [
        {
            "GroupId": "sg-0a11bb22cc33dd44",
            "GroupName": "api-prod-sg",
            "VpcId": "vpc-0example111",
            "Description": "API tier ingress from ALB",
            "IngressRules": 3,
            "EgressRules": 1,
        },
        {
            "GroupId": "sg-0eeff11223344556",
            "GroupName": "alb-public-sg",
            "VpcId": "vpc-0example111",
            "Description": "Internet-facing ALB",
            "IngressRules": 2,
            "EgressRules": 1,
        },
    ]
    alarm_states: dict[str, int] = {}
    for a in alarms:
        alarm_states[a["StateValue"]] = alarm_states.get(a["StateValue"], 0) + 1
    ec2_states: dict[str, int] = {}
    for i in instances:
        ec2_states[i["State"]] = ec2_states.get(i["State"], 0) + 1

    return {
        "demo_mode": True,
        "whoami": whoami,
        "summary": {
            "ec2_total": len(instances),
            "ec2_running": ec2_states.get("running", 0),
            "alarms_in_alarm": alarm_states.get("ALARM", 0),
            "alarms_total": len(alarms),
            "load_balancers": len(load_balancers),
            "lambda_functions": len(functions),
            "s3_buckets": len(buckets),
            "security_groups": len(security_groups),
        },
        "instances": instances,
        "alarms": alarms,
        "load_balancers": load_balancers,
        "functions": functions,
        "buckets": buckets,
        "security_groups": security_groups,
        "tools": [
            "aws_whoami",
            "list_ec2_instances",
            "describe_ec2_instance",
            "list_security_groups",
            "list_cloudwatch_alarms",
            "describe_cloudwatch_alarm",
            "list_s3_buckets",
            "list_lambda_functions",
            "describe_load_balancers_v2",
        ],
    }
