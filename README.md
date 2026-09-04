# Module 3 – Synchronous + Idempotence

Part of the [AWS Serverless Patterns Workshop](https://catalog.workshops.aws/serverless-patterns/en-US/module3), this module builds a synchronous, idempotent **Orders API** on top of the foundational patterns covered in Module 2 (Synchronous Invocation).

**Estimated duration:** 2–3 hours

---

## What You Will Build

A synchronous Orders API with the following characteristics:

- **Idempotent operations** – guarantees consistent system state even when a request is retried (e.g. due to network failures or client-side retries).
- **Single-purpose Lambda functions** – each function handles exactly one operation/route, rather than a single monolithic handler for the whole API.
- **Business rule enforcement** – order cancellation is restricted to orders that have not yet been acknowledged by a restaurant.
- **Observability by design** – structured logging and custom metrics are added using [Powertools for AWS Lambda (Python)](https://docs.powertools.aws.dev/lambda/python/latest/).

---

## What You Will Learn

- How to design APIs that are **safe to retry** by implementing idempotency, preventing duplicate side effects (e.g. duplicate orders) when the same request is sent more than once.
- How to structure Lambda functions using a **single-purpose (specialized function) approach** instead of a monolithic handler, and the trade-offs behind that architectural decision.
- How to share code across functions using **AWS Lambda Layers**.
- How to add **idempotency, structured logging, and custom metrics** with minimal code using Powertools for AWS Lambda (Python).
- How to deploy serverless infrastructure with the **AWS Serverless Application Model (AWS SAM)**, as an alternative to AWS CDK used in Module 2.
- How to write **integration tests** to verify API behavior end-to-end.

---

## Architect's Note: Why Multiple Lambda Functions?

When designing serverless applications, you must choose between a single monolithic Lambda function or multiple smaller, specialized functions. This module favors the specialized-function approach for the following reasons:

| Factor                        | Benefit of Specialized Functions                                                                       |
| ----------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Development & maintenance** | Smaller functions have clear boundaries, are easier to develop, test, troubleshoot, and maintain.      |
| **Modularity & reusability**  | Distinct functionality is isolated, making code more modular, reusable, and independently deployable.  |
| **Security**                  | Each function can be assigned a focused IAM role with the fewest permissions needed (least privilege). |
| **Scalability & performance** | Functions scale independently and can be tuned (e.g. memory allocation) for their specific workload.   |
| **Cost optimization**         | Resource allocation (e.g. memory) can be fine-tuned per function, reducing overall cost.               |

> The right architectural choice ultimately depends on your specific requirements — this is a recommended default, not a hard rule.

---

## Key AWS Services & Tools

| Service / Tool                             | Purpose                                                                                                  |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| **AWS Lambda Layers**                      | Package and share libraries/dependencies across multiple Lambda functions.                               |
| **Powertools for AWS Lambda (Python)**     | Developer toolkit for implementing serverless best practices (idempotency, structured logging, metrics). |
| **Amazon CloudWatch**                      | Application and infrastructure monitoring.                                                               |
| **AWS Serverless Application Model (SAM)** | Framework for defining and deploying serverless infrastructure via YAML templates and the SAM CLI.       |
| **Amazon Cognito**                         | Identity store for user sign-up/sign-in and access control.                                              |
| **Amazon DynamoDB**                        | Fully managed NoSQL key/value data store.                                                                |
| **Amazon API Gateway**                     | REST, HTTP, and WebSocket API management.                                                                |

---

## Prerequisites

- A prepared development environment (cloud-based IDE or local) with all required dependencies.
- If not yet set up, complete the **Getting Started** section of the workshop first.

---

## Relation to Other Modules

This module builds directly on **Module 2 – Synchronous Invocation**, which covered:

- Creating a data store and business logic (CDK + TypeScript)
- Securing an API with Amazon Cognito and a JWT Lambda Authorizer
- Unit and integration testing
- Observability (API Gateway access logging, X-Ray tracing)

Module 3 extends these concepts to a new use case (Orders) while introducing **idempotency**, **single-purpose functions**, and a **different toolchain (Python + AWS SAM)**, broadening the range of tools and patterns covered in the workshop.

---

## Reference

- Workshop link: [https://catalog.workshops.aws/serverless-patterns/en-US/module3](https://catalog.workshops.aws/serverless-patterns/en-US/module3)
