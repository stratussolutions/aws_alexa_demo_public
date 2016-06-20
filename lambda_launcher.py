from __future__ import print_function

import json
import boto3
import botocore

#=================================================
# Default handler
#=================================================
def lambda_handler(event, context):

    #print(str(event))

    #print("event.session.application.applicationId=" + event['session']['application']['applicationId'])

    # Validate that the Alexa app is actually invoking this function.
    # Add your Alexa skill application Id between the quotes
    if (event['session']['application']['applicationId'] != ""):
     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    # Determine how to route the intent.
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])

    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


#=================================================
# on_session_started
#=================================================
def on_session_started(session_started_request, session):
    """ Called when the session starts """

    #print("on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])


#=================================================
# on_launch
#=================================================
def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    #print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])

    # Dispatch to the skill's launch
    return get_welcome_response()


#=================================================
# on_intent
#=================================================
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    #print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name'].lower()

    # Dispatch to your skill's intent handlers
    if intent_name == "GateKeeperLaunchIntent".lower():
        return handle_gatekeeper_launch_intent(intent, session)
        
    elif intent_name == "QueryAlertIntent".lower():
        return handle_query_alert_intent(intent, session)

    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()

    else:
        return handle_unknown_request()
        #raise ValueError("Invalid intent")


#=================================================
# on_session_ended
#=================================================
def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    #print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Functions that control the skill's behavior ------------------

#=================================================
# get_welcome_response
#=================================================
def get_welcome_response():
    # Initialize anything here as necessary.

    session_attributes = {}
    speech_output = "Hello, thank you for launching the Stratus Solutions Gate Keeper Launcher. I can help secure Amazon EC2 instances by isolating compromised instances within a quarantine subnet. How may I be of assistance today? ";
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(speech_output, reprompt_text, should_end_session))


#=================================================
# handle_session_end_request
#=================================================
def handle_session_end_request():

    speech_output = "Closing Gate Keeper Launcher. Have a nice day."
    should_end_session = True
    return build_response(build_speechlet_response(speech_output, None, should_end_session))

#=================================================
# handle_unknown_request
#=================================================
def handle_unknown_request():

    speech_output = "I'm sorry, I wasn't able to process your request."
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response(build_speechlet_response(speech_output, None, should_end_session))


#=================================================
# handle_gatekeeper_launch_intent
#=================================================
def handle_gatekeeper_launch_intent(intent, session):

    session_attributes = {}
    should_end_session = True
    
    sns = boto3.client('sns')
    sns.publish(
	#Add SNS topic Id that will be used to initiate lambda_function.py
        TopicArn='',
        Message=' ',
        MessageStructure='string',
    )

    speech_output = "Applying security countermeasures. Initiating sequence to isolate infected instance."
    reprompt_text = speech_output

    return build_response(session_attributes, build_speechlet_response(speech_output, reprompt_text, should_end_session))


#=================================================
# handle_query_alert_intent
#=================================================
def handle_query_alert_intent(intent, session):

    session_attributes = {}
    should_end_session = False

    speech_output = "Alert! Connection established to known bad actor. Your instance may be compromised."
    reprompt_text = speech_output

    return build_response(session_attributes, build_speechlet_response(speech_output, reprompt_text, should_end_session))


# --------------- Helpers that build all of the responses----------------------


#=================================================
# build_speechlet_response
#=================================================
def build_speechlet_response(output, reprompt_text, should_end_session):

    return_value =  {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
        }

    return return_value


#=================================================
# build_response
#=================================================
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
