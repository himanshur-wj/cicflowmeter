import argparse

from scapy.sendrecv import AsyncSniffer

from .flow_session import generate_session_class

import threading as th

from datetime import datetime


def create_sniffer(
    input_file, input_interface, output_mode, output_file, verbose=False
):
    assert (input_file is None) ^ (
        input_interface is None
    ), "Either provide interface input or file input not both"

    NewFlowSession = generate_session_class(output_mode, output_file, verbose)

    if input_file:
        return AsyncSniffer(
            offline=input_file,
            filter="ip and (tcp or udp)",
            prn=None,
            session=NewFlowSession,
            store=False,
        )
    else:
        return AsyncSniffer(
            iface=input_interface,
            filter="ip and (tcp or udp)",
            prn=None,
            session=NewFlowSession,
            store=False,
        )


def main():
    S = None  # Declare the timer variable and initialize it to None

    parser = argparse.ArgumentParser()

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-i",
        "--interface",
        action="store",
        dest="input_interface",
        help="capture online data from INPUT_INTERFACE",
    )

    input_group.add_argument(
        "-f",
        "--file",
        action="store",
        dest="input_file",
        help="capture offline data from INPUT_FILE",
    )

    output_group = parser.add_mutually_exclusive_group(required=False)
    output_group.add_argument(
        "-c",
        "--csv",
        action="store_const",
        const="csv",
        dest="output_mode",
        help="output flows as csv",
    )

    # added timer agrument
    timer = parser.add_mutually_exclusive_group(required=False)
    timer.add_argument(
        "-t",
        action="store",
        dest="timer",
        help="give the time interval for capture (in seconds).",
    )

    # added datetime file name agrument
    file_name = parser.add_mutually_exclusive_group(required=False)
    file_name.add_argument(
        "-fn",
        action="store_const",
        const=True,
        dest="file_name",
        help="pass this argument if you want to save the filename with datetime",
    )

    parser.add_argument(
        "output",
        help="output file name (in flow mode) or directory (in sequence mode)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="more verbosity")

    args = parser.parse_args()

    if args.file_name is not None:
        # changed the output file name to avoid any mismatch of collecting continious traffic
        date_str = str(datetime.today())
        if '/' in args.output:
            args.output = args.output.rsplit('/', 1)[0] + "/" + \
                date_str.split('.', -1)[0].replace(' ', '-') + '.csv'
        else:
            args.output = date_str.split('.', -1)[0].replace(' ', '-') + '.csv'

    sniffer = create_sniffer(
        args.input_file,
        args.input_interface,
        args.output_mode,
        args.output,
        args.verbose,
    )
    sniffer.start()

    # Check if a timer argument is provided
    if args.timer is not None:
        # Using a timer to stop the script after the specified time
        S = th.Timer(int(args.timer), sniffer.stop)
        S.start()

    try:
        sniffer.join()
    except KeyboardInterrupt:
        if S is not None:
            S.cancel()
        sniffer.stop
        # sniffer.stop()
    finally:
        sniffer.join()


if __name__ == "__main__":
    main()
