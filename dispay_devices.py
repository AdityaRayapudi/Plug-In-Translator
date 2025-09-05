import pyaudio

def list_audio_devices_simple():
    """
    lists device index and name of audio devices
    """
    p = pyaudio.PyAudio()
    
    print("Audio Devices (Simple List):")
    print("=" * 50)
    
    device_count = p.get_device_count()
    
    for i in range(device_count):
        try:
            device_info = p.get_device_info_by_index(i)
            max_input_channels = device_info.get('maxInputChannels', 0)
            max_output_channels = device_info.get('maxOutputChannels', 0)
            default_sample_rate = device_info.get('defaultSampleRate', 0)

            # Determine device type
            if max_input_channels > 0 and max_output_channels > 0:
                device_type = "Input/Output"
            elif max_input_channels > 0:
                device_type = "Input Only"
            elif max_output_channels > 0:
                device_type = "Output Only"
            else:
                device_type = "Unknown"

            print(f"Index {i:<3}| {device_type:<11} | {device_info.get('name', 'Unknown')}")
        except:
            print(f"Index {i}: Error retrieving device info")
    
    p.terminate()

if __name__ == "__main__":
    print("PyAudio Device Lister")
    print("=" * 30)

    print("\n" + "="*60 + "\n")
    
    # Show simple list
    list_audio_devices_simple()