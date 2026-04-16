from logger import get_events, get_app_usage
from narrator import generate_narration
from summarizer import summarize_text


def create_report():
    #  Get events
    events = get_events()

    #  Generate narration
    narration = generate_narration(events)

    #  Generate summary
    lines = narration.split("\n")
    summary = summarize_text(lines)

    #  Get app usage
    app_usage = get_app_usage()

    usage_text = "\n\n Time Spent Per Application:\n"

    for app, duration in app_usage:

        # Skip useless apps
        if duration <= 0:
            continue

        #  Clean app name
        clean_name = app.split(" - ")[-1]

        #  Better time format
        if duration < 60:
            time_str = f"{duration} seconds"
        else:
            time_str = f"{round(duration / 60, 2)} minutes"

        usage_text += f"{clean_name} - {time_str}\n"

    #  Final output
    final_report = (
        " USER ACTIVITY REPORT\n\n"
        + narration
        + "\n\n"
        + summary
        + usage_text
    )

    return final_report


def export_report(filename="activity_report.txt"):
    report_text = create_report()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)