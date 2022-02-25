import os
import argparse
from pathlib import Path
from evo.tools import file_interface
from evo.core.trajectory import PosePath3D, PoseTrajectory3D
from rosbags.rosbag1 import Reader as Rosbag1Reader, Writer as Rosbag1Writer


def parse_args():
    parser = argparse.ArgumentParser(description="")
    script_dir_path = str(Path())
    parser.add_argument("--input-data-path", "-i", type=str, default=f"{script_dir_path}/data/camera_pose.txt")
    parser.add_argument("--output-data-path", "-o", type=str, default=f"{script_dir_path}/data/camera_pose.bag")
    return parser.parse_args()


def to_topic_name(name: str, args: argparse.Namespace) -> str:
    if args.subcommand in ("bag", "bag2"):
        return name.replace(":", "/")
    return "/" + os.path.splitext(os.path.basename(name))[0].replace(" ", "_")


if __name__ == "__main__":
    args = parse_args()
    trajectory_data: PoseTrajectory3D = file_interface.read_tum_trajectory_file(args.input_data_path)

    if Path(args.output_data_path).exists():
        print(f"{args.output_data_path} exists already, conduct overwriting.")
        os.remove(args.output_data_path)

    print("Start convertion")
    rosbag_writer = Rosbag1Writer(args.output_data_path)
    try:
        rosbag_writer.open()
        file_interface.write_bag_trajectory(writer=rosbag_writer, traj=trajectory_data, topic_name="/tum_data")
    finally:
        rosbag_writer.close()
        print("Done")
