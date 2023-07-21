from pyaudiowpatch import PyAudio, paWASAPI

def get_input_device_list():
    devices = {}
    with PyAudio() as p:
        for host_index in range(0, p.get_host_api_count()):
            host = p.get_host_api_info_by_index(host_index)
            for device_index in range(0, p.get_host_api_info_by_index(host_index)['deviceCount']):
                device = p.get_device_info_by_host_api_device_index(host_index, device_index)
                if device["maxInputChannels"] > 0 and device["isLoopbackDevice"] is False:
                    if host["name"] in devices.keys():
                        devices[host["name"]].append(device)
                    else:
                        devices[host["name"]] = [device]
    return devices

def get_output_device_list():
    devices =[]
    with PyAudio() as p:
        wasapi_info = p.get_host_api_info_by_type(paWASAPI)
        for device in p.get_loopback_device_info_generator():
            if device["hostApi"] == wasapi_info["index"] and device["isLoopbackDevice"] is True:
                devices.append(device)
    return devices

def get_default_input_device():
    with PyAudio() as p:
        api_info = p.get_default_host_api_info()
        defaultInputDevice = api_info["defaultInputDevice"]

        for host_index in range(0, p.get_host_api_count()):
            host = p.get_host_api_info_by_index(host_index)
            for device_index in range(0, p. get_host_api_info_by_index(host_index)['deviceCount']):
                device = p.get_device_info_by_host_api_device_index(host_index, device_index)
                if device["index"] == defaultInputDevice:
                    return {"host":host, "device": device}

def get_default_output_device():
    with PyAudio() as p:
        wasapi_info = p.get_host_api_info_by_type(paWASAPI)
        defaultOutputDevice = wasapi_info["defaultOutputDevice"]

        for host_index in range(0, p.get_host_api_count()):
            for device_index in range(0, p. get_host_api_info_by_index(host_index)['deviceCount']):
                device = p.get_device_info_by_host_api_device_index(host_index, device_index)
                if device["index"] == defaultOutputDevice:
                    default_speakers = device
                    if not default_speakers["isLoopbackDevice"]:
                        for loopback in p.get_loopback_device_info_generator():
                            if default_speakers["name"] in loopback["name"]:
                                default_device = loopback
                                return default_device