# Stratus Solutions 2016 AWS Public Sector Summit Demo
##AWS Policy Enforcement Engine

This demo involves the following technologies and AWS services: EC2, Elasticsearch, Kibana, ElastAlert, SNS, Lambda, an Amazon Echo, IFTTT, & LIFX Smart Home Light Bulbs.

##Scenario
Your company has a small, AWS-hosted web presence. In the interest of ensuring that your site is always available to your customers, you've taken the precautions of configuring load balancing and auto scaling for your web servers. But what about security? You decide that you want an automated means of isolating your web servers in the event that they come in contact with any known "bad actors" (i.e. sites or IP ranges that are known to be malicious). 

##AWS EC2
EC2 is used to provide two of the primary components of the demo: 1) A load balanced, highly available web server configured with auto scaling and 2) a "bad actor" instance. 

##Elasticsearch
An Elasticsearch cluster ingests network traffic logs from Packetbeat (running on the web servers) to facilitate real-time network traffic analysis within the environment.

##Kibana
Kibana serves as a graphical front end for Elasticsearch, with a custom dashboard displaying the number of active sessions to sites or IP ranges known to be malicious.

##ElastAlert
The open source tool, ElastAlert, is integrated with our Elasticsearch cluster to facilitate real-time alerting on data ingested into Elasticsearch. In this scenario, ElastAlert has been enriched with IP addresses that are known to be malicious (i.e. our "bad actor" EC2 instance) and sends an alert whenever a session is established to any of these addresses.

##AWS SNS
Once the ElastAlert is triggered, it reacts by publishing to an SNS topic in order to alert the operator that there may be an active security incident.

##IFTTT
IFTTT is integrated with SNS and once it receives a message it sends a command to the LIFX Smart Home Light Bulb to switch it from off to flashing red.

##AWS Lambda
Lambda is used to provide a function, written in Python, that is responsible for isolating the potentially compromised EC2 instance. It does so by performing the following steps:

	1. Creating an AMI of the compromised web server and then terminating the instance
	2. Provisioning a new instance based on the AMI in a quarantine subnet that has no inbound or outbound access; the AMI is subsequently deleted
	3. EC2 AutoScaling simultaneously handles re-provisioning a bootstrapped EC2 instance to ensure that the web server remains both highly available and load balanced

 The Event Source for the function is set to 'Alexa Skills Kit', allowing the function to be controlled by the Amazon Echo. In a real-world scenario, Lambda could be triggered directly from SNS, allowing a fully dynamic and automated security model.

##Amazon Echo
The Amazon Echo is equipped with a Custom Skill configured via the Amazon Developer Console, which is linked to the Lambda function. Interaction with the Skill is controlled by the IntentSchema (each intent corresponds to a handler in the Lambda function) and the Utterances file defines what the user can say to invoke the various Intents.


