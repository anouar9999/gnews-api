from django.core.management.base import BaseCommand
from articles.models import SitePage

PAGES = {
    'about': {
        'stats': [
            {'label': 'Monthly Readers', 'value': '2.4M+'},
            {'label': 'Articles Published', 'value': '12,000+'},
            {'label': 'Countries Reached', 'value': '80+'},
            {'label': 'Years Online', 'value': '6+'},
        ],
        'story': [
            'GNEWZ was founded with a single obsession: deliver gaming news faster, more accurately, and more passionately than anyone else. What started as a small blog run by a group of competitive gamers has grown into one of the most-read gaming media outlets in the world.',
            'We cover everything — from AAA game releases and indie gems to GPU benchmarks, esports tournaments, and the culture that surrounds it all. Our editorial team plays the games they write about, tests the hardware they review, and watches every match they report on.',
            'We are independent. We are unsponsored. We are GNEWZ.',
        ],
        'values': [
            {'title': 'Speed', 'desc': 'We publish breaking news within minutes of it happening. Speed is our edge.'},
            {'title': 'Coverage', 'desc': 'Gaming, esports, hardware, and culture — if it matters to gamers, we cover it.'},
            {'title': 'Community', 'desc': 'We exist for our readers. Every story, every review, every opinion is for you.'},
            {'title': 'Integrity', 'desc': 'No paid reviews. No hidden agendas. We call it as we see it, every time.'},
        ],
    },
    'contact': {
        'info': [
            {'title': 'Email', 'val': 'hello@gnewz.com'},
            {'title': 'Press', 'val': 'press@gnewz.com'},
            {'title': 'Based in', 'val': 'Global — Remote'},
        ],
        'topics': [
            'General Inquiry',
            'Press & Media',
            'Advertising',
            'Technical Issue',
            'Content Submission',
            'Other',
        ],
    },
    'privacy-policy': {
        'sections': [
            {
                'title': '1. Information We Collect',
                'body': 'We collect information you provide directly, such as when you subscribe to our newsletter, submit a comment, or contact us. This includes your name, email address, and any content you submit.\n\nWe also automatically collect certain technical data when you visit GNEWZ, including your IP address, browser type, device information, pages visited, and time spent on the site. This data is collected through cookies and similar technologies.',
            },
            {
                'title': '2. How We Use Your Information',
                'body': 'We use the information we collect to:\n• Send you newsletters and content updates you have subscribed to\n• Respond to your comments and inquiries\n• Analyse site traffic and improve our content\n• Detect and prevent fraud or abuse\n• Comply with legal obligations\n\nWe do not sell your personal information to third parties.',
            },
            {
                'title': '3. Cookies',
                'body': 'GNEWZ uses cookies to enhance your browsing experience and analyse site usage. You can manage your cookie preferences through the cookie consent banner displayed on your first visit, or through your browser settings. For more details, please see our Cookie Policy.',
            },
            {
                'title': '4. Third-Party Services',
                'body': 'We may use third-party services such as analytics providers and advertising networks. These services may collect information about your online activities over time and across different websites. We encourage you to review their privacy policies.',
            },
            {
                'title': '5. Data Retention',
                'body': 'We retain your personal data only for as long as necessary to fulfil the purposes for which it was collected, or as required by law. Newsletter subscribers may unsubscribe at any time via the link included in every email.',
            },
            {
                'title': '6. Your Rights',
                'body': 'Depending on your location, you may have the right to access, correct, or delete your personal data. To exercise these rights, contact us at privacy@gnewz.com.',
            },
            {
                'title': '7. Changes to This Policy',
                'body': 'We may update this Privacy Policy from time to time. We will notify you of significant changes by posting a notice on our site. Continued use of GNEWZ after changes constitutes your acceptance of the updated policy.',
            },
        ],
    },
    'terms-of-use': {
        'sections': [
            {
                'title': '1. Acceptance of Terms',
                'body': 'By accessing or using GNEWZ, you agree to be bound by these Terms of Use. If you do not agree, please discontinue use of the site.',
            },
            {
                'title': '2. Use of Content',
                'body': 'All content on GNEWZ — including articles, images, videos, and graphics — is the property of GNEWZ or its content partners and is protected by copyright law.\n\nYou may share our content for non-commercial purposes with proper attribution and a link back to the original article. Republishing full articles without written permission is prohibited.',
            },
            {
                'title': '3. User Comments',
                'body': 'By submitting a comment, you grant GNEWZ a non-exclusive, royalty-free licence to publish and display that comment on our site.\n\nYou agree not to post content that is defamatory, harassing, unlawful, or spammy. We reserve the right to remove any comment at our discretion.',
            },
            {
                'title': '4. Newsletter',
                'body': 'By subscribing to our newsletter you consent to receive periodic emails from GNEWZ. You can unsubscribe at any time via the link in any of our emails.',
            },
            {
                'title': '5. Disclaimer',
                'body': 'GNEWZ provides content for informational and entertainment purposes. While we strive for accuracy, we make no warranties about the completeness or reliability of the information presented.',
            },
            {
                'title': '6. Limitation of Liability',
                'body': 'GNEWZ shall not be liable for any indirect, incidental, or consequential damages arising from your use of, or inability to use, this site or its content.',
            },
            {
                'title': '7. External Links',
                'body': 'Our site may contain links to third-party websites. We are not responsible for the content or privacy practices of those sites.',
            },
            {
                'title': '8. Changes to Terms',
                'body': 'We reserve the right to modify these terms at any time. Changes will be posted on this page with an updated date. Continued use of GNEWZ constitutes acceptance of the revised terms.',
            },
            {
                'title': '9. Governing Law',
                'body': 'These terms are governed by applicable law. Any disputes shall be resolved in the competent courts of the jurisdiction in which GNEWZ operates.',
            },
        ],
    },
    'cookie-policy': {
        'cookie_types': [
            {
                'name': 'Essential Cookies',
                'required': True,
                'desc': 'These cookies are necessary for the website to function. They enable core features such as security, session management, and cookie consent preferences. They cannot be disabled.',
                'examples': 'Session token, cookie consent preference',
            },
            {
                'name': 'Analytics Cookies',
                'required': False,
                'desc': 'These cookies help us understand how visitors interact with our website by collecting and reporting information anonymously. This data helps us improve our content and user experience.',
                'examples': 'Page views, time on page, referral source',
            },
            {
                'name': 'Preference Cookies',
                'required': False,
                'desc': 'These cookies remember your preferences and settings to personalise your experience on GNEWZ, such as your selected language.',
                'examples': 'Language selection, theme preference',
            },
            {
                'name': 'Advertising Cookies',
                'required': False,
                'desc': 'These cookies may be set by our advertising partners to build a profile of your interests and show you relevant ads on other sites. They do not store personal information directly.',
                'examples': 'Ad targeting, frequency capping',
            },
        ],
    },
}


class Command(BaseCommand):
    help = 'Seed initial content for the 5 static site pages.'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0
        for slug, content in PAGES.items():
            page, created = SitePage.objects.update_or_create(
                slug=slug,
                defaults={'content': content},
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {slug}'))
            else:
                updated_count += 1
                self.stdout.write(f'  Already exists (skipped update): {slug}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone. {created_count} created, {updated_count} already existed.'
            )
        )
