#!/usr/bin/env python3
"""
Bipolar Wellness Tracker
Daily check-in system for mood, medications, sleep, and early warning signs

Usage:
  python bipolar_wellness_tracker.py --checkin     (daily check-in)
  python bipolar_wellness_tracker.py --weekly      (end-of-week review)
  python bipolar_wellness_tracker.py --stats       (show trends)
  python bipolar_wellness_tracker.py --warn        (alert on warning signs)
"""

import csv
from datetime import datetime, timedelta
from pathlib import Path
import json

TRACKER_FILE = Path(__file__).parent.parent / "Health_and_Wellbeing" / "wellness_log.csv"

def daily_checkin():
    """
    Interactive daily wellness check-in
    Asks 10 questions, saves to CSV
    """

    print("\n" + "="*60)
    print("DAILY BIPOLAR WELLNESS CHECK-IN")
    print("="*60 + "\n")

    date = datetime.now().strftime("%Y-%m-%d")
    time_of_day = datetime.now().strftime("%H:%M")

    # Medication
    meds = input("Did you take all medications today? (yes/no): ").lower() == "yes"

    # Sleep
    sleep_hours = input("How many hours did you sleep? (0-12): ")
    try:
        sleep_hours = float(sleep_hours)
    except:
        sleep_hours = 0

    # Mood
    print("Rate your mood on scale 1-10")
    print("  1-3: Depressed")
    print("  4-6: Mixed/Neutral")
    print("  7-10: Elevated/Happy")
    mood = input("Mood (1-10): ")
    try:
        mood = int(mood)
    except:
        mood = 5

    # Energy
    print("\nRate your energy on scale 1-10")
    print("  1-3: Very low, exhausted")
    print("  4-6: Normal")
    print("  7-10: High, racing")
    energy = input("Energy (1-10): ")
    try:
        energy = int(energy)
    except:
        energy = 5

    # Anxiety
    anxiety = input("\nRate anxiety on scale 1-10: ")
    try:
        anxiety = int(anxiety)
    except:
        anxiety = 3

    # Social
    social = input("Did you have social contact today? (yes/no): ").lower() == "yes"

    # Movement
    print("\nDid you move your body? (walk, exercise, stretch)")
    movement = input("Movement (yes/no): ").lower() == "yes"

    # Eating
    meals = input("\nHow many meals did you eat? (0-3): ")
    try:
        meals = int(meals)
    except:
        meals = 0

    # Warning signs
    print("\nAny warning signs? (racing thoughts, no sleep, spending, irritability, isolation)")
    warnings = input("Warning signs (describe or 'none'): ")

    # Notes
    notes = input("\nAny other notes?: ")

    # Check for danger signs
    danger_signs = []

    if sleep_hours < 4:
        danger_signs.append("Sleep < 4 hours (prodromal mania risk)")
    if energy >= 8 and mood >= 8 and sleep_hours < 6:
        danger_signs.append("High mood + energy + low sleep (mania pattern)")
    if mood <= 2 and energy <= 2:
        danger_signs.append("Severe depression (contact therapist)")
    if not meds:
        danger_signs.append("Missed medications (crucial for stability)")

    # Save to CSV
    row = {
        "Date": date,
        "Time": time_of_day,
        "Mood": mood,
        "Energy": energy,
        "Anxiety": anxiety,
        "Sleep_Hours": sleep_hours,
        "Medications_Taken": meds,
        "Social_Contact": social,
        "Movement": movement,
        "Meals": meals,
        "Warning_Signs": warnings,
        "Notes": notes,
        "Danger_Alert": "|".join(danger_signs) if danger_signs else ""
    }

    # Append to CSV
    file_exists = TRACKER_FILE.exists()

    with open(TRACKER_FILE, "a", newline="", encoding="utf-8") as f:
        fieldnames = list(row.keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    # Display summary
    print("\n" + "-"*60)
    print("✓ Check-in saved")
    print("-"*60)
    print(f"Date: {date}")
    print(f"Mood: {mood}/10 | Energy: {energy}/10 | Anxiety: {anxiety}/10")
    print(f"Sleep: {sleep_hours} hrs | Meals: {meals} | Movement: {'Yes' if movement else 'No'}")

    if danger_signs:
        print("\n⚠️  WARNING SIGNS DETECTED:")
        for sign in danger_signs:
            print(f"  • {sign}")
        print("\nConsider: Taking a mental health day, calling therapist, adjusting meds")

    print()

def weekly_review():
    """
    Review the week's patterns
    Identifies trends, triggers, improvements
    """

    if not TRACKER_FILE.exists():
        print("No data yet. Do daily check-ins first.")
        return

    rows = []
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Get last 7 days
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    week_rows = []

    for row in rows:
        try:
            row_date = datetime.strptime(row["Date"], "%Y-%m-%d")
            if row_date >= week_ago:
                week_rows.append(row)
        except:
            pass

    if not week_rows:
        print("No data for past week")
        return

    print("\n" + "="*60)
    print("WEEKLY WELLNESS REVIEW")
    print("="*60 + "\n")

    # Calculate averages
    moods = [int(r.get("Mood", 5)) for r in week_rows if r.get("Mood")]
    energies = [int(r.get("Energy", 5)) for r in week_rows if r.get("Energy")]
    sleeps = [float(r.get("Sleep_Hours", 7)) for r in week_rows if r.get("Sleep_Hours")]
    anxieties = [int(r.get("Anxiety", 3)) for r in week_rows if r.get("Anxiety")]

    meds_taken = sum(1 for r in week_rows if r.get("Medications_Taken") == "True")
    social_days = sum(1 for r in week_rows if r.get("Social_Contact") == "True")
    move_days = sum(1 for r in week_rows if r.get("Movement") == "True")

    avg_mood = sum(moods) / len(moods) if moods else 5
    avg_energy = sum(energies) / len(energies) if energies else 5
    avg_sleep = sum(sleeps) / len(sleeps) if sleeps else 7
    avg_anxiety = sum(anxieties) / len(anxieties) if anxieties else 3

    print(f"Days tracked: {len(week_rows)}")
    print(f"\nAverage Mood: {avg_mood:.1f}/10")
    print(f"Average Energy: {avg_energy:.1f}/10")
    print(f"Average Sleep: {avg_sleep:.1f} hours")
    print(f"Average Anxiety: {avg_anxiety:.1f}/10")

    print(f"\nMedication adherence: {meds_taken}/7 days")
    print(f"Social connection: {social_days}/7 days")
    print(f"Movement: {move_days}/7 days")

    # Trend analysis
    print("\n" + "-"*60)
    print("PATTERNS & INSIGHTS")
    print("-"*60)

    if avg_mood > 7:
        print("✓ Mood elevated this week (stable or slightly high)")
    elif avg_mood < 4:
        print("⚠️  Mood low this week (depressive phase)")
    else:
        print("✓ Mood relatively stable")

    if avg_sleep < 6:
        print("⚠️  Sleep below 6 hours (check for mania/anxiety)")
    elif avg_sleep > 9:
        print("⚠️  Sleep above 9 hours (may indicate depression)")
    else:
        print("✓ Sleep in healthy range")

    if meds_taken < 6:
        print("⚠️  Missed medications multiple days (critical)")
    else:
        print("✓ Medication adherence strong")

    if social_days < 3:
        print("⚠️  Low social contact (isolation risk)")
    else:
        print("✓ Good social connection")

    if move_days < 3:
        print("⚠️  Low movement (energy/mood impacts)")
    else:
        print("✓ Regular movement")

    print("\n" + "-"*60)
    print("RECOMMENDATIONS")
    print("-"*60)

    if meds_taken < 6:
        print("→ Set phone reminder for medications")
    if social_days < 3:
        print("→ Plan one social activity per day")
    if move_days < 3:
        print("→ Commit to 20-minute walk daily")
    if avg_sleep < 6 or avg_mood > 7:
        print("→ Contact therapist about mood changes")
    if avg_anxiety > 6:
        print("→ Increase coping strategies (breathing, movement)")

    print()

def show_stats():
    """Show long-term statistics and trends"""

    if not TRACKER_FILE.exists():
        print("No data yet. Do daily check-ins first.")
        return

    rows = []
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("No data")
        return

    print("\n" + "="*60)
    print("OVERALL WELLNESS STATISTICS")
    print("="*60 + "\n")

    moods = [int(r.get("Mood", 5)) for r in rows if r.get("Mood")]
    energies = [int(r.get("Energy", 5)) for r in rows if r.get("Energy")]
    sleeps = [float(r.get("Sleep_Hours", 7)) for r in rows if r.get("Sleep_Hours")]

    if moods:
        print(f"Total check-ins: {len(rows)}")
        print(f"Average mood: {sum(moods)/len(moods):.1f}/10")
        print(f"Mood range: {min(moods)}-{max(moods)}")
        print(f"\nAverage energy: {sum(energies)/len(energies):.1f}/10")
        print(f"Average sleep: {sum(sleeps)/len(sleeps):.1f} hours")

    print()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Bipolar Wellness Tracker")
    parser.add_argument("--checkin", action="store_true", help="Daily check-in")
    parser.add_argument("--weekly", action="store_true", help="Weekly review")
    parser.add_argument("--stats", action="store_true", help="Overall statistics")
    parser.add_argument("--warn", action="store_true", help="Show warnings from recent check-ins")

    args = parser.parse_args()

    if args.checkin:
        daily_checkin()
    elif args.weekly:
        weekly_review()
    elif args.stats:
        show_stats()
    elif args.warn:
        # Show recent danger signs
        if TRACKER_FILE.exists():
            with open(TRACKER_FILE, "r") as f:
                rows = list(csv.DictReader(f))
                recent = rows[-7:] if len(rows) > 7 else rows
                warnings = [r for r in recent if r.get("Danger_Alert")]
                if warnings:
                    print("\n⚠️  RECENT WARNING SIGNS:\n")
                    for w in warnings:
                        print(f"{w['Date']}: {w['Danger_Alert']}")
                else:
                    print("No recent warning signs detected ✓")
    else:
        # Default: daily check-in
        daily_checkin()
