# Bengali Media Implementation Guide

## Technical Stack

### Streaming Platform
- **Primary**: AzuraCast (self-hosted on DigitalOcean VPS)
  - Cost: $20/month
  - Features: Web-based management, listener statistics, auto-DJ
- **Alternative**: Icecast (open-source streaming server)
- **Backup**: SoundCloud for archived content

### Website
- **Platform**: WordPress with custom theme
- **Hosting**: DigitalOcean or Netlify
- **Features**:
  - Program schedule
  - Contributor profiles
  - Audio archive
  - Donation system
  - Live streaming player

### Mobile App (Future)
- **Platform**: React Native
- **Features**:
  - Live streaming
  - Offline listening
  - Push notifications
  - Contributor portal

## Content Production

### Equipment
- **Basic**: Smartphone + external mic ($50-100)
- **Intermediate**: Raspberry Pi + USB mic + portable recorder ($200-300)
- **Advanced**: Professional recorder + XLR mics ($1,000+)

### Workflow
1. **Recording**: Use Audacity or mobile app
2. **Editing**: Remove errors, normalize audio, add intro/outro
3. **Metadata**: Tag with title, description, contributors, date
4. **Upload**: To streaming server and archive
5. **Promotion**: Social media, newsletter, community networks

### Quality Standards
- Minimum 128kbps bitrate
- 44.1kHz sample rate
- Mono or stereo as appropriate
- ID3 tags for all metadata
- File naming: YYYY-MM-DD_Title_Contributor.mp3

## Legal Considerations

### India-Specific Regulations
- **Community Radio**: Requires license from Ministry of Information & Broadcasting
- **Online Streaming**: Fewer restrictions, but must comply with IT Rules 2021
- **Copyright**: Ensure all music/content is properly licensed or original
- **Defamation**: Avoid content that could lead to legal action

### Compliance Checklist
- [ ] Verify content does not violate IT Rules 2021
- [ ] Obtain necessary music licenses
- [ ] Include disclaimers about user-generated content
- [ ] Implement content moderation system
- [ ] Maintain records of all broadcast content

## Budget Breakdown

### Initial Setup ($1,500)
- VPS hosting: $600 (3 years at $20/month)
- Domain registration: $100 (3 years)
- Equipment: $500 (3 recording kits)
- Legal consultation: $300

### Monthly Operating Costs ($250)
- VPS hosting: $20
- Domain renewal: $8
- Marketing: $100
- Contributor stipends: $100
- Miscellaneous: $22

### Revenue Streams
- Sponsorships: $500-2,000/month (target)
- Donations: $200-1,000/month (target)
- Grants: $5,000-20,000/year (target)
- Merchandise: $100-500/month (future)