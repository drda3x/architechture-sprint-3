#!/bin/python
import argparse
import requests


URL = "http://localhost:5000{}"


def add_device(args):
    data = {
        "device_id": args.device_id,
        "device_type": args.device_type
    }

    response = requests.post(URL.format("/device/add"), json=data)
    return response.status_code


def set_light_state(args):
    data = {
        "device_id": args.device_id,
        "status": args.status
    }

    response = requests.post(URL.format("/device/state"), json=data)
    return response.status_code


def set_gate_state(args):
    data = {
        "device_id": args.device_id,
        "status": args.status
    }

    response = requests.post(URL.format("/device/state"), json=data)
    return response.status_code


def set_temperature_state(args):
    data = {
        "device_id": args.device_id,
        "temperature_val": args.temp
    }

    response = requests.post(URL.format("/device/state"), json=data)
    return response.status_code


def set_video_state(args):
    data = {
        "device_id": args.device_id,
        "status": args.status
    }

    response = requests.post(URL.format("/device/state"), json=data)
    return response.status_code


def get_state(args):
    data = {
        "device_id": args.device_id
    }

    response = requests.get(URL.format("/device/state"), json=data)
    return response.status_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--request_type", help="get | set | add")
    parser.add_argument("--device_id", help="Device id")
    parser.add_argument("--device_type", help="ligth_device | gate_device | video_device | hit_device")
    parser.add_argument("--status", help="parameter of ligth_device | gate_device | video_device")
    parser.add_argument("--temp", help="parameter of hit_device")

    args = parser.parse_args()

    if args.request_type == "get":
       print(get_state(args))

    elif args.request_type == "add":
        print(add_device(args))

    else:
        handlers_map = {
            'ligth_device': set_light_state,
            'hit_device': set_temperature_state,
            'video_device': set_video_state,
            'gate_device': set_gate_state
        }

        print(handlers_map.get(args.device_type, lambda x: None)(args))
