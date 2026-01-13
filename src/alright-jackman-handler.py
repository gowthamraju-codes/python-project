import json


def generate_mediaconvert_job(input_file_path, output_file_path, preset_name="System-Generic_Hd_Mp4_Av1_Aac_16x9_1920x1080p_24Hz_6000Kbps"):
    """
    Generate a MediaConvert job JSON configuration.

    Args:
        input_file_path (str): S3 path to the input video file
        output_file_path (str): S3 path for the output video file
        preset_name (str): MediaConvert preset name for output settings

    Returns:
        dict: MediaConvert job configuration
    """
    job_config = {
        "Role": "arn:aws:iam::123456789012:role/MediaConvertRole",
        "Settings": {
            "Inputs": [
                {
                    "FileInput": input_file_path,
                    "AudioSelectors": {
                        "Audio Selector 1": {
                            "DefaultSelection": "DEFAULT"
                        }
                    },
                    "VideoSelector": {},
                    "TimecodeSource": "ZEROBASED"
                }
            ],
            "OutputGroups": [
                {
                    "Name": "File Group",
                    "OutputGroupSettings": {
                        "Type": "FILE_GROUP_SETTINGS",
                        "FileGroupSettings": {
                            "Destination": output_file_path
                        }
                    },
                    "Outputs": [
                        {
                            "ContainerSettings": {
                                "Container": "MP4",
                                "Mp4Settings": {}
                            },
                            "VideoDescription": {
                                "CodecSettings": {
                                    "Codec": "H_264",
                                    "H264Settings": {
                                        "RateControlMode": "QVBR",
                                        "MaxBitrate": 6000000,
                                        "QualityTuningLevel": "SINGLE_PASS_HQ",
                                        "FramerateControl": "INITIALIZE_FROM_SOURCE"
                                    }
                                }
                            },
                            "AudioDescriptions": [
                                {
                                    "CodecSettings": {
                                        "Codec": "AAC",
                                        "AacSettings": {
                                            "Bitrate": 128000,
                                            "CodingMode": "CODING_MODE_2_0",
                                            "SampleRate": 48000
                                        }
                                    }
                                }
                            ],
                            "NameModifier": f"_{preset_name}"
                        }
                    ]
                }
            ],
            "TimecodeConfig": {
                "Source": "ZEROBASED"
            }
        },
        "AccelerationSettings": {
            "Mode": "DISABLED"
        },
        "StatusUpdateInterval": "SECONDS_60",
        "Priority": 0
    }

    return job_config


def main():
    """Main function that generates MediaConvert job JSON based on inputs."""
    # Define inputs
    input_video = "s3://my-input-bucket/videos/source-video.mp4"
    output_destination = "s3://my-output-bucket/transcoded/"
    preset = "HD_1080p_H264"

    print("=" * 60)
    print("AWS MediaConvert Job JSON Generator")
    print("=" * 60)
    print(f"\nInput Parameters:")
    print(f"  - Input Video: {input_video}")
    print(f"  - Output Destination: {output_destination}")
    print(f"  - Preset: {preset}")
    print("\n" + "=" * 60)

    # Generate the MediaConvert job configuration
    job_json = generate_mediaconvert_job(input_video, output_destination, preset)

    # Pretty print the JSON output
    print("\nAlright alright alright... Matheww is here!!")
    print("\nGenerated MediaConvert Job JSON :")
    print("=" * 60)
    print(json.dumps(job_json, indent=2))

    # Optionally save to file
    output_file = "mediaconvert_job.json"
    with open(output_file, 'w') as f:
        json.dump(job_json, f, indent=2)

    print("\n" + "=" * 60)
    print(f"JSON configuration saved to: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()

