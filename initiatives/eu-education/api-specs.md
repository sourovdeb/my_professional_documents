# EU Education API Specifications

## Overview
API for accessing verified EU education opportunities, designed for third-party integration and mobile applications.

## Base URL
https://api.eu-education-initiative.org/v1

## Authentication
- API Key: Required for all endpoints (rate limited)
- OAuth 2.0: For user-specific data (optional)
- EU Login: Integration with EU authentication (future)

## Rate Limits
- Free Tier: 100 requests/hour
- Standard Tier: 1,000 requests/hour
- Enterprise Tier: 10,000 requests/hour

## Main Endpoints

### GET /opportunities
List all verified education opportunities.
Parameters: country, type, level, discipline, funding_min, deadline_from, deadline_to, language, limit, offset

### GET /opportunities/{id}
Get detailed information about a specific opportunity.

### GET /institutions
List all institutions in the database.
Parameters: country, type, limit, offset

### GET /institutions/{id}
Get detailed information about a specific institution.

### GET /countries
List all countries with opportunities.

### GET /countries/{code}
Get detailed information about opportunities in a specific country.

### GET /search
Full-text search across all opportunities.
Parameter: q (required)

### GET /stats
Get database statistics.

## Webhooks
- Opportunity Updates: POST /webhooks/opportunities
- Verification Status: POST /webhooks/verification

## Error Codes
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 429: Rate Limit Exceeded
- 500: Internal Server Error

## SDKs Available
- JavaScript
- Python
- More coming soon

## Versioning
- Current: v1
- Backward compatible: minor version increment
- Breaking changes: major version increment

## Support
- Documentation: https://docs.eu-education-initiative.org
- Status Page: https://status.eu-education-initiative.org
- Contact: support@eu-education-initiative.org