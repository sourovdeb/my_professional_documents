#!/usr/bin/env python3
"""
Email Outreach Generator
Generate personalized job inquiry and collaboration emails from templates

Usage:
    python3 email_outreach_generator.py --type job --company "ACME Inc" --contact "john@acme.fr"

Requires:
    pip install jinja2 pandas
"""

import argparse
from datetime import datetime
import csv
import json
from pathlib import Path

class EmailGenerator:
    def __init__(self):
        self.templates = self._load_templates()
        self.output_dir = Path('email_drafts')
        self.output_dir.mkdir(exist_ok=True)

    def _load_templates(self):
        """Email templates for different scenarios"""
        return {
            'job_inquiry': {
                'subject': 'English Teaching Position - {name} | {company}',
                'body': """Dear {contact_name},

I'm reaching out regarding teaching opportunities at {company}. With my background in {background}, I'm confident I can contribute to your language program.

Key strengths:
- CELTA certification and {years} years of teaching experience
- Specialized in {specialization}
- Proven track record with {demographics}

I'd appreciate the opportunity to discuss how I can add value to your team.

Best regards,
{sender_name}
{sender_email}
{sender_phone}"""
            },

            'collaboration_partnership': {
                'subject': 'Partnership Opportunity - {name} & {company}',
                'body': """Hi {contact_name},

I admire your work in {industry}, and I think our backgrounds could create valuable synergy.

I specialize in:
- {specialization_1}
- {specialization_2}
- {specialization_3}

Potential collaboration areas:
1. {collaboration_idea_1}
2. {collaboration_idea_2}

Would you be open to a 15-minute call to explore this?

Best,
{sender_name}
{sender_email}"""
            },

            'writing_partnership': {
                'subject': 'Writing Partnership - {name}',
                'body': """Hi {contact_name},

I've read your work on {topic} and think we share a philosophy about {shared_interest}.

I'm building a publication focused on {publication_focus} and believe your perspective would resonate with our audience.

Would you be interested in:
- Co-authoring a series on {topic}?
- Contributing monthly essays?
- Being featured in our newsletter?

Let me know your thoughts.

{sender_name}
{sender_email}"""
            },

            'workshop_proposal': {
                'subject': 'Workshop Proposal: {workshop_title} | {organization}',
                'body': """Dear {contact_name},

I'd like to propose a workshop: "{workshop_title}"

**Target audience:** {target_audience}
**Duration:** {duration}
**Key outcomes:**
- {outcome_1}
- {outcome_2}
- {outcome_3}

I've successfully delivered similar programs to {past_audiences}.

Materials and testimonials available upon request.

Regards,
{sender_name}
{sender_email}"""
            },

            'freelance_pitch': {
                'subject': 'Freelance Opportunity - {service_type} for {company}',
                'body': """Hi {contact_name},

I noticed {company} is in the {industry} space. I offer {service_type} services that have helped {past_clients_type} with {results}.

Services:
- {service_1}: {description_1}
- {service_2}: {description_2}

I'm available for {engagement_type} projects starting {start_date}.

Portfolio: {portfolio_link}

Let's discuss a fit.

{sender_name}"""
            }
        }

    def generate(self, email_type, **variables):
        """Generate email from template"""
        if email_type not in self.templates:
            raise ValueError(f"Unknown email type: {email_type}")

        template = self.templates[email_type]

        try:
            subject = template['subject'].format(**variables)
            body = template['body'].format(**variables)
        except KeyError as e:
            raise ValueError(f"Missing variable: {e}")

        return {
            'subject': subject,
            'body': body,
            'type': email_type,
            'generated_at': datetime.now().isoformat()
        }

    def save_as_draft(self, email_data, format='md'):
        """Save email as markdown or txt draft"""
        filename = f"{email_data['type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        if format == 'md':
            filepath = self.output_dir / f"{filename}.md"
            content = f"""# Email Draft: {email_data['type']}

**Generated:** {email_data['generated_at']}
**Status:** Draft

## Subject

{email_data['subject']}

## Body

{email_data['body']}

---

## Notes for Review

- [ ] Personalization: Does this feel custom or generic?
- [ ] Tone: Is it professional yet human?
- [ ] Call to action: Is there a clear next step?
- [ ] Links: All URLs working?

**Ready to send?** Copy subject + body to Gmail and review for 24h before sending.
"""
        else:
            filepath = self.output_dir / f"{filename}.txt"
            content = f"SUBJECT: {email_data['subject']}\n\n{email_data['body']}"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def batch_generate(self, csv_file):
        """Generate emails from CSV with company data"""
        emails = []

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    email = self.generate(row['email_type'], **row)
                    emails.append(email)
                    self.save_as_draft(email)

            print(f"✓ Generated {len(emails)} email drafts")
            return emails
        except FileNotFoundError:
            print(f"❌ CSV file not found: {csv_file}")
            return []

    def print_preview(self, email_data):
        """Print email preview to console"""
        print("\n" + "="*80)
        print(f"✉️  EMAIL DRAFT: {email_data['type'].upper()}")
        print("="*80)
        print(f"\nTO: [recipient email]")
        print(f"SUBJECT: {email_data['subject']}")
        print("\n" + "-"*80)
        print(email_data['body'])
        print("-"*80)
        print(f"\n⏰ Generated: {email_data['generated_at']}")
        print("📋 Status: Review in 24h before sending\n")


def create_example_csv():
    """Create example CSV for batch generation"""
    example_file = 'email_batch_template.csv'

    headers = [
        'email_type',
        'company',
        'contact_name',
        'contact_email',
        'industry',
        'background',
        'years',
        'specialization',
        'demographics',
        'sender_name',
        'sender_email',
        'sender_phone'
    ]

    example_data = [
        [
            'job_inquiry',
            'France Langue',
            'Marie Dubois',
            'marie@francelangue.fr',
            'Language Education',
            'CELTA certification and curriculum development',
            '5',
            'Business English for professionals',
            'Corporate executives',
            'Sourov Deb',
            'sourov@example.com',
            '+33 6 12 34 56 78'
        ],
        [
            'collaboration_partnership',
            'Medium Publications',
            'Alex Chen',
            'alex@medium.com',
            'Writing & Publishing',
            'Mental health advocacy',
            'Disability inclusion in tech',
            'Writing & storytelling',
            'Collaboration on bipolar + neurodiversity topics',
            'Sourov Deb',
            'sourov@example.com',
            ''
        ]
    ]

    with open(example_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(example_data)

    print(f"✓ Created template: {example_file}")
    print("  Edit it with your company data, then run:")
    print(f"  python3 email_outreach_generator.py --batch {example_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate personalized email outreach from templates'
    )
    parser.add_argument('--type', choices=['job_inquiry', 'collaboration_partnership', 'writing_partnership', 'workshop_proposal', 'freelance_pitch'],
                       help='Email template type')
    parser.add_argument('--company', help='Company name')
    parser.add_argument('--contact-name', help='Contact person name')
    parser.add_argument('--contact-email', help='Contact email (for reference)')
    parser.add_argument('--background', help='Your background/expertise')
    parser.add_argument('--specialization', help='Your specialization')
    parser.add_argument('--batch', help='CSV file for batch generation')
    parser.add_argument('--create-template', action='store_true', help='Create example CSV template')

    args = parser.parse_args()

    generator = EmailGenerator()

    if args.create_template:
        create_example_csv()
        return

    if args.batch:
        generator.batch_generate(args.batch)
        print(f"✓ Drafts saved to: {generator.output_dir}/")
        print("📝 Review each draft before sending")
        return

    if not args.type:
        print("Error: Use --type or --batch or --create-template")
        parser.print_help()
        return

    # Build variables dict from command-line args
    variables = {
        'company': args.company or '[Company Name]',
        'contact_name': args.contact_name or '[Contact Name]',
        'contact_email': args.contact_email or '[email@company.com]',
        'background': args.background or '[Your background]',
        'specialization': args.specialization or '[Your specialization]',
        'sender_name': 'Sourov Deb',
        'sender_email': 'sourov@example.com',
        'sender_phone': '+33 6 XX XX XX XX',
        'years': '5',
        'demographics': '[your target audience]',
        'industry': '[industry]',
        'topic': '[topic]',
        'publication_focus': '[publication focus]'
    }

    try:
        email = generator.generate(args.type, **variables)
        generator.print_preview(email)
        filepath = generator.save_as_draft(email, format='md')
        print(f"💾 Saved as: {filepath}")
        print("📌 IMPORTANT: Review for 24h before sending")
    except ValueError as e:
        print(f"❌ Error: {e}")


if __name__ == '__main__':
    main()
