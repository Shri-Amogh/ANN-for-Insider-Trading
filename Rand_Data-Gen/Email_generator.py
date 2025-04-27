import random
import csv
from datetime import datetime, timedelta

# Settings
NUM_EMAILS = 1000
OUTPUT_FILE_EMAILS = "New_Emails.csv"

# Generate a pool of random email addresses
domains = [
    "company.com", "business.org", "finance.io", "techhub.net","venturecorp.com", 
    "cloudbase.org", "quantumfinance.io", "aerotechhub.net",
    "nextgenideas.com", "globalimpact.org", "fusionfund.io", "nanovate.net",
    "skylineventures.com", "openfuture.org", "stellarcapital.io", "nexustech.net",
    "zenithgroup.com", "brightpath.org", "infinityfunds.io", "pixelbyte.net",
    "elevateventures.com", "greenvision.org", "boldfinance.io", "hyperlooptech.net",
    "urbanflow.com", "socialimpact.org", "trustfinance.io", "cybernest.net",
    "primeventures.com", "newhorizons.org", "venturefunds.io", "techsphere.net",
    "solarisgroup.com", "sharedvalue.org", "blockcapital.io", "datamatrix.net",
    "lighthouseventures.com", "changemakers.org", "futurefunds.io", "smartgridtech.net",
    "peaktalent.com", "planetimpact.org", "shiftfinance.io", "xenonlabs.net",
    "clarityventures.com", "gogreen.org", "quantfinance.io", "cosmotech.net",
    "bridgecapital.com", "globaldreams.org", "sunriseventures.io", "innovatrix.net",
    "highlineventures.com", "socialhub.org", "blueoceanfinance.io", "pulsartech.net",
    "brightfuture.com", "worldconnect.org", "vergefund.io", "lumostech.net",
    "allianceventures.com", "communityrise.org", "launchpadfinance.io", "astraedge.net",
    "synergycapital.com", "saveplanet.org", "yfinance.io", "helixhub.net",
    "forwardventures.com", "thinkchange.org", "fusionledger.io", "zentech.net",
    "momentumgroup.com", "socialcircle.org", "trustledger.io", "alphawave.net",
    "venturelane.com", "greenplanet.org", "nexgenfinance.io", "omnitechhub.net",
    "elevationventures.com", "powerchange.org", "skycapital.io", "cubixtech.net",
    "velocitygroup.com", "impactworld.org", "bravofinance.io", "nebulahub.net",
    "ascendventures.com", "rethinkchange.org", "aviatefinance.io", "orionlabs.net",
    "skyventures.com", "connectfuture.org", "bloomfinance.io", "galaxinet.net",
    "founderspath.com", "weareone.org", "glidefinance.io", "datacoretech.net",
    "zenventures.com", "resilientworld.org", "sparkfund.io", "quarkhub.net",
    "peakcapital.com", "solutionshub.org", "traversefinance.io", "etherealnet.net",
    "upliftventures.com", "betterplanet.org", "orbitfund.io", "photonlabs.net",
    "novaenterprises.com", "unityforce.org", "fluxfinance.io", "synapsetech.net",
    "futurelaunch.com", "peacenet.org", "rapidfund.io", "aetherlabs.net",
    "dynamicventures.com", "planetforce.org", "revolvefinance.io", "genometech.net",
    "earlybirdventures.com", "onefuture.org", "ignitefund.io", "lightyearlabs.net",
    "ventureforge.com", "forwardchange.org", "pillarfinance.io", "atomotech.net",
    "ascendantventures.com", "changepath.org", "gravitasfund.io", "infinilab.net",
    "springboardventures.com", "onetogether.org", "altitudeinvest.io", "catalysthub.net",
    "brightsparkventures.com", "globalforce.org", "vectorfund.io", "skyhubnet.net",
    "greenlightventures.com", "openplanet.org", "kryptonfund.io", "stellarhub.net",
    "launchworks.com", "newimpact.org", "zenithfund.io", "cloudcoretech.net",
    "seedhouseventures.com", "changemission.org", "ventureboost.io", "orbytech.net",
    "originventures.com", "planetunity.org", "spirefund.io", "nexabyte.net",
    "magnifyventures.com", "connectplanet.org", "novawealth.io", "bytecore.net",
    "boldvisionventures.com", "riseimpact.org", "venturewave.io", "matrixhub.net",
    "northstarnetwork.com", "betterfuture.org", "aurorafund.io", "gridlabs.net",
    "fusionlaunch.com", "earthconnect.org", "venturetrail.io", "cubictech.net",
    "polarisventures.com", "togetherimpact.org", "summitfinance.io", "synctech.net",
    "evolveventures.com", "harmonyplanet.org", "parallaxfund.io", "zenethub.net",
    "heliosventures.com", "impactforce.org", "terrafund.io", "hydronet.net",
    "startsmartventures.com", "globalunite.org", "quasarfinance.io", "orbitalhub.net",
    "trailblazerventures.com", "planetconnect.org", "pioneerfund.io", "vectortech.net",
    "brightworksventures.com", "oneworldimpact.org", "venturevista.io", "galacticnet.net",
    "ignitionventures.com", "futureforce.org", "altairfund.io", "infranethub.net",
    "propulsionventures.com", "planetgrowth.org", "impactwealth.io", "stratonet.net",
    "skytrailventures.com", "nextimpact.org", "venturecore.io", "stellarnet.net",
    "venturefirst.com", "horizonconnect.org", "aerofinance.io", "polarisnet.net",
    "forwardlaneventures.com", "unityimpact.org", "astrofund.io", "meteorhub.net",
    "alphaquestventures.com", "globalgrowth.org", "plasmacapital.io", "quantanet.net",
    "leapventures.com", "connectuniverse.org", "orbitalfinance.io", "spectrumhub.net",
    "beaconventures.com", "sharedplanet.org", "zenwealth.io", "astrobyte.net",
    "eclipseventures.com", "worldrise.org", "cometfund.io", "synergynet.net",
    "venturebeyond.com", "socialprogress.org", "gravitatefund.io", "solarishub.net",
    "futurefrontventures.com", "earthforce.org", "ionfinance.io", "quantumhub.net",
    "launchlaneventures.com", "onenationimpact.org", "impactorbit.io", "neutrinet.net",
    "venturecatalyst.com", "nextworld.org", "planetaryfund.io", "fusionbyte.net",
    "skyshiftventures.com", "changewave.org", "venturepulse.io", "aeronethub.net"
]

emails = []
while len(emails) < random.randint(90,800):
    user = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 10)))
    domain = random.choice(domains)
    address = f"{user}@{domain}"
    if address not in emails:
        emails.append(address)

# Random timestamp generator (7 days)
def random_timestamp():
    now = datetime.now()
    days_ago = random.randint(0, 30)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return (now - timedelta(days=days_ago, hours=hour, minutes=minute, seconds=second))

# Subject generator (simple corporate language)
subjects = [
    "Project Update", "Meeting Reminder", "Budget Review", "Team Sync", "Contract Discussion",
    "Weekly Report", "Client Feedback", "New Hire Onboarding", "Market Analysis", "Sales Numbers"
    "Quarterly Business Review and Next Steps",
    "Team Alignment Session – Updated Agenda",
    "Important: Action Items for Compliance Audit",
    "Leadership Strategy Meeting Follow-Up",
    "Final Review of Contract Terms and Conditions",
    "Weekly Operations Update and Priorities",
    "Client Satisfaction Survey Results and Analysis",
    "Employee Training Program – Launch Details",
    "Deep Dive into Market Trends and Opportunities",
    "Updated Sales Targets and Pipeline Status",
    "Annual Budget Planning and Resource Allocation",
    "Board of Directors – Pre-Meeting Brief",
    "Internal Policy Changes – Immediate Attention Required",
    "Strategic Partnership Proposal and Feedback Request",
    "Employee Recognition Awards – Nomination Open",
    "Critical IT System Maintenance Notification",
    "Project Milestone Review and Risk Assessment",
    "Customer Retention Strategy – Working Draft",
    "Year-End Financial Summary and Highlights",
    "Global Expansion Strategy – Discussion Points",
    "Onboarding Checklist for New Project Managers",
    "Brand Refresh Initiative – Creative Review",
    "Security Protocol Update – Please Read",
    "Vendor Contract Renewal – Decision Needed",
    "Upcoming Compliance Training – RSVP Required",
    "Supply Chain Optimization Project Status",
    "Risk Management Framework Updates",
    "Team Building Workshop – Save the Date",
    "HR Policy Updates for 2025",
    "Product Launch Timeline and Deliverables",
    "No Subject",
    "No Subject – Internal Memo",
    "No Subject (System Generated)",
    "Confidential: Executive Briefing Materials",
    "Sales Enablement Resources – New Additions",
    "Cross-Functional Team Collaboration Guidelines",
    "Performance Review Cycle – Timeline and Expectations",
    "Legal Review Required: New Vendor Agreements",
    "Urgent: System Downtime Notification",
    "Customer Journey Mapping – Insights and Next Steps",
    "Internal Survey: Help Shape Our Future Strategy",
    "CEO Town Hall – Questions Submission Open",
    "Updated Travel Policy – Effective Immediately",
    "End-of-Quarter Reporting Deadlines",
    "Operational Excellence Program Kick-Off",
    "Invitation: Industry Networking Event",
    "IT Security Best Practices – Quick Reference Guide",
    "Open Enrollment Period for Benefits Plan",
    "Expense Report Submission Reminder",
    "Workplace Safety and Compliance Training",
    "Employee Engagement Survey Results Discussion"
    "Department Budget Review – Immediate Response Needed",
    "Client Contract Finalization – Signature Required",
    "Monthly Revenue Report and Forecast Adjustments",
    "Performance Metrics – Q2 Insights and Actions",
    "Marketing Campaign Results – Full Analysis Attached",
    "Corporate Social Responsibility Initiatives – Update",
    "Office Reopening Guidelines and Safety Protocols",
    "New Client Onboarding Checklist and Assignments",
    "Reminder: Complete Mandatory Compliance Training",
    "Quarterly Investor Relations Update",
    "Cross-Department Collaboration Project Kickoff",
    "Launch Strategy Meeting – Revised Calendar",
    "Executive Leadership Development Program Details",
    "Data Privacy Policy Changes – Staff Awareness Required",
    "Important: Review Updated Employee Handbook",
    "Board Meeting Agenda and Prep Materials",
    "Strategic Goals Planning Session – Confirm Attendance",
    "Supply Chain Disruptions – Mitigation Plan Discussion",
    "Technology Innovation Roadmap – 2025 and Beyond",
    "Upcoming Product Demonstration – Internal Review",
    "Cybersecurity Threat Update – Action Required",
    "Urgent: Client Account Escalation Handling",
    "Internal Announcement: Promotions and Organizational Changes",
    "System Migration Downtime Notification – Prepare Accordingly",
    "Request for Proposal (RFP) Submission – Final Steps",
    "Employee Satisfaction Survey – Your Input Matters",
    "Expense Policy Update and Reimbursement Guidelines",
    "Confidential: Acquisition Opportunity Discussion",
    "Regional Sales Team Performance Summary",
    "IT System Upgrade – Migration Timeline Overview",
    "New Vendor Onboarding Process Guidelines",
    "Quarterly OKRs Review and Goal Alignment",
    "Project Greenlight: Final Feasibility Report",
    "Reminder: Town Hall Meeting This Friday",
    "End of Fiscal Year Checklist for Managers",
    "Client Portfolio Review and Retention Strategies",
    "Executive Summary: Product Roadmap for 2025",
    "Internal Project Deadlines – Urgent Status Update",
    "New Compliance Standards – Immediate Implementation Required",
    "Training Session Invite: Advanced Leadership Skills",
    "Talent Acquisition Strategy – Next Phase Planning",
    "Customer Feedback Analysis Report – Please Review",
    "Action Needed: System Access Permissions Update",
    "No Subject",
    "No Subject (Follow-up Required)",
    "No Subject – Draft Only",
    "No Subject – For Internal Use",
    "Sales Incentive Program Launch – Guidelines and Timeline",
    "Updated Payroll Processing Schedule",
    "Client Risk Assessment – New Procedures",
    "Important: Data Security Awareness Reminder",
    "R&D Department – Innovation Proposal Submissions Open",
    "Management Training Series – Enrollment Now Open",
    "Confidential: Strategic Workforce Planning",
    "Customer Support Case Escalation Process Changes",
    "New Hiring Manager Toolkit – Available Now",
    "Asset Management Review – Midyear Update",
    "Operational Risk Assessment Presentation",
    "Review and Approval: Final Project Scope Document",
    "Team Reorganization – Effective Next Quarter",
    "Remote Work Policy Update – Key Changes",
    "Technical Workshop Invite: Best Practices in Cloud Security",
    "Monthly KPI Dashboard – Full Report Inside",
    "New Partnership Announcement – Global Markets Expansion",
    "Corporate Giving Program – Annual Review",
    "Open Role Announcements – Referral Bonus Details",
    "Business Continuity Plan – Revised Draft",
    "New Employee Wellness Initiatives",
    "Customer Acquisition Strategy – Brainstorm Session",
    "Urgent Review: Pending Legal Agreements",
    "Annual Cybersecurity Audit Preparation",
    "Weekly Executive Briefing Packet",
    "Urgent: Vendor Compliance Certification Needed",
    "Upcoming Brand Launch Strategy Review",
    "Request for Feedback: Team Efficiency Improvement Plan",
    "Invitation: Product Beta Testing Team Recruitment",
    "End of Quarter Employee Recognition Nominations",
    "Client Satisfaction Improvement Plan",
    "Budget Overruns: Action Plan Discussion",
    "IT Helpdesk Service Level Agreement Update",
    "Mandatory System Security Patch Installation Notice",
    "Upcoming Sustainability Initiatives Workshop",
    "Global Leadership Forum – Preliminary Agenda",
    "Market Intelligence Report – May Edition",
    "Cross-Functional Innovation Challenge – Call for Ideas",
    "Expense Auditing Changes – New Process Overview",
    "Risk and Compliance Strategy Briefing",
    "Team Retreat Planning – Initial Survey",
    "Manager's Toolkit Update – New Resources",
    "Workforce Analytics Report – Insights and Recommendations",
    "Project Risk Registry – Urgent Updates Required",
    "Global Expansion Readiness Checklist",
    "Final Approvals Needed: Annual Goals Submission",
    "Reminder: Security Best Practices for Mobile Devices",
    "Upcoming Client Satisfaction Webinar – RSVP Now",
    "Procurement Policy Refresh – Staff Training Required",
    "COVID-19 Office Protocol Adjustments",
    "No Subject",
    "No Subject – Review Pending",
    "No Subject – Needs Edits",
    "No Subject – Final Copy"
]

# Email body length
def random_body_length():
    return random.randint(50, 500)  # characters

# Generate emails
email_logs = []

for _ in range(NUM_EMAILS):
    sender = random.choice(emails)
    receiver = random.choice([e for e in emails if e != sender])
    timestamp = random_timestamp()
    subject = random.choice(subjects)
    body_length = random_body_length()
    
    log = {
        "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "Sender": sender,
        "Receiver": receiver,
        "Subject": subject,
        "Body Length (characters)": body_length
    }
    email_logs.append(log)

# Sort by time
email_logs.sort(key=lambda x: x["Timestamp"])

# Save to CSV
with open(OUTPUT_FILE_EMAILS, "w", newline='') as csvfile:
    fieldnames = ["Timestamp", "Sender", "Receiver", "Subject", "Body Length (characters)"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for email in email_logs:
        writer.writerow(email)

print(f"✅ Generated {NUM_EMAILS} realistic emails into '{OUTPUT_FILE_EMAILS}'")
