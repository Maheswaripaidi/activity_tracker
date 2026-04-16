def generate_narration(events):
    report = []
    last_window = None

    for timestamp, event_type, details in events:

        # Session Start
        if event_type == "session" and "started" in details:
            report.append(f"\n Session Started at {timestamp}")

        #  Session End
        elif event_type == "session" and "ended" in details:
            report.append(f"\n Session Ended at {timestamp}")

        #  Window Activity (Avoid duplicates)
        elif event_type == "window":
            if details != last_window:
                report.append(f"{timestamp} - {details}")
                last_window = details

        #  Smart Text Input
        elif event_type == "text":
            report.append(f"{timestamp} - {details}")

        # Idle Time
        elif event_type == "idle":
            report.append(f"{timestamp} - {details}")

        # Ignore noisy logs
        elif event_type in ["mouse", "keyboard"]:
            continue

    return "\n".join(report)