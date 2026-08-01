import json
import paho.mqtt.client as mqtt

from common.data_source import fetch_price


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="pub-1")
client.connect("localhost", 1883)
client.loop_start()


reading = fetch_price("BTC-USD")
message = json.dumps(reading)
result = client.publish("telemetry/pub-1/crypto", message)
result.wait_for_publish()
print("Published!")

client.loop_stop()
client.disconnect()