from django.core.management.base import BaseCommand
from blog.models import BlogCategory, Post

class Command(BaseCommand):
    help = "Seed initial high-impact blog posts and categories"

    def handle(self, *args, **options):
        self.stdout.write("Seeding blog categories and articles...")

        cat_ai, _ = BlogCategory.objects.get_or_create(
            slug="ai-automation",
            defaults={"name": "AI Systems & Automation", "description": "Cutting-edge artificial intelligence systems driving business revenue.", "order": 1}
        )
        cat_web, _ = BlogCategory.objects.get_or_create(
            slug="web-engineering",
            defaults={"name": "Web Architecture & Performance", "description": "High-speed modern web engineering and digital conversion platforms.", "order": 2}
        )
        cat_growth, _ = BlogCategory.objects.get_or_create(
            slug="growth-strategy",
            defaults={"name": "Client Acquisition & CRO", "description": "Actionable tactics for generating, qualifying, and closing inbound clients.", "order": 3}
        )

        posts_data = [
            {
                "category": cat_ai,
                "title": "Why A Static Website Is Costing You Clients: The Era of AI Lead Qualification Engines",
                "slug": "why-static-website-costs-you-clients-ai-lead-qualification",
                "author_name": "Lawrence Otieno",
                "author_role": "Founder & Principal Solutions Architect",
                "excerpt": "Most business websites function like static digital brochures that leak 95% of their traffic. Discover how pairing your website with an autonomous AI qualification engine transforms cold visitors into booked sales calls.",
                "read_time": "6 min read",
                "tags": "AI Systems, Lead Generation, Web Development, Automation, Business Growth",
                "is_featured": True,
                "content": """
                <p class="lead">For over a decade, businesses operated under a simple premise: build a clean website, list your phone number and contact form, and wait for the phone to ring. In 2026, that playbook is officially obsolete.</p>
                
                <h2>The 95% Traffic Leak Problem</h2>
                <p>When high-intent prospects search for your services—whether you are a clinic, a furniture retailer, a real estate developer, or an engineering firm—they expect instant answers. If your website simply displays an email address or an unmonitored contact form, over 95% of those visitors will bounce to your competitor who responds within seconds.</p>

                <blockquote>"A website without an automated qualification and follow-up system is not an asset; it is an expensive digital placeholder."</blockquote>

                <h2>What Is An AI Client Acquisition Engine?</h2>
                <p>At UniqueTechCamp, we architect websites as the high-speed frontend of an intelligent client capture pipeline. Here is what happens when a prospect lands on an AI-powered website:</p>
                <ul>
                    <li><strong>Instant 24/7 Engagement:</strong> The conversational bot greets the visitor based on the exact page they are viewing (e.g., pricing, dental implants, luxury sofas).</li>
                    <li><strong>Autonomous Qualification:</strong> The AI asks targeted screening questions: What is your timeline? What is your budget range? What specific challenges are you looking to resolve?</li>
                    <li><strong>Zero Friction Booking:</strong> Qualified buyers can book a physical or virtual appointment directly into your calendar.</li>
                    <li><strong>Multi-Channel Follow-Up:</strong> If a user leaves their phone number but drops off before booking, an automated WhatsApp sequence engages them within 10 minutes with helpful guidance.</li>
                </ul>

                <h2>Turning Visitors Into Predictable Income</h2>
                <p>When you shift your perspective from buying a commodity "website" to deploying an integrated "Customer Growth Engine", your digital presence stops being a cost center and becomes your most profitable, indefatigable sales rep.</p>
                """
            },
            {
                "category": cat_growth,
                "title": "WhatsApp Sales Automation in Africa: From Casual Chats to High-Ticket Closings",
                "slug": "whatsapp-sales-automation-africa-high-ticket-closings",
                "author_name": "UniqueTechCamp Strategy Team",
                "author_role": "Revenue Operations Unit",
                "excerpt": "In emerging markets, commerce moves on WhatsApp. Learn how integrating official WhatsApp API automation with your web storefront yields a 98% message open rate and eliminates sales delays.",
                "read_time": "5 min read",
                "tags": "WhatsApp Automation, Meta API, Sales Funnel, CRM, Africa Tech",
                "is_featured": True,
                "content": """
                <p>While email open rates struggle to top 18%, WhatsApp messages boast an astonishing 98% open rate—with over 80% of messages opened within five minutes of delivery.</p>

                <h2>Why Traditional Form Fills Fail</h2>
                <p>Standard website checkout and contact forms create excessive friction on mobile screens. Consumers in Kenya and across Africa prefer discussing specifications, delivery dates, and custom pricing via WhatsApp. However, relying on manual human replies means leads go cold after hours, over weekends, and during busy afternoon rushes.</p>

                <h2>The Automated WhatsApp Solution</h2>
                <p>By connecting your website directly to an enterprise WhatsApp automation workflow:</p>
                <ol>
                    <li>A visitor clicks "Inquire on WhatsApp" on any product or service page.</li>
                    <li>The message is pre-populated with the exact service SKU or package name.</li>
                    <li>Our AI bot answers common questions, presents downloadable brochures, and collects customer requirements.</li>
                    <li>Hot deals trigger an instant notification to your sales manager's phone with complete lead qualification notes.</li>
                </ol>

                <p>The result? You capture leads before they look elsewhere, and your team spends their time closing deals rather than answering repetitive pricing queries.</p>
                """
            },
            {
                "category": cat_web,
                "title": "Sub-Second Speed & Modern Architecture: Why Web Performance Determines Your Google Rank",
                "slug": "sub-second-speed-modern-web-architecture-google-ranking",
                "author_name": "Technical Architecture Desk",
                "author_role": "Engineering Unit",
                "excerpt": "Discover how Core Web Vitals, server-side caching, and modern CSS frameworks like Tailwind deliver blazing fast page loads that delight users and dominate search rankings.",
                "read_time": "4 min read",
                "tags": "Web Performance, SEO, Core Web Vitals, Tailwind CSS, Django",
                "is_featured": False,
                "content": """
                <p>Google has made it unequivocally clear: page experience and loading speed directly dictate your organic search positioning. If your website takes longer than 2.5 seconds to render on a standard 4G mobile connection, over 53% of mobile visitors abandon the session before seeing your headline.</p>

                <h2>The Anatomy of High-Performance Web Engineering</h2>
                <p>At UniqueTechCamp, we build web applications using modern, lightweight architectures that bypass bloated drag-and-drop page builders. Every page is crafted with:</p>
                <ul>
                    <li><strong>Asset Compression & Modern Formats:</strong> Next-gen WebP/AVIF images and vector iconography.</li>
                    <li><strong>Zero Render-Blocking Scripts:</strong> Asynchronous script loading and optimized CSS stylesheets.</li>
                    <li><strong>Semantic Schema Markup:</strong> Rich JSON-LD microdata enabling rich snippets in Google search results.</li>
                </ul>

                <p>When speed meets compelling sales copy and AI lead qualification, your website transforms into an unstoppable revenue asset.</p>
                """
            },
            {
                "category": cat_ai,
                "title": "How Healthcare & Dental Clinics Double Patient Consultations with Instant AI Intake",
                "slug": "how-healthcare-dental-clinics-double-patient-consultations-ai",
                "author_name": "Lawrence Otieno",
                "author_role": "Lead Architect",
                "excerpt": "Medical and aesthetic practices lose dozens of high-value procedures every month to slow receptionist responses. See how 24/7 AI intake bots streamline triage and appointment bookings.",
                "read_time": "7 min read",
                "tags": "Healthcare, Dental Clinics, AI Intake, Booking Systems, Patient Care",
                "is_featured": False,
                "content": """
                <p>Patients seeking specialized healthcare, dental procedures, or aesthetic consultations rarely call during office hours. Most conduct their private research late in the evening or early in the morning.</p>

                <h2>The Front-Desk Bottleneck</h2>
                <p>A typical clinic relies on front-desk receptionists who are overwhelmed with in-person patients, billing, and patient check-ins. Phone calls go unanswered, WhatsApp messages sit unread for hours, and prospective patients move to the next clinic on Google Maps.</p>

                <h2>Intelligent 24/7 Patient Intake</h2>
                <p>By deploying an automated AI healthcare intake assistant:</p>
                <ul>
                    <li>The patient receives immediate answers to treatment options, insurance acceptance, and operating hours.</li>
                    <li>The bot performs preliminary triage, collecting key health goals and procedure interests.</li>
                    <li>Available calendar slots are offered directly in chat, locking in patient consultations with automated SMS reminders.</li>
                </ul>

                <p>This automated intake operates seamlessly 24/7/365, turning your clinic's web presence into a patient acquisition machine.</p>
                """
            }
        ]

        for p in posts_data:
            post, created = Post.objects.update_or_create(
                slug=p["slug"],
                defaults={
                    "category": p["category"],
                    "title": p["title"],
                    "author_name": p["author_name"],
                    "author_role": p["author_role"],
                    "excerpt": p["excerpt"],
                    "read_time": p["read_time"],
                    "tags": p["tags"],
                    "content": p["content"],
                    "is_featured": p["is_featured"],
                    "is_published": True,
                }
            )
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} post: {post.title}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded blog posts!"))
