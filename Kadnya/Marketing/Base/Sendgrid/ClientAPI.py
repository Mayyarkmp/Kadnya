import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    From,
    To,
    Cc,
    Bcc,
    Subject,
    Substitution,
    Header,
    CustomArg,
    SendAt,
    Content,
    MimeType,
    Attachment,
    FileName,
    FileContent,
    FileType,
    Disposition,
    ContentId,
    TemplateId,
    Section,
    ReplyTo,
    Category,
    BatchId,
    Asm,
    GroupId,
    GroupsToDisplay,
    IpPoolName,
    MailSettings,
    BccSettings,
    BccSettingsEmail,
    BypassBounceManagement,
    BypassListManagement,
    BypassSpamManagement,
    BypassUnsubscribeManagement,
    FooterSettings,
    FooterText,
    FooterHtml,
    SandBoxMode,
    SpamCheck,
    SpamThreshold,
    SpamUrl,
    TrackingSettings,
    ClickTracking,
    SubscriptionTracking,
    SubscriptionText,
    SubscriptionHtml,
    SubscriptionSubstitutionTag,
    OpenTracking,
    OpenTrackingSubstitutionTag,
    Ganalytics,
    UtmSource,
    UtmMedium,
    UtmTerm,
    UtmContent,
    UtmCampaign,
)

from Kadnya.Marketing.Base.Marketing_Interface import MarketingProvider

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")


class SendGridClient(MarketingProvider):
    @staticmethod
    def send_email(payload):
        message = Mail(
            from_email="OurEmail@kadnya.com",
            to_emails=payload["email"],
            subject="Marriage Proposal",
            plain_text_content="I want to marry you",
        )
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            status_code = response.status_code
            body = response.body
            # Handle status codes
            return 200, {"success": "True", "response": body}
        except Exception as e:
            print(e.message)
            return 500, {"error": "Server error occured"}

    @staticmethod
    def get_statistics(start_date, end_date, aggregated_by="day"):
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

        query_params = {
            "start_date": start_date,
            "end_date": end_date,
            "aggregated_by": aggregated_by,
        }

        try:
            response = sg.client.stats.get(query_params=query_params)
            status_code = response.status_code
            body = response.body
            # Handle status codes
            return 200, {"success": "True", "response": body}
        except Exception as e:
            print(e.message)
            return 500, {"error": "Server error occured"}
