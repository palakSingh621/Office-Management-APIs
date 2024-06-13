# Office-Management-APIs
Creating a set of API endpoints to manage office-related data for an organization.
## Objective:
API is developed using Python (AWS Lambda without any framework) and hosted on AWS Lambda.
Using Amazon DynamoDB to access database.
## Amazon DynamoDB
Amazon DynamoDB is a fully managed NoSQL database service that provides fast and predictable performance with seamless scalability. We can use Amazon DynamoDB to create a database table that can store and retrieve any amount of data, and serve any level of request traffic. Amazon DynamoDB automatically spreads the data and traffic for the table over a sufficient number of servers to handle the request capacity specified by the customer and the amount of data stored, while maintaining consistent and fast performance.
### Step1: Creating DynamoDB Tables
![dynamodb1](https://github.com/palakSingh621/Office-Management-APIs/assets/107800373/42a66f8e-fbff-48ab-86a3-c57f3b35384f)

_Table1: office_data_
id : String (Partition key)
name : String 
location :String 
_Table2: office_transactions_
officeid : String (Partition key)
amount : Number
transactionType : String

## API Gateway
Amazon API Gateway lets developers connect non-AWS applications to AWS back-end resources. It is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. APIs act as the "front door" for applications to access data, business logic, or functionality from your backend services.

## RESTful API:
A RESTful API is an architectural style for an application programming interface that uses HTTP requests to access and use data. That data can be used to GET , PUT , POST and DELETE data types, which refers to reading, updating, creating and deleting operations related to resources.

### Step2: Creating API Gateway

![API1](https://github.com/palakSingh621/Office-Management-APIs/assets/107800373/143fbd37-9aba-49db-874d-6baf029e2504)
![API2](https://github.com/palakSingh621/Office-Management-APIs/assets/107800373/e56bebec-848a-4977-abd9-0f99f8aa10de)
_Resources inside the API:_
 * office:
 * offices:
   -> transaction
 * status:

Deploying API staging it as officedata to invoke the Staging URL:
https://qrba02lwn4.execute-api.ap-south-1.amazonaws.com/officedata

## AWS Lambda
AWS Lambda is a serverless, event-driven compute service that lets us run code for virtually any type of application or backend service without provisioning or managing servers. It lets us automatically run code in response to many types of events, such as HTTP requests from the Amazon API gateway, table updates in Amazon DynamoDB, and state transitions.

### Step3: Creating AWS Lambda Function
![Lambda1](https://github.com/palakSingh621/Office-Management-APIs/assets/107800373/396942bd-2d41-4b08-abee-f8e0ac844713)


![Lambda2](https://github.com/palakSingh621/Office-Management-APIs/assets/107800373/33f4640f-c438-4690-b091-3dabf211dc3f)



![Lambda3](https://github.com/palakSingh621/Office-Management-APIs/assets/107800373/62d30d9c-96b3-402d-b879-0b2a2f9203ed)
![Lambda4](https://github.com/palakSingh621/Office-Management-APIs/assets/107800373/8745e38e-75b3-4426-aaa3-73671ec6c247)
