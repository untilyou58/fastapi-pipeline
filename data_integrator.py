import requests
from datetime import datetime


def fetch_data_from_api(endpoint):
    response = requests.get(f"http://localhost:8000{endpoint}")
    return response.json()


def data_integrator():
    weather_data = fetch_data_from_api("/api/weather")
    traffic_data = fetch_data_from_api("/api/traffic")
    event_data = fetch_data_from_api("/api/events")

    for weather, traffic, event in zip(weather_data, traffic_data, event_data):
        yield {
            "date": weather["date"],
            "weather": weather,
            "traffic": traffic,
            "event": event,
        }


def plan_week():
    today = datetime.now().date()
    for day_data in data_integrator():
        date = datetime.strptime(day_data["date"], "%Y-%m-%d").date()
        weather = day_data["weather"]
        traffic = day_data["traffic"]
        event = day_data["event"]

        if date == today:
            continue  # 今日のデータはスキップ

        plan = f"Day: {date}\n"
        plan += (
            f"Weather: {weather['condition']}, Temperature: {weather['temperature']}℃\n"
        )
        plan += f"Traffic: Congestion {traffic['congestion_level']}, expected delay {traffic['delay_minutes']} minutes\n"
        plan += f"Events: {event['event_name']} @ {event['location']}\n"

        if weather["condition"] == "雨" and traffic["congestion_level"] == "高":
            plan += "Action Plan: Telecommuting is recommended.\n"
        elif (
            weather["condition"] in ["晴れ", "曇り"]
            and traffic["congestion_level"] == "低"
        ):
            if event["event_name"] != "イベントなし":
                plan += f"Plan of action: a great day to work in the office. How about joining {event['event_name']} after work?\n"
            else:
                plan += "Plan of action: a great day to work in the office.\n"
        else:
            plan += "Plan of Action: No problem with normal schedule.\n"

        yield plan


if __name__ == "__main__":
    print("Next week's action plan:")
    for daily_plan in plan_week():
        print(daily_plan)
        print("-" * 40)
