import requests, json
from time import sleep
counter = 0
partNums = [
  "MLY43ZP/A", # midnight
  "MLY23ZP/A", # starlight
  "MLXX3ZP/A", # spacegrey
  "MLY03ZP/A" # silver
]

ifttt_event = "apple_store_state_changed"
ifttt_auth = "enter ifttt auth key here"
def fetchStatus(partNum):
  res = requests.get("https://www.apple.com/sg/shop/fulfillment-messages?little=false&mt=regular&parts.0=" + partNum + "&option.0=065-CCJV,065-CCJW,065-CCL1,065-CCM2,065-CCLY,065-CCM1,065-CCM0,065-CD7G,065-CD0F,065-CD5Y,065-CD61&fts=true")
  res = json.loads(res.text)
  pickUpEligibility = res['body']['content']['pickupMessage']['pickupEligibility'][partNum]['storePickEligible']
  showDeliveryOptions = res['body']['content']['deliveryMessage'][partNum]['showDeliveryOptionsLink']
  isBuyable = res['body']['content']['deliveryMessage'][partNum]['isBuyable']
  subHeader = res['body']['content']['deliveryMessage'][partNum]['subHeader']
  return subHeader, pickUpEligibility, showDeliveryOptions, isBuyable


def postWebhook(partNum, subHeader, pickUpEligibility, showDeliveryOptions, isBuyable):
  payload = {
    "title": "Apple Store Stock Status Changed",
    "message": subHeader + "\n\n" + "Pickup Eligible: " + str(pickUpEligibility) + "\n" + "Show Delivery Options: " + str(showDeliveryOptions) + "\n" + "Is Buyable: " + str(isBuyable),
  }
  res = requests.post("https://maker.ifttt.com/trigger/" + ifttt_event + "/json/with/key/" + ifttt_auth, data=json.dumps(payload), headers={"Content-Type": "application/json"})
  print(res.text)
while(counter < 4):
  for p in partNums:
    subHeader, pickUpEligibility, showDeliveryOptions, isBuyable = fetchStatus(p)
    print(p, subHeader, pickUpEligibility, showDeliveryOptions, isBuyable)
    if (pickUpEligibility == True or showDeliveryOptions == True or isBuyable == True):
      postWebhook(p, subHeader, pickUpEligibility, showDeliveryOptions, isBuyable)
      counter += 1
    print('------')
  sleep(60)
sleep(60 * 60 * 24)