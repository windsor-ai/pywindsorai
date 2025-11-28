class DatePresets:
    """Predefined date ranges supported by the API."""

    TODAY = "today"
    YESTERDAY = "yesterday"
    LAST_7D = "last_7d"
    LAST_30D = "last_30d"
    LAST_90D = "last_90d"
    LAST_180D = "last_180d"
    LAST_MONTH = "last_month"
    LAST_YEAR = "last_year"


class UnifiedFields:
    """
    The most common fields available across Windsor.ai connectors.
    Derived from connector availability analysis.
    """

    # Time/Date Dimensions
    TODAY = "today"
    DATE = "date"
    YEAR = "year"
    WEEK = "week"
    YEAR_WEEK_ISO = "year_week_iso"
    YEAR_WEEK = "year_week"
    YEAR_OF_WEEK_ISO = "year_of_week_iso"
    YEAR_OF_WEEK = "year_of_week"
    YEAR_MONTH = "year_month"
    WEEK_ISO = "week_iso"
    WEEK_DAY_ISO = "week_day_iso"
    WEEK_DAY = "week_day"
    MONTH = "month"
    DAY_OF_MONTH = "day_of_month"

    # Dimensions
    SOURCE = "source"
    DATASOURCE = "datasource"
    ACCOUNT_ID = "account_id"
    ACCOUNT_NAME = "account_name"
    CAMPAIGN = "campaign"
    CAMPAIGN_ID = "campaign_id"
    CAMPAIGN_NAME = "campaign_name"
    CAMPAIGN_STATUS = "campaign_status"
    CAMPAIGN_TYPE = "campaign_type"
    AD_ID = "ad_id"
    CREATIVE_ID = "creative_id"
    COUNTRY = "country"
    CURRENCY = "currency"
    PRODUCTS_ID = "products__id"

    # CRM / User Data
    USERS_ID = "users__id"
    USERS_EMAIL = "users__email"
    USERS_NAME = "users__name"

    # Metrics
    CLICKS = "clicks"
    IMPRESSIONS = "impressions"
    SPEND = "spend"
    TOTALCOST = "totalcost"
    CTR = "ctr"
    CPC = "cpc"
    CPM = "cpm"
    CPA = "cpa"
    CONVERSIONS = "conversions"
