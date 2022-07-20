#!/usr/bin/python3
import traceback
from datetime import datetime

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

from storebox_rgb_led import *

import threading
import json
import math
import signal
import schedule

received_all_event = threading.Event()

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)

# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))
    current_datetime = datetime.now()
    current_week_day = current_datetime.weekday()  # 0 is monday, 6 is sunday
    current_hour = current_datetime.hour  # between 0 and 23
    if current_week_day > 4:
        print(f"weekday is {current_week_day}, ignore event")
        return
    if current_hour < 8 or current_hour > 19:
        print(f"current hour is {current_hour}, ignore event")
        return
    if RGB_STRIP_AVAILABLE is False:
        print("No RGB animation")
        return
    if "keyresults" in topic:
        payloadDict = json.loads(payload)
        department = payloadDict["department"]
        if department == "CustomerHappinessGrowth":
            startAnimation(StoreboxAnimation.abwischen)
        elif department == "Marketing":
            startAnimation(StoreboxAnimation.KeyResultMarketing)
        elif department == "PeopleCulture":
            startAnimation(StoreboxAnimation.anim3)
        elif department == "BusinessDevelopment":
            startAnimation(StoreboxAnimation.anim2)
        elif department == "Operations":
            startAnimation(StoreboxAnimation.KeyResultOperation)
        elif department == "Finance":
            startAnimation(StoreboxAnimation.KeyResultFinance)
        elif department == "Tech":
            startAnimation(StoreboxAnimation.KeyResultTech)
        elif department == "CuSe":
            startAnimation(StoreboxAnimation.abwischen)
        else:
            print("Unknown department: " + department)
    elif "bookings" in topic:
        print("Start booking animation")
        payloadDict = json.loads(payload)
        monthlyDebitNetto = payloadDict["monthlyDebitNetto"]
        monthlyDebitNettoFloor = int(math.floor(monthlyDebitNetto))
        insuranceSum = payloadDict["insuranceSum"]
        startAnimation(StoreboxAnimation.Booking, monthlyDebitNettoFloor, insuranceSum)

        # TODO 
    elif "sensor/limit" in topic:
        print("Received sensor limit animation")
        payloadDict = json.loads(payload)
        limitType = payloadDict["type"]
        if "_TOO_COLD" in limitType:
            print("Start sensor limit animation (TOO_COLD)")
            storeboxTemperatureEffectTooCold(strip)
        else:
            print("Start sensor limit animation (TOO_HOT)")
            storeboxTemperatureEffectTooHot(strip)
    elif "alarm" in topic:
        print("Start alarm animation")
        storeboxFireEffect(strip)
    else:
        print("Cannot handle topic ".format(topic))


def shutdown(signum, frame):
    print("Shutdown event received")
    raise ServiceExit
def job():
    print("I'm working")
def coding():
    print("Coding time..")

class ServiceExit(Exception):
    pass

    
if __name__ == '__main__':
    
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGHUP, shutdown)
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    credentials_provider = auth.AwsCredentialsProvider.new_default_chain(client_bootstrap)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=CERT_FILEPATH,
        pri_key_filepath=PRIVATE_KEY_FILEPATH,
        client_bootstrap=client_bootstrap,
        ca_filepath=CA_FILEPATH,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=600)  # was 6

    print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    try:
        print("Connecting to {} with client ID '{}'...".format(ENDPOINT, CLIENT_ID))
        
        connect_future = mqtt_connection.connect()

        connect_future.result()
        print("connected")
        if (RGB_STRIP_AVAILABLE):
            print("setting schedule to start rapid animation at 10:58 every day")
            startAnimation(StoreboxAnimation.abwischen)
            startAnimation(StoreboxAnimation.anim3)
            startAnimation(StoreboxAnimation.anim2)
            startAnimation(StoreboxAnimation.Fire)
            startAnimation(StoreboxAnimation.TempratureTooHot)
            startAnimation(StoreboxAnimation.KeyResultHR)
            startAnimation(StoreboxAnimation.KeyResultTech)
            schedule.every().day.at("10:58").do(lambda: startAnimation(StoreboxAnimation.Rapid))

        # Subscribe  to topics
    #    topics = ["/backend/TEST/bookings", "/backend/TEST/sensor/limit", "/backend/TEST/sensor/alarm"]
        topics = ["backend/TEST/bookings", "backend/TEST/keyresults", "backend/bookings", "backend/keyresults"]

        for topic in topics:
            print("Subscribing to topic '{}'...".format(topic))
            subscribe_future, packet_id = mqtt_connection.subscribe(
                topic=topic,
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=on_message_received)

            subscribe_result = subscribe_future.result()
            print("Subscribed with {}".format(str(subscribe_result['qos'])))

        received_all_event.wait()  # wait forever? => no clean disconnect??
    except ServiceExit:
        print("Shutdown event received, stopped execution")
        received_all_event.set()
    except:
        traceback.print_exc()
    finally:
        # Disconnect
        print("Disconnecting...")
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")

