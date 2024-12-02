from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from ninja import NinjaAPI
from ninja.errors import HttpError
import json
import os

AnalyticsApi = NinjaAPI()


def get_google_analytics_client():
    try:
        file_path = os.path.join(
            os.path.dirname(__file__), "ga-probe-kadnya-55529bfe7f0f.json"
        )
        with open(file_path) as f:
            credentials = json.load(f)
        client = BetaAnalyticsDataClient.from_service_account_info(credentials)
        return client
    except FileNotFoundError:
        raise HttpError(404, "Credentials file not found.")
    except Exception as e:
        raise HttpError(500, f"Error initializing Google Analytics client: {str(e)}")


@AnalyticsApi.get("/fetch_analytics", tags=["Analytics"])
def fetch_google_analytics_data(request, property_id: str):
    client = get_google_analytics_client()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="city"),
            Dimension(name="country"),
            Dimension(name="deviceCategory"),
            Dimension(name="sessionSource"),
            Dimension(name="sessionMedium"),
            Dimension(name="sessionCampaignId"),
            Dimension(name="pagePath"),
        ],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="newUsers"),
            Metric(name="sessions"),
            Metric(name="screenPageViews"),
            Metric(name="averageSessionDuration"),
            Metric(name="engagementRate"),
            Metric(name="bounceRate"),
            Metric(name="sessionConversionRate"),
        ],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
    )

    try:
        response = client.run_report(request)
    except Exception as e:
        raise HttpError(500, f"Error fetching analytics data: {str(e)}")

    data = {
        "dimension_headers": [header.name for header in response.dimension_headers],
        "metric_headers": [header.name for header in response.metric_headers],
        "rows": [
            {
                "dimensions": [dim.value for dim in row.dimension_values],
                "metrics": [metric.value for metric in row.metric_values],
            }
            for row in response.rows
        ],
    }
    return data
