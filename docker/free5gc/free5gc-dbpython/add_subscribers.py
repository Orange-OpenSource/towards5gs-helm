import argparse
import free5gc_db

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mongo", help="Mongodb address", default='mongodb')
parser.add_argument("-a", "--action", help="Action to be performed (list|add|clean", default='list')
parser.add_argument("-i", "--imsi", help="IMSI of first UE", default='999700000000001')
parser.add_argument("-n", "--number", type=int, help="Number of UEs", default=1)

args = parser.parse_args()

free5gc_instance = free5gc_db.Free5gc(args.mongo, 27017)

if args.action == 'list':
    subscribers_data = free5gc_instance.get_subscribers()
    for key, value in subscribers_data.items():
        print(key)
        counter = 0
        for item in value:
            print(item)
            counter += 1
            if args.number != -1 and counter > args.number:
                break
        print("\n\n\n")
    print("Summary:")
    for key, value in subscribers_data.items():
        print(f"{key}: {len(value)}")

if args.action == 'clean':
    free5gc_instance.delete_all_subscribers()

if args.action == 'add':
    subscriber_data = {
        'subscriptionData.provisionedData.smfSelectionSubscriptionData': [{
            'servingPlmnId': '20893',
            'subscribedSnssaiInfos': {'01010203': {'dnnInfos': [{'dnn': 'internet'}]},
                                      '01112233': {'dnnInfos': [{'dnn': 'internet'}]}},
            'ueId': 'imsi-208930000000003'
          }],
        'subscriptionData.provisionedData.smData': [{
            'dnnConfigurations': {'internet': {'5gQosProfile': {'5qi': 9.0,
                                                                'arp': {'preemptCap': '',
                                                                        'preemptVuln': '',
                                                                        'priorityLevel': 8.0},
                                                                'priorityLevel': 8.0},
                                              'pduSessionTypes': {'allowedSessionTypes': ['IPV4'],
                                                                  'defaultSessionType': 'IPV4'},
                                              'sessionAmbr': {'downlink': '100 Mbps',
                                                              'uplink': '200 Mbps'},
                                              'sscModes': {'allowedSscModes': ['SSC_MODE_2',
                                                                                'SSC_MODE_3'],
                                                            'defaultSscMode': 'SSC_MODE_1'}}},
            'servingPlmnId': '20893',
            'singleNssai': {'sd': '010203', 'sst': 1.0},
            'ueId': 'imsi-208930000000003'},
          {
            'dnnConfigurations': {'internet': {'5gQosProfile': {'5qi': 9.0,
                                                                'arp': {'preemptCap': '',
                                                                        'preemptVuln': '',
                                                                        'priorityLevel': 8.0},
                                                                'priorityLevel': 8.0},
                                              'pduSessionTypes': {'allowedSessionTypes': ['IPV4'],
                                                                  'defaultSessionType': 'IPV4'},
                                              'sessionAmbr': {'downlink': '100 Mbps',
                                                              'uplink': '200 Mbps'},
                                              'sscModes': {'allowedSscModes': ['SSC_MODE_2',
                                                                                'SSC_MODE_3'],
                                                            'defaultSscMode': 'SSC_MODE_1'}}},
            'servingPlmnId': '20893',
            'singleNssai': {'sd': '112233', 'sst': 1.0},
            'ueId': 'imsi-208930000000003'}],
        'policyData.ues.smData': [{
            'smPolicySnssaiData': {'01010203': {'smPolicyDnnData': {'internet': {'dnn': 'internet'}},
                                                'snssai': {'sd': '010203', 'sst': 1.0}},
                                  '01112233': {'smPolicyDnnData': {'internet': {'dnn': 'internet'}},
                                                'snssai': {'sd': '112233', 'sst': 1.0}}},
            'ueId': 'imsi-208930000000003'}],
        'policyData.ues.amData': [{
            'subscCats': ['free5gc'],
            'ueId': 'imsi-208930000000003'}],
        'subscriptionData.provisionedData.amData': [{
          'gpsis': ['msisdn-0900000000'],
          'nssai': {'defaultSingleNssais': [{'sd': '010203', 'sst': 1.0},
                                            {'sd': '112233', 'sst': 1.0}]},
          'servingPlmnId': '20893',
          'subscribedUeAmbr': {'downlink': '2 Gbps', 'uplink': '1 Gbps'},
          'ueId': 'imsi-208930000000003'}],

        'subscriptionData.authenticationData.authenticationSubscription': [{
            'authenticationManagementField': '8000',
            'authenticationMethod': '5G_AKA',
            'milenage': {'op': {'encryptionAlgorithm': 0.0,
                                'encryptionKey': 0.0,
                                'opValue': ''}},
            'opc': {'encryptionAlgorithm': 0.0,
                    'encryptionKey': 0.0,
                    'opcValue': '8e27b6af0e692e750f32667a3b14605d'},
            'permanentKey': {'encryptionAlgorithm': 0.0,
                            'encryptionKey': 0.0,
                            'permanentKeyValue': '8baf473f2f8fd09487cccbd7097c6862'},
            'sequenceNumber': '16f3b3f70fc2',
            'ueId': 'imsi-208930000000003'}],
    }


    initial_imsi = args.imsi
    number_of_ues = args.number

    imsi_prefix = initial_imsi[:-9]
    initial_index = int(initial_imsi[-9:])

    for _index in range(number_of_ues):
        imsi_suffix = str(initial_index+_index).rjust(9, '0')
        imsi_value = imsi_prefix+imsi_suffix
        for key, value in subscriber_data.items():
            for item in value:
                item['ueId'] = imsi_value
        result = free5gc_instance.add_subscriber(subscriber_data)
        if result:
          print("One subscriber stored in the database")
        else:
          print("error")
