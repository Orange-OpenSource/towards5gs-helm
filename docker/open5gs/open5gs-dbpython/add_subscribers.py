import argparse
import bson
import Open5GS

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--imsi", help="IMSI of first UE", default='999700000000001')
parser.add_argument("-n", "--number", type=int, help="Number of UEs", default=1)
parser.add_argument("-m", "--mongo", help="Mongodb address", default='mongodb')

args = parser.parse_args()

Open5GS_1 = Open5GS.Open5GS(args.mongo, 27017)

slice_data = [
    {
      "sst": 1,
      "default_indicator": True,
      "session": [
        {
          "name": "internet",
          "type": 3, "pcc_rule": [], "ambr": {"uplink": {"value": 1, "unit": 3}, "downlink": {"value": 1, "unit": 3}},
          "qos": {
            "index": 9,
            "arp": {"priority_level": 8, "pre_emption_capability": 1, "pre_emption_vulnerability": 1}
          }
        }
      ]
    }
  ]

sub_data = {
  "_id": '',
  "imsi": "",
  "subscribed_rau_tau_timer": 12,
  "network_access_mode": 0,
  "subscriber_status": 0,
  "access_restriction_data": 32,
  "slice" : slice_data,
  "ambr": {"uplink": {"value": 1, "unit": 3}, "downlink": {"value": 1, "unit": 3}},
  "security": {
    "k": "465B5CE8 B199B49F AA5F0A2E E238A6BC",
    "amf": "8000",
    'op': None,
    "opc": "E8ED289D EBA952E4 283B54E8 8E6183CA"
  },
  "schema_version": 1,
  "__v": 0
}

initial_imsi = args.imsi
number_of_ues = args.number

imsi_prefix = initial_imsi[:-9]
initial_index = int(initial_imsi[-9:])

for _index in range(number_of_ues):
    sub_data["_id"] = bson.ObjectId()
    imsi_suffix = str(initial_index+_index).rjust(9, '0')
    imsi_value = imsi_prefix+imsi_suffix
    sub_data["imsi"] = imsi_value
    print(Open5GS_1.AddSubscriber(sub_data))                        #Add Subscriber using dict of sub_data
