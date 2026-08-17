#!/usr/bin/env python3

import subprocess


def run_command(command):
    """
    Run a system command and return:
    (success, stdout, stderr)
    """

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5
        )

        return (
            result.returncode == 0,
            result.stdout.strip(),
            result.stderr.strip()
        )

    except Exception as e:
        return False, "", str(e)


def get_battery_info():
    """
    Read battery percentage and charging status.
    """

    try:
        import glob

        batteries = glob.glob(
            "/sys/class/power_supply/BAT*/"
        )

        if not batteries:
            return 0, "Unknown"

        battery = batteries[0]

        with open(
            battery + "capacity",
            "r"
        ) as f:
            capacity = int(f.read().strip())

        with open(
            battery + "status",
            "r"
        ) as f:
            status = f.read().strip()

        return capacity, status

    except Exception:
        return 0, "Unknown"


def get_available_profiles():
    """
    Get power profiles supported by power-profiles-daemon.
    """

    success, output, error = run_command(
        ["powerprofilesctl", "list"]
    )

    if not success:
        return []

    profiles = []

    for line in output.splitlines():

        line = line.strip()

        if line.startswith("*"):
            line = line[1:].strip()

        if line.startswith("performance"):
            profiles.append("performance")

        elif line.startswith("balanced"):
            profiles.append("balanced")

        elif line.startswith("power-saver"):
            profiles.append("power-saver")

    # Remove duplicates while preserving order
    return list(dict.fromkeys(profiles))


def get_current_profile():
    """
    Get the ACTUAL currently active Linux power profile.
    """

    success, output, error = run_command(
        ["powerprofilesctl", "get"]
    )

    if not success:
        return "unknown"

    profile = output.strip()

    if profile in (
        "performance",
        "balanced",
        "power-saver"
    ):
        return profile

    return "unknown"


def set_power_profile(profile):
    """
    Change the ACTUAL Linux power profile.

    Returns:
        (success, actual_profile)
    """

    valid_profiles = (
        "performance",
        "balanced",
        "power-saver"
    )

    if profile not in valid_profiles:
        return False, get_current_profile()

    # Check that the requested profile is actually supported
    available = get_available_profiles()

    if profile not in available:
        return False, get_current_profile()

    # Ask power-profiles-daemon to change the profile
    success, output, error = run_command(
        ["powerprofilesctl", "set", profile]
    )

    if not success:
        print(
            f"Power profile change failed: {error}"
        )

        return False, get_current_profile()

    # IMPORTANT:
    # Don't trust the command blindly.
    # Ask Linux what profile is actually active.
    actual_profile = get_current_profile()

    if actual_profile == profile:
        return True, actual_profile

    return False, actual_profile


def get_power_info():
    """
    Return complete power information for the GUI.
    """

    battery, status = get_battery_info()

    current_profile = get_current_profile()

    available_profiles = get_available_profiles()

    return {
        "battery": battery,
        "status": status,
        "profile": current_profile,
        "available_profiles": available_profiles
    }


# ------------------------------------------------------------
# COMMAND LINE TEST
# ------------------------------------------------------------

if __name__ == "__main__":

    print("Acer Control Center - Power")
    print("=" * 40)

    info = get_power_info()

    print(
        f"Battery: {info['battery']}%"
    )

    print(
        f"Status: {info['status']}"
    )

    print(
        f"Current profile: {info['profile']}"
    )

    print(
        "Available profiles: "
        + ", ".join(info["available_profiles"])
    )

    print()

    print("Testing profile switching...")
    print()

    for profile in (
        "performance",
        "balanced",
        "power-saver"
    ):

        print(
            f"Switching to: {profile}"
        )

        success, actual = set_power_profile(
            profile
        )

        if success:
            print(
                f"SUCCESS - Actual profile: {actual}"
            )
        else:
            print(
                f"FAILED - Actual profile: {actual}"
            )

        print()
